import datetime as dt
import io
import logging
from uuid import uuid4

import httpx
import streamlit as st
from config import read_config
from PIL import Image

log = logging.getLogger(__file__)

st.set_page_config(layout="wide")

CONFIG = read_config()
BASE_URL = f"http://localhost:{CONFIG['server']['port']}"


def make_database_dir():
    import os

    _input_path = CONFIG["image_input_path"]["path"]
    _output_path = CONFIG["image_output_path"]["path"]

    def _mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    _mkdir(_input_path)
    _mkdir(_output_path)


def get_models() -> dict:
    if st.session_state["models"] is None:
        log.info("get_models()")
        r = httpx.get(BASE_URL + "/models")
        models = r.json()
        st.session_state["models"] = models
    else:
        # log.info("get_models22()")
        models = st.session_state["models"]
    return [model["name"] for model in models]


def session_init():
    print("session init")
    if "inferenced" not in st.session_state:
        st.session_state["inferenced"] = None
    if "models" not in st.session_state:
        st.session_state["models"] = None
    if "upload_file" not in st.session_state:
        st.session_state["upload_file"] = None
    if "name" not in st.session_state:
        st.session_state["name"] = None
    if "image_input_path" not in st.session_state:
        st.session_state["image_input_path"] = None


def inference(model_name: str, media_filepath: str) -> str:
    log.info(f"inference(model_name={model_name!r}, media_filepath={media_filepath!r})")

    # 현재 페이지 상단에 spinner가 뜬다.
    with st.spinner("Predicting results. Please wait a moment!"):
        r = httpx.post(
            BASE_URL + "/inference",
            json={"model_name": model_name, "media_filepath": media_filepath},
            timeout=None,
        )  # timeout 설정

    log.info(f"inference: r.json() = {r.json()!r}")
    if r.status_code == 200:
        output_filepath = r.json()
        log.info(f"inference: output_filepath = {output_filepath!r}")
        st.session_state["inferenced"] = output_filepath


def mysql_image_insert(id: str, input_path: str, output_path: str):
    r = httpx.post(
        BASE_URL + "/img/insert",
        json={"id": id, "input_path": input_path, "output_path": output_path},
        timeout=None,
    )
    if r.status_code == 200:
        log.info("mysql data save success")
    else:
        log.error("mysql data save fail")


def insert_gcs(path: str, name: str, flag: str):
    r = httpx.post(
        BASE_URL + "/img/gcs", json={"path": path, "name": name}, timeout=None
    )
    if r.status_code == 200:
        log.info(f"gcs {flag} image save success")
    else:
        log.info(f"gcs {flag} image save success")


def main():
    st.title("Sixth Sense Image Demo Page")

    # session 초기화
    session_init()
    make_database_dir()

    models = get_models()
    model_name = st.selectbox("Model List", models)

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    col1, col2 = st.columns(2)

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        with col1:
            st.image(image, caption="Uploaded Image")

            if st.session_state["upload_file"] is None:
                # input 이미지 서버에 저장
                name = (
                    dt.datetime.today().strftime("%Y%m%d") + "_" + str(uuid4())
                )  # 날짜_uuid4
                image_input_path = f'{CONFIG["image_input_path"]["path"]}/{name}.jpg'
                image.save(image_input_path, "JPEG")

                st.button(
                    "Inference",
                    on_click=inference,
                    kwargs={
                        "model_name": model_name,
                        "media_filepath": image_input_path,
                    },
                )

                # input 이미지 gcs에 저장
                insert_gcs(image_input_path, f"{name}.jpg", "input")

                st.session_state["upload_file"] = True
                st.session_state["name"] = name
                st.session_state["image_input_path"] = image_input_path

        with col2:
            if st.session_state["inferenced"] is not None:
                st.image(st.session_state["inferenced"], caption="Infenece Image")
                # output 이미지 gcs에 저장
                insert_gcs(
                    st.session_state["inferenced"],
                    f'inferenced_{st.session_state["name"]}.jpg',
                    "output",
                )
                # mysql 이미지 data 저장
                mysql_image_insert(
                    st.session_state["name"],
                    f'{CONFIG["google"]["path"]}{CONFIG["google"]["bucket"]}/{st.session_state["name"]}.jpg',
                    f'{CONFIG["google"]["path"]}{CONFIG["google"]["bucket"]}/inferenced_{st.session_state["name"]}.jpg',
                )

    else:
        del st.session_state["upload_file"]
        del st.session_state["inferenced"]
        del st.session_state["name"]
        del st.session_state["image_input_path"]


if __name__ == "__main__":
    main()
