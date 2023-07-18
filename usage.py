from HiFi_Net import HiFi_Net
from RED import main
from PIL import Image
from io import BytesIO
import base64

from MulticoreTSNE import MulticoreTSNE as TSNE

import numpy as np
import imageio as imageio
import argparse

HiFi = HiFi_Net()

# def analysis(img_array):
#     res3, prob3, feat_map = HiFi.detect(img_array)
#     HiFi.viz_feature_map(feat_map, img_path)
#     print(res3, prob3)

#     pred_mask_name = img_path.replace('.', '_pred_mask.')
#     binary_mask = HiFi.localize(img_path)
#     HiFi.viz_tsne_plot(img_path)
#     binary_mask = Image.fromarray((binary_mask*255.).astype(np.uint8))
#     #binary_mask.save(pred_mask_name)

#     return binary_mask

def img_analysis(img_path):
    res3, prob3, feat_map = HiFi.detect(img_path)
    HiFi.viz_feature_map(feat_map, 'result.png')
    print(res3, prob3)

    detection = "Real"
    if res3 == 1:
        detection = "Fake"
    
    imgdata = base64.b64decode(detection)
    filename = 'demo.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    pred_mask_name = img_path.replace('.', '_pred_mask.')
    binary_mask = HiFi.localize(img_path)
    HiFi.viz_tsne_plot('result.png')
    binary_mask = Image.fromarray((binary_mask*255.).astype(np.uint8))
    #binary_mask.save(pred_mask_name)

    parser = argparse.ArgumentParser()
    ## Configuration
    parser.add_argument('--img_path', type=str, default=img_path, help="the image path.")
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

    layer_string = main(args)

    return detection, prob3, binary_mask, layer_string

if __name__ == '__main__':
    
    img_path = 'asset/sample_1.jpg'
    #arr = imageio.imread(img_path)
    
    binary_mask = img_analysis(img_path)
    binary_mask.save('pred_mask.png')