# python -m app.server 
import logging
from datetime import datetime
from pathlib import Path
from typing import List

import cv2
import mmcv
from fastapi import FastAPI, HTTPException
from mmcv.transforms import Compose
from mmdet.apis import inference_detector, init_detector
from mmengine.utils import track_iter_progress
from pydantic import BaseModel, FilePath
from rich.logging import RichHandler

from mmyolo.registry import VISUALIZERS
from mmyolo.utils import register_all_modules
from mmyolo.utils.misc import get_file_list

from .config import read_config

from .routes.user import user

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")

app = FastAPI()
app.include_router(user)            # user route 설정


class ModelInfo(BaseModel):
    name: str
    config: FilePath
    pth: FilePath


def _get_models() -> List[ModelInfo]:
    config = read_config()
    return [ModelInfo(**m) for m in config["model"]]

@app.get("/")
def get_index():
    return {'sixsenth backend server'}
    


@app.get("/config")
def get_config() -> dict:
    log.info("GET /config")
    return read_config()


@app.get("/models")
def get_models() -> List[ModelInfo]:
    log.info("GET /models")
    return _get_models()


@app.get("/model")
def get_model_by_name(model_name: str) -> ModelInfo:
    log.info(f"GET /model (model_name={model_name!r})")
    for model in _get_models():
        if model.name == model_name:
            return model
    raise HTTPException(status_code=404, detail="모델을 찾을 수 없습니다")


def _get_filepaths(key: str) -> List[FilePath]:
    config = read_config()
    directory = Path(config[key]["directory"])
    formats = config[key]["format"]
    return [_path for format in formats for _path in directory.glob(f"**/*{format}")]


@app.get("/images")
def get_images() -> List[FilePath]:
    log.info("GET /images")
    return _get_filepaths("image")


@app.get("/videos")
def get_videos() -> List[FilePath]:
    log.info("GET /images")
    return _get_filepaths("video")


def _is_image_file(filepath: FilePath) -> bool:
    config = read_config()
    return filepath.suffix in config["image"]["format"]


def _is_video_file(filepath: FilePath) -> bool:
    config = read_config()
    return filepath.suffix in config["video"]["format"]


def _identify_media(filepath: FilePath) -> str:
    if _is_image_file(filepath):
        return "image"
    elif _is_video_file(filepath):
        return "video"
    else:
        raise HTTPException(status_code=500, detail="미디어의 형식을 인식할 수 없습니다")


def _get_visualizer_name(filepath: FilePath) -> str:
    datetime_str = datetime.now().strftime("%Y-%m-%d %H;%M;%S")
    return f"{filepath.name} {datetime_str}"


def _inference_image(model_info: ModelInfo, image_filepath: FilePath) -> FilePath:
    register_all_modules()
    model = init_detector(model_info.config, str(model_info.pth), device="cuda:0")
    model.cfg.visualizer["name"] = _get_visualizer_name(image_filepath)
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta
    files, source_type = get_file_list(str(image_filepath))
    file = files[0]
    result = inference_detector(model, file)
    img = mmcv.imread(file)
    img = mmcv.imconvert(img, "bgr", "rgb")
    out_filepath = image_filepath.parent / (f"inferenced_{image_filepath.name}")
    visualizer.add_datasample(
        file,
        img,
        data_sample=result,
        draw_gt=False,
        wait_time=0,
        out_file=out_filepath,
        pred_score_thr=0.3,
    )
    return out_filepath


def _inference_video(model_info: ModelInfo, video_filepath: FilePath) -> FilePath:
    register_all_modules()
    model = init_detector(model_info.config, str(model_info.pth), device="cuda:0")
    model.cfg.visualizer["name"] = _get_visualizer_name(video_filepath)
    model.cfg.test_dataloader.dataset.pipeline[0].type = "mmdet.LoadImageFromNDArray"
    test_pipeline = Compose(model.cfg.test_dataloader.dataset.pipeline)
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta
    video_reader = mmcv.VideoReader(str(video_filepath))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_filepath = video_filepath.parent / (f"inferenced_{video_filepath.name}")
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
    return out_filepath


class InferenceBody(BaseModel):
    model_name: str
    media_filepath: FilePath


@app.post("/inference")
async def inference(body: InferenceBody) -> FilePath:
    log.info("POST /inference")
    log.info(f"  - model_name={body.model_name!r}")
    log.info(f"  - media_filepath={body.media_filepath!r}")

    model = get_model_by_name(body.model_name)
    media_type = _identify_media(body.media_filepath)
    if media_type == "image":
        return _inference_image(model, body.media_filepath)

    return _inference_video(model, body.media_filepath)


if __name__ == "__main__":
    config = read_config()

    import uvicorn

    uvicorn.run(
        "app.server:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
        reload=True,
    )
