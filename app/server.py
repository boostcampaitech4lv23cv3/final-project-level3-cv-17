import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, FilePath
from rich.logging import RichHandler

from .config import read_config

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")

app = FastAPI()


class ModelInfo(BaseModel):
    name: str
    config: FilePath
    pth: FilePath


def _get_models() -> List[ModelInfo]:
    config = read_config()
    return [ModelInfo(**m) for m in config['model']]


@app.get("/config")
def get_config() -> dict:
    log.info("GET /config")
    return read_config()


@app.get('/models')
def get_models() -> List[ModelInfo]:
    log.info("GET /models")
    return _get_models()


@app.get('/model')
def get_model_by_name(model_name: str) -> ModelInfo:
    log.info(f"GET /model (model_name={model_name!r})")
    for model in _get_models():
        if model.name == model_name:
            return model
    raise HTTPException(status_code=404, detail="모델을 찾을 수 없습니다")


def _get_filepaths(key: str) -> List[FilePath]:
    config = read_config()
    directory = Path(config[key]['directory'])
    formats = config[key]["format"]
    return [
        _path for format in formats for _path in directory.glob(f"**/*{format}")
    ]


@app.get('/images')
def get_images() -> List[FilePath]:
    log.info("GET /images")
    return _get_filepaths('image')


@app.get('/videos')
def get_videos() -> List[FilePath]:
    log.info("GET /images")
    return _get_filepaths('video')


def _is_image_file(filepath: FilePath) -> bool:
    config = read_config()
    return filepath.suffix in config['image']['format']


def _is_video_file(filepath: FilePath) -> bool:
    config = read_config()
    return filepath.suffix in config['video']['format']


def _identify_media(filepath: FilePath) -> str:
    if _is_image_file(filepath):
        return 'image'
    elif _is_video_file(filepath):
        return 'video'
    else:
        raise HTTPException(status_code=500, detail='미디어의 형식을 인식할 수 없습니다')


def _inference_image(model_info: ModelInfo, image_filepath: FilePath) -> FilePath:
    # TODO
    return image_filepath


def _inference_video(model_info: ModelInfo, video_filepath: FilePath) -> FilePath:
    # TODO
    return video_filepath


class InferenceBody(BaseModel):
    model_name: str
    media_filepath: FilePath


@app.post('/inference')
async def inference(body: InferenceBody) -> FilePath:
    log.info("POST /inference")
    log.info(f"  - model_name={body.model_name!r}")
    log.info(f"  - media_filepath={body.media_filepath!r}")

    model = get_model_by_name(body.model_name)
    media_type = _identify_media(body.media_filepath)
    if media_type == 'image':
        return _inference_image(model, body.media_filepath)

    return _inference_video(model, body.media_filepath)


if __name__ == '__main__':
    config = read_config()

    import uvicorn

    uvicorn.run(
        app, host=config['server']['host'], port=config['server']['port'], reload=True
    )
