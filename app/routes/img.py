from ..db_models.img import imgs
from ..db_config.db import conn
from fastapi import APIRouter
from ..schemas.img import Img

img = APIRouter(prefix="/img")

# insert table
@img.post("/insert")
def insert_table(p_img: Img):
    conn.execute(imgs.insert().values(
        id=p_img.id,
        input_path=p_img.input_path,
        output_path=p_img.output_path
    ))
    
# select table
@img.get("/select")
def select_table():
    return conn.execute(imgs.select()).fetchall()
    
    
    