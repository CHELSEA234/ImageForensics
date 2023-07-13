from HiFi_Net import HiFi_Net
from PIL import Image
from io import BytesIO
import base64

from MulticoreTSNE import MulticoreTSNE as TSNE

import numpy as np
import imageio as imageio

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

    return detection, prob3, binary_mask

if __name__ == '__main__':
    
    img_path = 'asset/sample_1.jpg'
    #arr = imageio.imread(img_path)
    
    binary_mask = img_analysis(img_path)
    binary_mask.save('pred_mask.png')