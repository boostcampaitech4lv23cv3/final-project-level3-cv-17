_base_ = "./yolov5_m-p6-v62_syncbn_fast_8xb16-300e_coco.py"

load_from = "https://download.openmmlab.com/mmyolo/v0/yolov5/yolov5_l-p6-v62_syncbn_fast_8xb16-300e_coco/yolov5_l-p6-v62_syncbn_fast_8xb16-300e_coco_20221027_234308-7a2ba6bf.pth"

deepen_factor = 1.0
widen_factor = 1.0

model = dict(
    backbone=dict(
        deepen_factor=deepen_factor,
        widen_factor=widen_factor,
    ),
    neck=dict(
        deepen_factor=deepen_factor,
        widen_factor=widen_factor,
    ),
    bbox_head=dict(head_module=dict(widen_factor=widen_factor)),
)
