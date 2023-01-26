from pathlib import Path
from typing import List

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, FilePath

from .config import read_config

app = FastAPI()


class Model(BaseModel):
    name: str
    config: FilePath
    pth: FilePath


def _get_models() -> List[Model]:
    config = read_config()
    return [Model(**m) for m in config['model']]


@app.get('/models')
def get_models() -> List[Model]:
    return _get_models()


@app.get('/model')
def get_model_by_name(model_name: str) -> Model:
    for model in _get_models():
        if model.name == model_name:
            return model
    raise HTTPException(status_code=404, detail='모델을 찾을 수 없습니다')


def _get_filepaths(key: str) -> List[FilePath]:
    config = read_config()
    directory = Path(config[key]['directory'])
    formats = ','.join(config[key]['format'])
    return [FilePath(_path) for _path in directory.glob(f'**/*{{{formats}}}')]


@app.get('/images')
def get_images() -> List[FilePath]:
    return _get_filepaths('image')


@app.get('/videos')
def get_videos() -> List[FilePath]:
    return _get_filepaths('video')


@app.get('/image')
def get_image(filepath: FilePath) -> bytes:
    image_file = open(filepath, 'rb')
    # image = Image.open(io.BytesIO(image_bytes))
    return image_file.read()


@app.get('/video')
def get_video(filepath: FilePath) -> bytes:
    video_file = open(filepath, 'rb')
    # st.video(video_bytes)
    return video_file.read()


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


def _inference_image(model: Model, image_filepath: FilePath) -> FilePath:
    # TODO
    return


def _inference_video(model: Model, video_filepath: FilePath) -> FilePath:
    # TODO
    return


@app.post('/inference')
def inference(model_name: str, media_filepath: FilePath) -> FilePath:
    model = get_model_by_name(model_name)
    media_type = _identify_media(media_filepath)
    if media_type == 'image':
        return _inference_image(model, media_filepath)

    return _inference_video(model, media_filepath)


if __name__ == '__main__':
    config = read_config()
    
    import uvicorn

    uvicorn.run(
        app, host=config['server']['host'], port=config['server']['port'], reload=True
    )
