"""AIHub 라벨 데이터를 COCO 포맷으로 변경

Before File Structure:
    📂 /opt/ml/input/aihub
    ┣━━ 📂 1.Training
    ┃   ┣━━ 📂 라벨링데이터_1007_add
    ┃   ┃   ┣━━ 📂 M12_고가사다리소방차
    ┃   ┃   ┃   ┣━━ 📝 P_211115_P_03_M12_01_01_S_0001.json (2.2 kB)
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┣━━ 📂 M14_구급차
    ┃   ┃   ┃   ┣━━ 📝 P_211115_P_04_M14_01_01_S_0001.json (3.3 kB)
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┗━━ 📂 M32_소방차
    ┃   ┃       ┣━━ 📝 P_211025_L_07_M32_01_01_D_0001.json (2.1 kB)
    ┃   ┃       ┗━━ ...
    ┃   ┗━━ 📂 원천데이터_0906_add
    ┃       ┣━━ 📂 M12_고가사다리소방차
    ┃       ┃   ┣━━ 🖼️ P_211115_P_03_M12_01_01_S_0001.jpg (1.2 MB)
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ 📂 M14_구급차
    ┃       ┃   ┣━━ 🖼️ P_211115_P_04_M14_01_01_S_0001.jpg (1.4 MB)
    ┃       ┃   ┗━━ ...
    ┃       ┗━━ 📂 M32_소방차
    ┃           ┣━━ 🖼️ P_211025_L_07_M32_01_01_D_0001.jpg (1.1 MB)
    ┃           ┗━━ ...
    ┗━━ 📂 2.Validation
        ┣━━ 📂 라벨링데이터_1007_add
        ┃   ┣━━ 📂 M12_고가사다리소방차
        ┃   ┃   ┣━━ 📝 P_211115_P_03_M12_01_01_S_0006.json (2.2 kB)
        ┃   ┃   ┗━━ ...
        ┃   ┣━━ 📂 M14_구급차
        ┃   ┃   ┣━━ 📝 P_211115_P_04_M14_01_01_S_0005.json (2.1 kB)
        ┃   ┃   ┗━━ ...
        ┃   ┗━━ 📂 M32_소방차
        ┃       ┣━━ 📝 P_211025_L_07_M32_01_01_D_0002.json (3.5 kB)
        ┃       ┗━━ ...
        ┗━━ 📂 원천데이터_0906_add
            ┣━━ 📂 M12_고가사다리소방차
            ┃   ┣━━ 🖼️ P_211115_P_03_M12_01_01_S_0006.jpg (1.2 MB)
            ┃   ┗━━ ...
            ┣━━ 📂 M14_구급차
            ┃   ┣━━ 🖼️ P_211115_P_04_M14_01_01_S_0005.jpg (1.4 MB)
            ┃   ┗━━ ...
            ┗━━ 📂 M32_소방차
                ┣━━ 🖼️ P_211025_L_07_M32_01_01_D_0002.jpg (1.1 MB)
                ┗━━ ...

After File Structure:
    📂 /opt/ml/input/aihub
    ┣━━ 📁 1.Training
    ┣━━ 📁 2.Validation
    ┣━━ 📝 1.Training.json (5.0 MB)
    ┣━━ 📝 1.Training_pretty.json (8.7 MB)
    ┣━━ 📝 2.Validation.json (503.9 kB)
    ┣━━ 📝 2.Validation_pretty.json (867.9 kB)
    ┣━━ 📝 total.json (10.1 MB)
    ┗━━ 📝 total_pretty.json (17.4 MB)
"""
import copy
import json
from pathlib import Path

from PIL import Image

AIHUB_DIR = Path("/opt/ml/input/aihub")
CATEGORIES = {"M14_구급차": 1, "M32_소방차": 2, "M12_고가사다리소방차": 3}
DATA = {
    "info": {
        "description": "주행 차량 관점의 특수 차량 형상 데이터",
        "contributor": "AIHub",
        "url": "https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=553",
        "version": "1.2",
        "year": 2022,
        "date_created": "2022/10/07",
    },
    "images": [],
    "categories": [
        {"id": 1, "name": "ambulance", "supercategory": "vehicle"},
        {"id": 2, "name": "fire truck", "supercategory": "vehicle"},
        {"id": 3, "name": "ladder truck", "supercategory": "vehicle"},
    ],
    "annotations": [],
}


def get_bbox_area(_data):
    objects = _data["learningDataInfo"]["objects"]
    obj = next(obj for obj in objects if obj["annotation"] == "bbox")

    top_left = obj["coords"]["tl"]
    bottom_right = obj["coords"]["br"]

    x1 = top_left["x"]
    y1 = top_left["y"]
    x2 = bottom_right["x"]
    y2 = bottom_right["y"]

    xmin = min(x1, x2)
    ymin = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)

    area = (x2 - x1) * (y2 - y1)
    bbox = [xmin, ymin, width, height]

    return bbox, area


if __name__ == "__main__":
    image_id, ann_id = 1, 1

    total_data = copy.deepcopy(DATA)

    for step_dir in AIHUB_DIR.iterdir():
        if step_dir.is_file():
            continue

        label_dir = step_dir / "라벨링데이터_1007_add"
        image_dir = step_dir / "원천데이터_0906_add"

        step_data = copy.deepcopy(DATA)

        for category_dir in label_dir.iterdir():
            category_id = CATEGORIES[category_dir.name]

            for json_path in category_dir.iterdir():
                _data = json.load(open(json_path, encoding="utf8"))

                _datetime = (
                    f"{_data['rawDataInfo']['date']} "
                    + _data["rawDataInfo"]["StartTime"]
                )

                _stem = _data["sourceDataInfo"]["sourceDataID"]  # == json_path.stem
                _suffix = _data["sourceDataInfo"]["fileExtension"]

                image_path = image_dir / category_dir.name / f"{_stem}.{_suffix}"
                img = Image.open(image_path)

                # image_name = str(image_path.relative_to(AIHUB_DIR))
                image_name = f"{_stem}.{_suffix}"
                image = {
                    "file_name": image_name,
                    "height": img.height,
                    "width": img.width,
                    "date_captured": _datetime,
                    "id": image_id,
                }

                _bbox, _area = get_bbox_area(_data)
                ann = {
                    "id": ann_id,
                    "image_id": image_id,
                    "category_id": category_id,
                    "area": _area,
                    "bbox": _bbox,
                    "iscrowd": 0,
                }

                image_id += 1
                ann_id += 1

                step_data["images"].append(image)
                step_data["annotations"].append(ann)

        json.dump(
            step_data,
            open(AIHUB_DIR / f"{step_dir.name}.json", "w", encoding="utf8"),
            ensure_ascii=False,
        )
        json.dump(
            step_data,
            open(AIHUB_DIR / f"{step_dir.name}_pretty.json", "w", encoding="utf8"),
            indent=4,
            ensure_ascii=False,
        )

        total_data["images"].extend(step_data["images"])
        total_data["annotations"].extend(step_data["annotations"])

    json.dump(
        total_data,
        open(AIHUB_DIR / "total.json", "w", encoding="utf8"),
        ensure_ascii=False,
    )
    json.dump(
        total_data,
        open(AIHUB_DIR / "total_pretty.json", "w", encoding="utf8"),
        indent=4,
        ensure_ascii=False,
    )
