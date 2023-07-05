# ImageForensics

- For each sample, we can produce results including one binary mask, detection score, 4 feature maps and one TSNE plot.
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
