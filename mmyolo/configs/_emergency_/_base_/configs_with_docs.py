# runtime


# model: Union[nn.Module, Dict],
"""
model (:obj:`torch.nn.Module` or dict): The model to be run. It can be
a dict used for build a model.
"""
deepen_factor = 0.33
widen_factor = 0.5
num_classes = 3
strides = [8, 16, 32]
num_det_layers = 3
anchors = [
    [(10, 13), (16, 30), (33, 23)],  # P3/8
    [(30, 61), (62, 45), (59, 119)],  # P4/16
    [(116, 90), (156, 198), (373, 326)],  # P5/32
]
img_scale = (640, 640)
model = dict(
    type="YOLODetector",
    # The type of the data preprocessor, refer to
    # https://mmdetection.readthedocs.io/en/dev-3.x/api.html#module-mmdet.models.data_preprocessors.
    # It is worth noticing that using
    # `YOLOv5DetDataPreprocessor` achieves faster training speed.
    data_preprocessor=dict(
        type="mmdet.DetDataPreprocessor",
        mean=[0.0, 0.0, 0.0],
        std=[255.0, 255.0, 255.0],
        bgr_to_rgb=True,
    ),
    backbone=dict(
        type="YOLOv5CSPDarknet",
        deepen_factor=deepen_factor,
        widen_factor=widen_factor,
        norm_cfg=dict(type="BN", momentum=0.03, eps=0.001),
        act_cfg=dict(type="SiLU", inplace=True),
    ),
    neck=dict(
        type="YOLOv5PAFPN",
        deepen_factor=deepen_factor,
        widen_factor=widen_factor,
        in_channels=[256, 512, 1024],
        out_channels=[256, 512, 1024],
        num_csp_blocks=3,
        norm_cfg=dict(type="BN", momentum=0.03, eps=0.001),
        act_cfg=dict(type="SiLU", inplace=True),
    ),
    bbox_head=dict(
        type="YOLOv5Head",
        head_module=dict(
            type="YOLOv5HeadModule",
            num_classes=num_classes,
            in_channels=[256, 512, 1024],
            widen_factor=widen_factor,
            featmap_strides=strides,
            num_base_priors=3,
        ),
        prior_generator=dict(
            type="mmdet.YOLOAnchorGenerator", base_sizes=anchors, strides=strides
        ),
        # scaled based on number of detection layers
        loss_cls=dict(
            type="mmdet.CrossEntropyLoss",
            use_sigmoid=True,
            reduction="mean",
            loss_weight=0.5 * (num_classes / 80 * 3 / num_det_layers),
        ),
        loss_bbox=dict(
            type="IoULoss",
            iou_mode="ciou",
            bbox_format="xywh",
            eps=1e-7,
            reduction="mean",
            loss_weight=0.05 * (3 / num_det_layers),
            return_iou=True,
        ),
        loss_obj=dict(
            type="mmdet.CrossEntropyLoss",
            use_sigmoid=True,
            reduction="mean",
            loss_weight=1.0 * ((img_scale[0] / 640) ** 2 * 3 / num_det_layers),
        ),
        prior_match_thr=4.0,
        obj_level_weights=[4.0, 1.0, 0.4],
    ),
    test_cfg=dict(
        multi_label=True,
        nms_pre=30000,
        score_thr=0.001,
        nms=dict(type="nms", iou_threshold=0.65),
        max_per_img=300,
    ),
)


# work_dir: str
"""
work_dir (str): The working directory to save checkpoints. The logs
will be saved in the subdirectory of `work_dir` named
:attr:`timestamp`.
"""


