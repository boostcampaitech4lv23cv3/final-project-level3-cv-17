from pydantic import BaseModel


class Img(BaseModel):
    id: str
    input_path: str
    output_path: str
    

class GCS(BaseModel):
    path: str               
    name: str               