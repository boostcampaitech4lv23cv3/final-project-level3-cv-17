"""COCO 포맷으로 변경된 AIHub 라벨 데이터를 MMYOLO에 맞게 폴더 구조 변경

Input File Structure:
    📂 /opt/ml/input/aihub
    ┣━━ 📂 1.Training
    ┃   ┣━━ 📂 라벨링데이터_1007_add
    ┃   ┃   ┣━━ 📂 M12_고가사다리소방차
    ┃   ┃   ┃   ┣━━ 📝 P_211115_P_03_M12_01_01_S_0001.json (2.2 kB)
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┣━━ 📂 M14_구급차
    ┃   ┃   ┗━━ 📂 M32_소방차
    ┃   ┗━━ 📂 원천데이터_0906_add
    ┃       ┣━━ 📂 M12_고가사다리소방차
    ┃       ┃   ┣━━ 🖼️ P_211115_P_03_M12_01_01_S_0001.jpg (1.2 MB)
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ 📂 M14_구급차
    ┃       ┗━━ 📂 M32_소방차
    ┣━━ 📂 2.Validation
    ┃   ┣━━ 📂 라벨링데이터_1007_add
    ┃   ┃   ┣━━ 📂 M12_고가사다리소방차
    ┃   ┃   ┃   ┣━━ 📝 P_211115_P_03_M12_01_01_S_0006.json (2.2 kB)
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┣━━ 📂 M14_구급차
    ┃   ┃   ┗━━ 📂 M32_소방차
    ┃   ┗━━ 📂 원천데이터_0906_add
    ┃       ┣━━ 📂 M12_고가사다리소방차
    ┃       ┃   ┣━━ 🖼️ P_211115_P_03_M12_01_01_S_0006.jpg (1.2 MB)
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ 📂 M14_구급차
    ┃       ┗━━ 📂 M32_소방차
    ┣━━ 📝 1.Training.json (5.0 MB)
    ┣━━ 📝 1.Training_pretty.json (8.7 MB)
    ┣━━ 📝 2.Validation.json (503.9 kB)
    ┣━━ 📝 2.Validation_pretty.json (867.9 kB)
    ┣━━ 📝 total.json (10.1 MB)
    ┗━━ 📝 total_pretty.json (17.4 MB)

Output File Structure:
    📂 /opt/ml/input/car
    ┣━━ 📁 annotations
    ┃   ┣━━ 📝 1.Training.json (5.0 MB)
    ┃   ┣━━ 📝 1.Training_pretty.json (8.7 MB)
    ┃   ┣━━ 📝 2.Validation.json (503.9 kB)
    ┃   ┣━━ 📝 2.Validation_pretty.json (867.9 kB)
    ┃   ┣━━ 📝 total.json (10.1 MB)
    ┃   ┗━━ 📝 total_pretty.json (17.4 MB)
    ┗━━ 📁 images
        ┣━━ 🖼️ P_211115_P_03_M12_01_01_S_0001.jpg (1.2 MB)
        ┣━━ 🖼️ P_211115_P_04_M14_01_01_S_0001.jpg (1.4 MB)
        ┣━━ 🖼️ P_211025_L_07_M32_01_01_D_0001.jpg (1.1 MB)
        ┣━━ 🖼️ P_211115_P_03_M12_01_01_S_0006.jpg (1.2 MB)
        ┣━━ 🖼️ P_211115_P_04_M14_01_01_S_0005.jpg (1.4 MB)
        ┣━━ 🖼️ P_211025_L_07_M32_01_01_D_0002.jpg (1.1 MB)
        ┗━━ ...

References:
    - https://mmyolo.readthedocs.io/en/latest/user_guides/custom_dataset.html
        #create-a-new-config-file-based-on-the-dataset
    - https://cocodataset.org/#format-data

"""

import imghdr  # Deprecated since version 3.11, will be removed in version 3.13
import json
import os
import shutil
from pathlib import Path

from rich.console import Console

INPUT_DIR = Path("/opt/ml/input")
AIHUB_DIR = INPUT_DIR / "aihub"
CAR_DIR = INPUT_DIR / "car"
ANN_DIR = CAR_DIR / "annotations"
IMG_DIR = CAR_DIR / "images"

console = Console()


def is_image_file(filepath: Path) -> bool:
    # from PIL import Image
    # try:
    #     Image.open(filepath)
    # except Exception:
    #     return False
    # return True
    return imghdr.what(filepath) is not None


def is_coco_file(filepath: Path) -> bool:
    try:
        assert filepath.suffix == ".json"

        dic = json.load(open(filepath, encoding="utf8"))

        coco_top_keys = ["info", "images", "annotations", "categories"]
        assert all(k in coco_top_keys for k in dic.keys())

        # coco_anno_keys = ['id', 'image_id', 'category_id', 'area', 'bbox', 'iscrowd']
        # for anno in dic['annotations']:
        #     assert all(k in coco_anno_keys for k in anno.keys())

        # coco_image_keys = ['id', 'width', 'height', 'file_name', 'date_captured']
        # for image in dic['images']:
        #     assert all(k in coco_image_keys for k in image.keys())

        # coco_category_keys = ['id', 'name', 'supercategory']
        # for cat in dic['categories']:
        #     assert all(k in coco_category_keys for k in cat.keys())

    except Exception:
        return False
    else:
        return True


def get_relative(path_str: str, base_dir: Path = INPUT_DIR) -> str:
    return str(Path(path_str).relative_to(base_dir))


if __name__ == "__main__":
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    ANN_DIR.mkdir(parents=True, exist_ok=True)

    with console.status("[bold green]Working on tasks...") as status:
        for root, dirs, files in os.walk(AIHUB_DIR):
            for file in files:
                filepath = Path(root) / file

                if is_image_file(filepath):
                    shutil.copy(filepath, IMG_DIR / file)

                elif is_coco_file(filepath):
                    shutil.copy(filepath, ANN_DIR / file)

            console.log(f"{len(files)} files in {root!r}")