# train_dataloader: Optional[Union[DataLoader, Dict]] = None
"""
train_dataloader (Dataloader or dict, optional): A dataloader object or
a dict to build a dataloader. If ``None`` is given, it means
skipping training steps. Defaults to None.
See :meth:`build_dataloader` for more details.
"""
train_batch_size_per_gpu = 16
train_num_workers = 8
persistent_workers = True  # persistent_workers must be False if num_workers is 0.
dataset_type = "YOLOv5CocoDataset"
data_root = "/opt/ml/input/car/"
class_name = ("ambulance", "fire truck", "ladder truck")
metainfo = dict(classes=class_name, palette=[(220, 20, 60)])
file_client_args = dict(backend="disk")
pre_transform = [
    dict(type="LoadImageFromFile", file_client_args=file_client_args),
    dict(type="LoadAnnotations", with_bbox=True),
]
albu_train_transforms = [
    dict(type="Blur", p=0.01),
    dict(type="MedianBlur", p=0.01),
    dict(type="ToGray", p=0.01),
    dict(type="CLAHE", p=0.01),
]
train_pipeline = [
    *pre_transform,
    dict(
        type="Mosaic", img_scale=img_scale, pad_val=114.0, pre_transform=pre_transform
    ),
    dict(
        type="YOLOv5RandomAffine",
        max_rotate_degree=0.0,
        max_shear_degree=0.0,
        scaling_ratio_range=(0.5, 1.5),
        # img_scale is (width, height)
        border=(-img_scale[0] // 2, -img_scale[1] // 2),
        border_val=(114, 114, 114),
    ),
    dict(
        type="mmdet.Albu",
        transforms=albu_train_transforms,
        bbox_params=dict(
            type="BboxParams",
            format="pascal_voc",
            label_fields=["gt_bboxes_labels", "gt_ignore_flags"],
        ),
        keymap={"img": "image", "gt_bboxes": "bboxes"},
    ),
    dict(type="YOLOv5HSVRandomAug"),
    dict(type="mmdet.RandomFlip", prob=0.5),
    dict(
        type="mmdet.PackDetInputs",
        meta_keys=(
            "img_id",
            "img_path",
            "ori_shape",
            "img_shape",
            "flip",
            "flip_direction",
        ),
    ),
]
train_dataloader = dict(
    batch_size=train_batch_size_per_gpu,
    num_workers=train_num_workers,
    persistent_workers=persistent_workers,
    pin_memory=True,
    sampler=dict(type="DefaultSampler", shuffle=True),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        # ann_file='annotations/instances_train2017.json',
        ann_file="annotations/1.Training_pretty.json",
        # data_prefix=dict(img='train2017/'),
        data_prefix=dict(img="images/"),
        filter_cfg=dict(filter_empty_gt=False, min_size=32),
        pipeline=train_pipeline,
    ),
)


# val_dataloader: Optional[Union[DataLoader, Dict]] = None
"""
val_dataloader (Dataloader or dict, optional): A dataloader object or
a dict to build a dataloader. If ``None`` is given, it means
skipping validation steps. Defaults to None.
See :meth:`build_dataloader` for more details.
"""
val_batch_size_per_gpu = 1
val_num_workers = 2
test_pipeline = [
    dict(type="LoadImageFromFile", file_client_args=file_client_args),
    dict(type="YOLOv5KeepRatioResize", scale=img_scale),
    dict(
        type="LetterResize",
        scale=img_scale,
        allow_scale_up=False,
        pad_val=dict(img=114),
    ),
    dict(type="LoadAnnotations", with_bbox=True, _scope_="mmdet"),
    dict(
        type="mmdet.PackDetInputs",
        meta_keys=(
            "img_id",
            "img_path",
            "ori_shape",
            "img_shape",
            "scale_factor",
            "pad_param",
        ),
    ),
]
# only on Val
batch_shapes_cfg = dict(
    type="BatchShapePolicy",
    batch_size=val_batch_size_per_gpu,
    img_size=img_scale[0],
    size_divisor=32,
    extra_pad_ratio=0.5,
)
val_dataloader = dict(
    batch_size=val_batch_size_per_gpu,
    num_workers=val_num_workers,
    persistent_workers=persistent_workers,
    pin_memory=True,
    drop_last=False,
    sampler=dict(type="DefaultSampler", shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        test_mode=True,
        # data_prefix=dict(img='val2017/'),
        data_prefix=dict(img="images/"),
        # ann_file='annotations/instances_val2017.json',
        ann_file="annotations/2.Validation_pretty.json",
        pipeline=test_pipeline,
        batch_shapes_cfg=batch_shapes_cfg,
    ),
)


