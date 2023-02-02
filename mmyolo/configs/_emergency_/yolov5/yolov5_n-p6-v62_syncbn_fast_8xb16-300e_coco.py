_base_ = 'yolov5_s-p6-v62_syncbn_fast_8xb16-300e_coco.py'

load_from = 'https://download.openmmlab.com/mmyolo/v0/yolov5/yolov5_n-p6-v62_syncbn_fast_8xb16-300e_coco/yolov5_n-p6-v62_syncbn_fast_8xb16-300e_coco_20221027_224705-d493c5f3.pth'

deepen_factor = 0.33
widen_factor = 0.25

model = dict(
    backbone=dict(
        deepen_factor=deepen_factor,
        widen_factor=widen_factor,
    ),
    neck=dict(
        deepen_factor=deepen_factor,
        widen_factor=widen_factor,
    ),
    bbox_head=dict(head_module=dict(widen_factor=widen_factor)))
