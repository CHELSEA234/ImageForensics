## ImageForensics Demo

### Graph_pooling algorithm for the model parsing.
- Please first download weights into `./RED_weights`
- Run the bash file to call `RED.py` which generates a list of string, which predicts the hyperparameters used in the generative model.
```bash
  conda activate HiFi_Net_xiao
  bash RED.sh
```
- Please place the output string in the first row's second window, which is the placeholder in the previous design. 

### HiFi_Net for the image detection and manipulation.
- For each sample, we can produce results including one binary mask, detection score, 4 feature maps and one TSNE plot. All of these results need to go to the layout discussed beforehand. Please take a look on page 6 of [slides](https://docs.google.com/presentation/d/1SeVhILx0nB8tYWWkawuV9mAX2usNe3_epjOdQ8_Mk24/edit?usp=sharing).
- The quick usage on HiFi_Net with the new viz code.
```python
  from HiFi_Net import HiFi_Net 
  from PIL import Image
  ...
  from MulticoreTSNE import MulticoreTSNE as TSNE # pip install MulticoreTSNE
  ...
  import numpy as np

  HiFi = HiFi_Net()   # initialize
  img_path = 'asset/sample_1.jpg'

  ## detection
  res3, prob3, feat_map = HiFi.detect(args.img_path)
  HiFi.viz_feature_map(feat_map, args.img_path)    ## output 4 feature map, e.x. sample_1_feat_32.jpg, sample_1_feat_64.jpg ...
  print(res3, prob3)

  ## localization
  pred_mask_name = args.img_path.replace('.', '_pred_mask.')
  binary_mask = HiFi.localize(args.img_path)
  HiFi.viz_tsne_plot(args.img_path)   ## output tsne figure, e.x. sample_1_tsne.jpg, sample_2_tsne.jpg ...
  binary_mask = Image.fromarray((binary_mask*255.).astype(np.uint8))
  binary_mask.save(pred_mask_name)
```
- Please try to reproduce the results in `./asset`
```bash
  python HiFi_Net.py --img_path asset/sample_1.jpg
  python HiFi_Net.py --img_path asset/sample_2.jpg
  python HiFi_Net.py --img_path asset/sample_3.jpg
  python HiFi_Net.py --img_path asset/sample_4.png
```