# test_dataloader: Optional[Union[DataLoader, Dict]] = None
"""
test_dataloader (Dataloader or dict, optional): A dataloader object or
a dict to build a dataloader. If ``None`` is given, it means
skipping test steps. Defaults to None.
See :meth:`build_dataloader` for more details.
"""
test_dataloader = val_dataloader


# train_cfg: Optional[Dict] = None
"""
train_cfg (dict, optional): A dict to build a training loop. If it does
not provide "type" key, it should contain "by_epoch" to decide
which type of training loop :class:`EpochBasedTrainLoop` or
:class:`IterBasedTrainLoop` should be used. If ``train_cfg``
specified, :attr:`train_dataloader` should also be specified.
Defaults to None. See :meth:`build_train_loop` for more details.
"""
max_epochs = 300
save_epoch_intervals = 10
train_cfg = dict(
    type="EpochBasedTrainLoop", max_epochs=max_epochs, val_interval=save_epoch_intervals
)


# val_cfg: Optional[Dict] = None
"""
val_cfg (dict, optional): A dict to build a validation loop. If it does
not provide "type" key, :class:`ValLoop` will be used by default.
If ``val_cfg`` specified, :attr:`val_dataloader` should also be
specified. If ``ValLoop`` is built with `fp16=True``,
``runner.val()`` will be performed under fp16 precision.
Defaults to None. See :meth:`build_val_loop` for more details.
"""
val_cfg = dict(type="ValLoop")


# test_cfg: Optional[Dict] = None
"""
test_cfg (dict, optional): A dict to build a test loop. If it does
not provide "type" key, :class:`TestLoop` will be used by default.
If ``test_cfg`` specified, :attr:`test_dataloader` should also be
specified. If ``ValLoop`` is built with `fp16=True``,
``runner.val()`` will be performed under fp16 precision.
Defaults to None. See :meth:`build_test_loop` for more details.
"""
test_cfg = dict(type="TestLoop")


# auto_scale_lr: Optional[Dict] = None
"""
auto_scale_lr (dict, Optional): Config to scale the learning rate
automatically. It includes ``base_batch_size`` and ``enable``.
``base_batch_size`` is the batch size that the optimizer lr is
based on. ``enable`` is the switch to turn on and off the feature.
"""


# optim_wrapper: Optional[Union[OptimWrapper, Dict]] = None
"""
optim_wrapper (OptimWrapper or dict, optional):
Computing gradient of model parameters. If specified,
:attr:`train_dataloader` should also be specified. If automatic
mixed precision or gradient accmulation
training is required. The type of ``optim_wrapper`` should be
AmpOptimizerWrapper. See :meth:`build_optim_wrapper` for
examples. Defaults to None.
"""
# Base learning rate for optim_wrapper
base_lr = 0.01
optim_wrapper = dict(
    type="OptimWrapper",
    optimizer=dict(
        type="SGD",
        lr=base_lr,
        momentum=0.937,
        weight_decay=0.0005,
        nesterov=True,
        batch_size_per_gpu=train_batch_size_per_gpu,
    ),
    constructor="YOLOv5OptimizerConstructor",
)


# param_scheduler: Optional[Union[_ParamScheduler, Dict, List]] = None
"""
param_scheduler (_ParamScheduler or dict or list, optional):
Parameter scheduler for updating optimizer parameters. If
specified, :attr:`optimizer` should also be specified.
Defaults to None.
See :meth:`build_param_scheduler` for examples.
"""
param_scheduler = None


# val_evaluator: Optional[Union[Evaluator, Dict, List]] = None
"""
val_evaluator (Evaluator or dict or list, optional): A evaluator object
used for computing metrics for validation. It can be a dict or a
list of dict to build a evaluator. If specified,
:attr:`val_dataloader` should also be specified. Defaults to None.
"""
val_evaluator = dict(
    type="mmdet.CocoMetric",
    proposal_nums=(100, 1, 10),
    ann_file=data_root + "annotations/2.Validation_pretty.json",
    metric="bbox",
)


# test_evaluator: Optional[Union[Evaluator, Dict, List]] = None
"""
test_evaluator (Evaluator or dict or list, optional): A evaluator
object used for computing metrics for test steps. It can be a dict
or a list of dict to build a evaluator. If specified,
:attr:`test_dataloader` should also be specified. Defaults to None.
"""
test_evaluator = val_evaluator


