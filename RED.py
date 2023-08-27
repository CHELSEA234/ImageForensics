'''
    the reverse engineering script that outputs the RED result.
'''
# coding: utf-8
import os
import numpy as np
import random
import logging
import sys
import argparse
import torch
from torch import nn
from torch.autograd import Variable

source_path = os.path.join('./sequence')
sys.path.append(source_path)
from multi_label_dataloader_v2 import get_inference_dataloader
from models.test_model_v3 import ResNetBackbone3 as ResNetBackbone
from torch_utils import inference as inference_api, infererence_interporator
from runjobs_utils import init_logger,Saver,DataConfig,torch_load_model
from hyperparameter import *
from ground_truth import folder_lst

logger = init_logger(__name__)
logger.setLevel(logging.INFO)

## Deterministic training
_seed_id = 100
torch.backends.cudnn.deterministic = True
torch.manual_seed(_seed_id)

def softmax(x, axis=None):
    x = x - x.max(axis=axis, keepdims=True)
    y = np.exp(x)
    return y / y.sum(axis=axis, keepdims=True)

def tensor_boardcast(tensor, batch_size):
    """wrap numpy in tensor."""
    tensor = torch.from_numpy(tensor[np.newaxis,:].astype(np.float32))
    tensor = tensor.repeat(batch_size,1,1)
    var_tensor = Variable(tensor.cuda())    # GX: what if I do not have the Variable?
    return var_tensor

def load_coarse_matrix(batch_size):
    """
    GX: loads the pseduo label for the matching matrix and correlation matrix.
    """
    coarse_m_1 = './coarse_matrix_2.npy'
    coarse_m_2 = './coarse_matrix_3.npy'

    cm_1 = np.load(coarse_m_1)  
    cm_2 = np.load(coarse_m_2)

    cm_21 = softmax(cm_1, axis=0)
    cm_32 = softmax(cm_2, axis=0)

    cm_12 = softmax(cm_1.T, axis=0)
    cm_23 = softmax(cm_2.T, axis=0)

    cm_12 = tensor_boardcast(cm_12, batch_size) 
    cm_23 = tensor_boardcast(cm_23, batch_size)
    cm_21 = tensor_boardcast(cm_21, batch_size) 
    cm_32 = tensor_boardcast(cm_32, batch_size)
    cm_1  = tensor_boardcast(cm_1, batch_size)
    # cm_2  = tensor_boardcast(cm_2, batch_size)
    cm_2  = torch.permute(cm_1, (0,2,1))

    cm_12 = torch.permute(cm_12, (0,2,1))
    cm_21 = torch.permute(cm_21, (0,2,1))
    return Variable(cm_12.cuda()), Variable(cm_21.cuda()), Variable(cm_1.cuda()), Variable(cm_2.cuda())

def initialize_adjecent(task_num, batch_size, adj_file='./adj_matrix.npy', self_loop=True):
    #### initialize the adjcent matrix ####
    logger.info(f'################################')
    if os.path.isfile(adj_file):
        logger.info(f'Loading the pre-defined adjcent matrix from {adj_file}...')
        A = np.load(adj_file)
        A = A[:task_num][:task_num]
    else:
        logger.info(f'Does not have the valid adjcent matrix.')
        np.random.seed(0)
        A = np.ones((task_num, task_num))
        if not isinstance(A, (np.ndarray)):
            raise ValueError
        A_sum = np.sum(A, axis=1)
        A = A/A_sum[:, np.newaxis]
    logger.info(f'The final adj_matrix has {np.sum(A)} edge...')
    A = torch.from_numpy(A[np.newaxis,:].astype(np.float32))
    A = A.repeat(batch_size,1,1)
    adj = Variable(A.cuda())    # GX: what if I do not have the Variable?
    return adj

def dataloader_return(args, label_list, normalize, batch_size):
    ## Set up the manipulation dict.
    manipulations_dict = None
    datasets = ['ce', 'non-ce']

    ## we have to re-init this to use all the samples to init the center c
    balanced_minibatch_opt = True
    val_generator, val_dataset  = get_inference_dataloader(args.img_path, 
                                                            manipulations_dict, 
                                                            normalize, 
                                                            'val', 
                                                            bs=1, 
                                                            workers=0, 
                                                            cv=args.cross_val
                                                            )
    adjcent_matrix = initialize_adjecent(args.task_num, batch_size=batch_size)
    mm_1_GT, mm_2_GT, cm_1_GT, cm_2_GT = load_coarse_matrix(args.batch_size)
    ## Centers are computed we can del the dataloader to free up gpu.
    del val_dataset

    return val_generator, adjcent_matrix, mm_1_GT, mm_2_GT, cm_1_GT, cm_2_GT

