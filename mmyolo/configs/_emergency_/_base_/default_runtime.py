default_scope = "mmyolo"

# dataset version 3
# num_classes = 4
# metainfo = dict(
#     classes=("ambulance", "fire truck", "ladder truck", "police car")
# )

# dataset version 4
# num_classes = 3
# metainfo = dict(
#     classes=("ambulance", "fire truck", "police car")
# )

# data directory and annotation file paths
data_root = "/opt/ml/input/"
train_ann_file = "labels/*.json"
val_ann_file = "labels/*.json"

default_hooks = dict(
    timer=dict(type="IterTimerHook"),
    logger=dict(type="LoggerHook", interval=50),
    param_scheduler=dict(type="ParamSchedulerHook"),
    checkpoint=dict(type="CheckpointHook", interval=1),
    sampler_seed=dict(type="DistSamplerSeedHook"),
    visualization=dict(type="mmdet.DetVisualizationHook"),
)

env_cfg = dict(
    cudnn_benchmark=False,
    mp_cfg=dict(mp_start_method="fork", opencv_num_threads=0),
    dist_cfg=dict(backend="nccl"),
)

vis_backends = [
    dict(type="LocalVisBackend"),
    dict(
        type="WandbVisBackend",
        init_kwargs={
            "entity": "boostcamp-ai-tech-4-cv-17",
            "project": "Final Project",
            "name": "model_name",
        },
    ),
]
visualizer = dict(
    type="mmdet.DetLocalVisualizer", vis_backends=vis_backends, name="visualizer"
)
log_processor = dict(type="LogProcessor", window_size=50, by_epoch=True)

log_level = "INFO"
load_from = None
resume = False

# file_client_args = dict(
#         backend='petrel',
#         path_mapping=dict({
#             './data/': 's3://openmmlab/datasets/detection/',
#             'data/': 's3://openmmlab/datasets/detection/'
#         }))
file_client_args = dict(backend="disk")