# default_hooks: Optional[Dict[str, Union[Hook, Dict]]] = None
"""
default_hooks (dict[str, dict] or dict[str, Hook], optional): Hooks to
execute default actions like updating model parameters and saving
checkpoints. Default hooks are ``OptimizerHook``,
``IterTimerHook``, ``LoggerHook``, ``ParamSchedulerHook`` and
``CheckpointHook``. Defaults to None.
See :meth:`register_default_hooks` for more details.
"""
default_hooks = dict(
    timer=dict(type="IterTimerHook"),
    logger=dict(type="LoggerHook", interval=50),
    param_scheduler=dict(type="ParamSchedulerHook"),
    checkpoint=dict(type="CheckpointHook", interval=1),
    sampler_seed=dict(type="DistSamplerSeedHook"),
    visualization=dict(type="mmdet.DetVisualizationHook"),
)


# custom_hooks: Optional[List[Union[Hook, Dict]]] = None
"""
custom_hooks (list[dict] or list[Hook], optional): Hooks to execute
custom actions like visualizing images processed by pipeline.
Defaults to None.
"""


# data_preprocessor: Union[nn.Module, Dict, None] = None
"""
data_preprocessor (dict, optional): The pre-process config of
:class:`BaseDataPreprocessor`. If the ``model`` argument is a dict
and doesn't contain the key ``data_preprocessor``, set the argument
as the ``data_preprocessor`` of the ``model`` dict.
Defaults to None.
"""


# load_from: Optional[str] = None
"""
load_from (str, optional): The checkpoint file to load from.
Defaults to None.
"""
load_from = None


# resume: bool = False
"""
resume (bool): Whether to resume training. Defaults to False. If
``resume`` is True and ``load_from`` is None, automatically to
find latest checkpoint from ``work_dir``. If not found, resuming
does nothing.
"""
resume = False


# launcher: str = 'none'
"""
launcher (str): Way to launcher multi-process. Supported launchers
are 'pytorch', 'mpi', 'slurm' and 'none'. If 'none' is provided,
non-distributed environment will be launched.
"""


# env_cfg: Dict = dict(dist_cfg=dict(backend='nccl'))
"""
env_cfg (dict): A dict used for setting environment. Defaults to
dict(dist_cfg=dict(backend='nccl')).
"""
# single-scale training is recommended to
# be turned on, which can speed up training.
env_cfg = dict(cudnn_benchmark=True)


# log_processor: Optional[Dict] = None
"""
log_processor (dict, optional): A processor to format logs. Defaults to
None.
"""
log_processor = dict(type="LogProcessor", window_size=50, by_epoch=True)


# log_level: str = 'INFO'
"""
log_level (int or str): The log level of MMLogger handlers.
Defaults to 'INFO'.
"""
log_level = "INFO"


# visualizer: Optional[Union[Visualizer, Dict]] = None
"""
visualizer (Visualizer or dict, optional): A Visualizer object or a
dict build Visualizer object. Defaults to None. If not
specified, default config will be used.
"""
visualizer = dict(
    type="mmdet.DetLocalVisualizer",
    vis_backends=[dict(type="LocalVisBackend")],
    name="visualizer",
)


# default_scope: str = 'mmengine'
"""
default_scope (str): Used to reset registries location.
Defaults to "mmengine".
"""
default_scope = "mmyolo"


# randomness: Dict = dict(seed=None)
"""
randomness (dict): Some settings to make the experiment as reproducible
as possible like seed and deterministic.
Defaults to ``dict(seed=None)``. If seed is None, a random number
will be generated and it will be broadcasted to all other processes
if in distributed environment. If ``cudnn_benchmarch`` is
``True`` in ``env_cfg`` but ``deterministic`` is ``True`` in
``randomness``, the value of ``torch.backends.cudnn.benchmark``
will be ``False`` finally.
"""


# experiment_name: Optional[str] = None
"""
experiment_name (str, optional): Name of current experiment. If not
specified, timestamp will be used as ``experiment_name``.
Defaults to None.
"""


# cfg: Optional[ConfigType] = None
"""
cfg (dict or Configdict or :obj:`Config`, optional): Full config.
Defaults to None.
"""
