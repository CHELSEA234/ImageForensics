from HiFi_Net import HiFi_Net
from PIL import Image
import numpy as np
import imageio as imageio

HiFi = HiFi_Net()

def analysis(img_array):
    ### detection
    res3, prob3 = HiFi.detect(img_array)

    # print(res3, prob3) 1 1.0
    HiFi.detect(img_array, verbose=True)

    ###localization
    binary_mask = HiFi.localize(img_array)
    binary_mask = Image.fromarray((binary_mask*255.).astype(np.uint8))

    return binary_mask

if __name__ == '__main__':
    
    img_path = 'asset/sample_1.jpg'
    arr = imageio.imread(img_path)
    
    binary_mask = analysis(arr)
    binary_mask.save('pred_mask.png')