# ------------------------------------------------------------------------------
# Author: Xiao Guo (guoxia11@msu.edu)
# CVPR2023: Hierarchical Fine-Grained Image Forgery Detection and Localization
# ------------------------------------------------------------------------------
from utils.utils import *
from utils.custom_loss import IsolatingLossFunction, load_center_radius_api
from models.seg_hrnet import get_seg_model
from models.seg_hrnet_config import get_cfg_defaults
from models.NLCDetection_api import NLCDetection
from MulticoreTSNE import MulticoreTSNE as TSNE # pip install MulticoreTSNE
from PIL import Image
from glob import glob
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (5,5)
plt.rcParams['savefig.facecolor']='skyblue'

import cv2
import torch
import torch.nn as nn
import numpy as np
import argparse
import imageio.v2 as imageio

class HiFi_Net():
    '''
        FENET is the multi-branch feature extractor.
        SegNet contains the classification and localization modules.
        LOSS_MAP is the classification loss function class.
    '''
    def __init__(self):
        device = torch.device('cuda:0')
        device_ids = [0]

        FENet_cfg = get_cfg_defaults()
        FENet  = get_seg_model(FENet_cfg).to(device) # load the pre-trained model inside.
        SegNet = NLCDetection().to(device)
        FENet  = nn.DataParallel(FENet)
        SegNet = nn.DataParallel(SegNet)

        self.FENet  = restore_weight_helper(FENet,  "RED_weights/HRNet",  750001)
        self.SegNet = restore_weight_helper(SegNet, "RED_weights/NLCDetection", 750001)
        self.FENet.eval()
        self.SegNet.eval()

        self.center, self.radius = load_center_radius_api()
        self.LOSS_MAP = IsolatingLossFunction(self.center, self.radius).to(device)

    def _transform_image(self, image_name):
        '''transform the image.'''
        image = imageio.imread(image_name)
        image = Image.fromarray(image)
        image = image.resize((256,256), resample=Image.BICUBIC)
        image = np.asarray(image)
        image = image.astype(np.float32) / 255.
        image = torch.from_numpy(image)
        image = image.permute(2, 0, 1)
        image = torch.unsqueeze(image, 0)
        return image

    def _normalized_threshold(self, res, prob, threshold=0.5, verbose=False):
        '''to interpret detection result via omitting the detection decision.'''
        if res > threshold:
            decision = "Forged"
            prob = (prob - threshold) / threshold
        else:
            decision = 'Real'
            prob = (threshold - prob) / threshold
        print(f'Image being {decision} with the confidence {prob*100:.1f}.')

    def detect(self, image_name, verbose=False):
        """
            Para: image_name is string type variable for the image name.
            Return:
                res: binary result for real and forged.
                prob: the prob being the forged image.
        """
        with torch.no_grad():
            img_input = self._transform_image(image_name)
            output, feat_map = self.FENet(img_input)
            mask1_fea, mask1_binary, out0, out1, out2, out3 = self.SegNet(output, img_input)
            res, prob = one_hot_label_new(out3)
            res = level_1_convert(res)[0]
            if not verbose:
                return res, prob[0], feat_map
            else:
                self._normalized_threshold(res, prob[0])

    def viz_process(self, feat_map_viz, viz_name, resize_value):  
        '''use opencv to write the image.'''
        viz_name = viz_name.replace('.', f'_feat_{resize_value}.')
        feat_map_viz = feat_map_viz[:,:, np.newaxis]
        feat_map_viz = cv2.applyColorMap(feat_map_viz, cv2.COLORMAP_JET)
        if resize_value != 256:
            feat_map_viz = cv2.resize(feat_map_viz, (resize_value, resize_value), interpolation = cv2.INTER_AREA)
            feat_map_viz = cv2.resize(feat_map_viz, (256, 256), interpolation = cv2.INTER_AREA)
        cv2.imwrite(viz_name, feat_map_viz)

    def viz_feature_map(self, feat_map, img_name):
        """visualize the feature map."""
        feat_map = feat_map.detach().cpu().numpy()
        feat_map = (feat_map * 255.0).astype(np.uint8)
        self.viz_process(feat_map[0,62,:,:], img_name, 256)
        self.viz_process(feat_map[0,37,:,:], img_name, 128)
        self.viz_process(feat_map[0,6,:,:], img_name, 64)
        self.viz_process(feat_map[0,45,:,:], img_name, 32)

    def viz_tsne_plot(self, image_name):
        '''TSNE visualization.'''
        tsne_fig_name = image_name.replace('.', f'_tsne.')
        tsne_feat  = self.tsne_feat
        tsne_label = self.tsne_label

        ## tsne feature.
        tsne_feat = np.reshape(tsne_feat, (tsne_feat.shape[0], -1))
        center_feat = self.center.clone().cpu().numpy()
        center_feat = center_feat[np.newaxis,:]
        tsne_feat = np.concatenate((tsne_feat.T, center_feat), axis=0)

        tsne_label = np.reshape(tsne_label, (-1))
        center_label = np.array([2])
        tsne_label = np.concatenate((tsne_label, center_label), axis=0)

        tsne = TSNE(n_jobs=4)
        X_embedded = tsne.fit_transform(tsne_feat)
        vis_x = X_embedded[:, 0]
        vis_y = X_embedded[:, 1]
        plt.scatter(vis_x[tsne_label == 0], vis_y[tsne_label == 0], s=250, c='orange', marker='.')
        plt.scatter(vis_x[tsne_label == 1], vis_y[tsne_label == 1], s=250, c='blueviolet', marker='*')
        plt.scatter(vis_x[tsne_label == 2], vis_y[tsne_label == 2], s=350, c='black', marker='x')
        plt.clim(4.0, 4.5)
        plt.axis('off')
        plt.savefig(tsne_fig_name)

    def localize(self, image_name):
        """
            Para: image_name is string type variable for the image name.
            Return:
                binary_mask: forgery mask.
        """
        with torch.no_grad():
            img_input = self._transform_image(image_name)
            output, feat_map = self.FENet(img_input)
            mask1_fea, mask1_binary, out0, out1, out2, out3 = self.SegNet(output, img_input)
            pred_mask, pred_mask_score = self.LOSS_MAP.inference(mask1_fea)   # inference
            pred_mask_score = pred_mask_score.cpu().numpy()
            ## 2.3 is the threshold used to seperate the real and fake pixels.
            ## 2.3 is the dist between center and pixel feature in the hyper-sphere.
            ## for center and pixel feature please refer to "IsolatingLossFunction" in custom_loss.py
            pred_mask_score[pred_mask_score<2.3] = 0.
            pred_mask_score[pred_mask_score>=2.3] = 1.
            binary_mask = pred_mask_score[0]
            ## prepare tsne plot.
            self.tsne_label = binary_mask[::16,::16]
            self.tsne_feat  = mask1_fea[0,:,::16,::16].detach().cpu().numpy()
            return binary_mask

def inference(args):
    HiFi = HiFi_Net()   # initialize
    
    ## detection
    res3, prob3, feat_map = HiFi.detect(args.img_path)
    HiFi.viz_feature_map(feat_map, args.img_path)    ## output 4 feature map.
    print(res3, prob3) # 1 1.0
    
    ## localization
    pred_mask_name = args.img_path.replace('.', '_pred_mask.')
    binary_mask = HiFi.localize(args.img_path)
    HiFi.viz_tsne_plot(args.img_path)   ## output tsne figure.
    binary_mask = Image.fromarray((binary_mask*255.).astype(np.uint8))
    binary_mask.save(pred_mask_name)
    print("...over...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, default='asset/sample_3.jpg')
    parser.add_argument('--img_floder', type=str, default='asset/folder/')
    args = parser.parse_args()
    inference(args)