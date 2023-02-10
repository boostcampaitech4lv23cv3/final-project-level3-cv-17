import os
from datetime import datetime
from pathlib import Path

import cv2
import mmcv
from mmcv.transforms import Compose
from mmdet.apis import inference_detector, init_detector
from mmengine.utils import track_iter_progress

from mmyolo.registry import VISUALIZERS
from mmyolo.utils import register_all_modules


def _get_visualizer_name(filepath: Path) -> str:
    datetime_str = datetime.now().strftime("%Y-%m-%d %H;%M;%S")
    return f"{filepath.name} {datetime_str}"


def _inference_video(config_path: Path, model_path: Path, video_filepath: Path) -> Path:
    register_all_modules()

    model = init_detector(config_path, str(model_path), device="cuda:0")
    model.cfg.visualizer["name"] = _get_visualizer_name(video_filepath)
    model.cfg.test_dataloader.dataset.pipeline[0].type = "mmdet.LoadImageFromNDArray"

    test_pipeline = Compose(model.cfg.test_dataloader.dataset.pipeline)

    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta

    video_reader = mmcv.VideoReader(str(video_filepath))
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    out_filepath = model_path.parent / (f"inferenced_{video_filepath.name}")

    video_writer = cv2.VideoWriter(
        str(out_filepath),
        fourcc,
        video_reader.fps,
        (video_reader.width, video_reader.height),
    )

    for frame in track_iter_progress(video_reader):
        result = inference_detector(model, frame, test_pipeline=test_pipeline)
        visualizer.add_datasample(
            name="video",
            image=frame,
            data_sample=result,
            draw_gt=False,
            show=False,
            pred_score_thr=0.3,
        )
        frame = visualizer.get_image()
        video_writer.write(frame)
    video_writer.release()

    new_filename = f"{video_filepath.stem}_inferenced{video_filepath.suffix}"
    h264_filepath = model_path.with_name(new_filename)
    os.system(f"/url/bin/ffmpeg -i {out_filepath} -vcodec libx264 {h264_filepath}")
    return h264_filepath


if __name__ == "__main__":
    PROJ_DIR = Path("/opt/ml/final-project-level3-cv-17")
    mmyolo_dir = PROJ_DIR / "mmyolo"
    work_dir = mmyolo_dir / "work_dirs"
    video_dir = Path("/opt/ml/input/videos")

    model_dir = work_dir / "yolov8_m-syncbn_fast_8xb16-500e-coco_pretrained"
    config_path = model_dir / "yolov8_m-syncbn_fast_8xb16-500e-coco_pretrained.py"
    model_path = model_dir / "epoch_500.pth"

    for video_filepath in video_dir.iterdir():
        _inference_video(config_path, model_path, video_filepath)
