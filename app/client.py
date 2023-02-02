# streamlit run app/client.py --server.port 30002
import logging
from pathlib import Path

import httpx
import streamlit as st
from config import read_config

log = logging.getLogger(__file__)

st.set_page_config(layout="wide")

CONFIG = read_config()
BASE_URL = f"http://localhost:{CONFIG['server']['port']}"


def get_models() -> dict:
    log.info("get_models()")
    r = httpx.get(BASE_URL + "/models")
    models = r.json()
    return [model["name"] for model in models]


def get_model(model_name: str) -> dict:
    log.info(f"get_model(model_name={model_name!r})")
    r = httpx.get(BASE_URL + "/model", params={"model_name": model_name})
    return r.json()


def get_images() -> list:
    log.info("get_images()")
    r = httpx.get(BASE_URL + "/images")
    return r.json()


def get_videos() -> list:
    log.info("get_videos()")
    r = httpx.get(BASE_URL + "/videos")
    return r.json()


def get_video_names() -> list:
    log.info("get_video_names()")
    videos = get_videos()
    return [Path(video).name for video in videos]


def inference(model_name: str, media_filepath: str) -> str:
    log.info(f"inference(model_name={model_name!r}, media_filepath={media_filepath!r})")
    r = httpx.post(
        BASE_URL + "/inference",
        json={"model_name": model_name, "media_filepath": media_filepath},
    )

    log.info(f"inference: r.json() = {r.json()!r}")

    if r.status_code == 200:
        output_filepath = r.json()
        log.info(f"inference: output_filepath = {output_filepath!r}")
        st.session_state["inferenced"] = output_filepath


def get_inferenced_media(media_filepath: str) -> str:
    log.info(f"inference(media_filepath={media_filepath!r})")
    r = httpx.get(
        BASE_URL + "/inference",
        params={"filepath": media_filepath}
    )

    log.info(f"inference: r.json() = {r.json()!r}")

    if r.status_code == 200:
        output_filepath = r.json()
        log.info(f"inference: output_filepath = {output_filepath!r}")
        st.session_state["inferenced"] = output_filepath


def read_image(image_path: str) -> bytes:
    log.info(f"read_image(image_path={image_path!r})")
    with open(image_path, "rb") as f:
        return f.read()


def read_video(video_path: str) -> bytes:
    log.info(f"read_video(video_path={video_path!r})")
    with open(video_path, "rb") as f:
        return f.read()


def main():
    st.title("Sixth Sense Streamlit Demo Page")
    if "inferenced" not in st.session_state:
        st.session_state["inferenced"] = None

    models = get_models()
    images = get_images()
    videos = get_videos()
    video_names = get_video_names()

    with st.sidebar.container():
        model_name = st.selectbox("Model List", models)
        video_name = st.selectbox("Video List", video_names, key="select_video")
        video_index = next((i for i, n in enumerate(video_names) if n == video_name))
        log.info(f"video_name: {video_name!r} (type: {type(video_name)}")
        log.info(f"video_index: {video_index!r} (type: {type(video_index)}")

    with st.sidebar.container():
        video_path = videos[video_index]
        if video_path is not None:
            input_video = read_video(video_path)
            st.video(input_video)

            st.button(
                "inference",
                on_click=get_inferenced_media,
                kwargs={"media_filepath": video_path},
            )

    if st.session_state["inferenced"] is not None:
        output_video = read_video(st.session_state["inferenced"])
        st.video(output_video)


if __name__ == "__main__":
    main()
