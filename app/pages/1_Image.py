import logging
import streamlit as st
from config import read_config
from PIL import Image
import io
import httpx
from uuid import UUID, uuid4



log = logging.getLogger(__file__)

st.set_page_config(layout="wide")

CONFIG = read_config()
BASE_URL = f"http://localhost:{CONFIG['server']['port']}"

def get_models() -> dict:
    log.info("get_models()")
    r = httpx.get(BASE_URL + "/models")
    models = r.json()
    return [model["name"] for model in models]

def session_init():
    if "inferenced" not in st.session_state:
        st.session_state["inferenced"] = None
        
def inference(model_name: str, media_filepath: str) -> str:
    log.info(f"inference(model_name={model_name!r}, media_filepath={media_filepath!r})")
    
    # 현재 페이지 상단에 spinner가 뜬다.
    with st.spinner("wait!!!"):
        r = httpx.post(
            BASE_URL + "/inference",
            json={"model_name": model_name, "media_filepath": media_filepath},
            timeout = None                          # timeout 설정
        )
            
    log.info(f"inference: r.json() = {r.json()!r}")
    if r.status_code == 200:
        output_filepath = r.json()
        log.info(f"inference: output_filepath = {output_filepath!r}")
        st.session_state["inferenced"] = output_filepath
        
def mysql_image_insert(id: str, input_path: str, output_path: str):
    
    r = httpx.post(BASE_URL+ "/img/insert",
                   json={"id": id, "input_path": input_path, "output_path": output_path},
                   timeout=None
                   )
    if r.status_code == 200:
        log.info("mysql data save success")
    else:
        log.error("mysql data save fail")
        
        
        
    
    
def main():
    st.title("This is Image Page")
    
    session_init()              # session 초기화
    text_spinner_placeholder = st.empty()
    
    
    models = get_models()
    model_name = st.selectbox("Model List", models)
    
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    col1, col2 = st.columns(2)
    
    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))
        
        
        # 이미지 서버에 저장
        name = str(uuid4())
        image_input_path = f'{CONFIG["image_input_path"]["path"]}/{name}.jpg'
        image.save(image_input_path, 'JPEG')
        
        with col1:
            st.image(image, caption='Uploaded Image')
          
            st.button("Inference",
                      on_click=inference,
                      kwargs={"model_name": model_name, "media_filepath": image_input_path},
                      )
        with col2:
            if st.session_state["inferenced"] is not None:
                st.image(st.session_state["inferenced"], caption='Infenece Image')
                mysql_image_insert(name, image_input_path, st.session_state["inferenced"])
        

if __name__ == '__main__':
    main()
