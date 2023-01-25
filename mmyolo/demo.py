from mmdet.apis import init_detector, inference_detector
from mmyolo.utils import register_all_modules

register_all_modules()
config_file = 'yolov5_s-v61_syncbn_fast_8xb16-300e_coco.py'
checkpoint_file = 'yolov5_s-v61_syncbn_fast_8xb16-300e_coco_20220918_084700-86e02187.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')  # or device='cuda:0' 'cpu'
inference_detector(model, 'demo/demo.jpg')