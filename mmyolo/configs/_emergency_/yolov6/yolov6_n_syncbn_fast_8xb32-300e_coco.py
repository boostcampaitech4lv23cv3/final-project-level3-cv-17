_base_ = "./yolov6_s_syncbn_fast_8xb32-300e_coco.py"

load_from = "https://download.openmmlab.com/mmyolo/v0/yolov6/yolov6_n_syncbn_fast_8xb32-400e_coco/yolov6_n_syncbn_fast_8xb32-400e_coco_20221030_202726-d99b2e82.pth"

deepen_factor = 0.33
widen_factor = 0.25

model = dict(
    backbone=dict(deepen_factor=deepen_factor, widen_factor=widen_factor),
    neck=dict(deepen_factor=deepen_factor, widen_factor=widen_factor),
    bbox_head=dict(
        head_module=dict(widen_factor=widen_factor), loss_bbox=dict(iou_mode="siou")
    ),
)

default_hooks = dict(param_scheduler=dict(lr_factor=0.02))