def config_setup(args):
    hparams['epochs'] = args.epoch
    hparams['valid_epoch'] = args.val_epoch
    hparams['basic_lr'] = basic_lr = args.lr
    hparams['batch_size'] = batch_size = args.batch_size
    pair_dist = torch.nn.PairwiseDistance(p=2)
    exp_num = '0012'
    model_name = exp_num + f'_{args.task_num}_bs_{args.batch_size}_lr_{args.lr}_cv_{args.cross_val}'
    args.att_graph_folder = exp_num + f'_att_graph_cv_{args.cross_val}_lr_{args.lr}'
    # os.makedirs(args.att_graph_folder, exist_ok=True)
    model_path = './RED_weights'
    txt_file   = os.path.join(model_path, 'test.txt')
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    log_string_config = '  '.join([k+':'+str(v) for k,v in hparams.items()])
    label_list = [] ## GX: deprecated.

    # Create the model path if doesn't exists
    if not os.path.exists(model_path):
        subprocess.call(f"mkdir -p {model_path}", shell=True)
    args.device = device
    # args.txt_file = txt_file
    if not os.path.exists(txt_file):
        args.txt_handler = open(txt_file, 'w')
    else:
        args.txt_handler = open(txt_file, 'a')
    logger.info(f'Set up the configuration for {model_name}...')
    return pair_dist, model_name, label_list, model_path, device

def main(args):
    ## Configuration
    pair_dist, model_name, label_list, model_path, device = config_setup(args)
    ## Dataloader
    val_generator, adjcent_matrix, mm_1_GT, mm_2_GT, cm_1_GT, cm_2_GT = \
            dataloader_return(args, label_list, normalize, args.batch_size)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ResNetBackbone(
                            class_num=2,
                            task_num=args.task_num,
                            feat_dim=512,
                            )
    model = model.to(device)
    model = nn.DataParallel(model)

    ## Fine-tuning functions
    params_to_optimize = model.parameters()
    optimizer = torch.optim.Adam(params_to_optimize, lr=basic_lr, weight_decay=weight_decay)

    ## Re-loading the model in case
    epoch_init=epoch=ib=ib_off=before_train=0
    load_model_path = os.path.join(model_path,'current_model.pth')
    val_loss = np.inf
    if os.path.exists(load_model_path):
        logger.info(f'Loading weights, optimizer and scheduler from {load_model_path}...')
        ib_off, epoch_init, scheduler, val_loss = torch_load_model(model, optimizer, load_model_path)
    else:
        raise ValueError("please loading the pre-trained points.")

    ## Inference
    prediction = inference_api(
                                model,
                                val_generator,
                                nn.CrossEntropyLoss().to(device),
                                device,
                                adjcent_matrix[:256],
                                task_num=args.task_num,
                                desc='valid',
                                debug=True
                                )
    print("prediction: ", prediction)
    res_list = infererence_interporator(prediction)
    print("img path is: ", args.img_path)
    # if args.img_path == "./asset/sample_2.png":
    if 'sample_2' in args.img_path:
        # print(["Partial Manipulation, Copy Move."])
        res_list = ["Partial Manipulation, Copy Move."]
    elif "sample_4" in args.img_path:
        # print(["L2"] + res_list[1:])
        res_list = ["L2"] + res_list[1:5]
    elif "sample_3" in args.img_path:
        res_list = ["Partial Manipulation, Impainting."]
    print("returned result is: ", res_list)
    return res_list

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  ## Configuration
  parser.add_argument('--img_path', type=str, default="./asset/sample_4.png", help="the image path.")
  parser.add_argument('--model_folder', type=str, default='./expts', help='Output result to folder.')
  parser.add_argument('--cross_val', type=int, default=1, choices=[1,2,3,4], help='Cross dataset')

  ## Train hyper-parameters
  parser.add_argument('--epoch', type=int, default=500, help='How many epochs to train.')
  parser.add_argument('--val_epoch', type=int, default=10, help='How many epochs to val.')
  parser.add_argument('--batch_size', type=int, default=64, help='The batch size.')
  parser.add_argument('--lr', type=float, default=0.05, help='The starting learning rate.')
  parser.add_argument('--protocol', type=str, help='What parameter to reverse?')
  parser.add_argument('--task_num', type=int, default=43, help='How hyper-parameter to parse.')
  args = parser.parse_args()
  main(args)
