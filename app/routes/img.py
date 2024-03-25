from fastapi import APIRouter

from ..config import read_config
from ..db_config.db import conn
from ..db_models.img import imgs
from ..schemas.img import GCS, Img

img = APIRouter(prefix="/img")


# insert image data to mysql
@img.post("/insert")
def insert_table(p_img: Img):
    conn.execute(
        imgs.insert().values(
            id=p_img.id, input_path=p_img.input_path, output_path=p_img.output_path
        )
    )


# insert image to gcs
@img.post("/gcs")
def insert_gcs(p_gcs: GCS):
    import os

    from google.cloud import storage

    CONFIG = read_config()
    # 환경 변수 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "/opt/ml/input/gcp/storage/keys/storage-root.json"
    )

    bucket_name = CONFIG["google"]["bucket"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    # p_gcs.name : 업로드 할 파일을 GCS에 저장할 때의 이름
    blob = bucket.blob(p_gcs.name)

    # p_gcs.path : GCS에 업로드 파일의 절대경로
    with open(p_gcs.path, "rb") as file:
        blob.upload_from_file(file)


# select table
@img.get("/select")
def select_table():
    return conn.execute(imgs.select()).fetchall()
