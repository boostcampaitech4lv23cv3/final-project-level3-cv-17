from collections import Counter
from pathlib import Path

from PIL import Image
from rich.console import Console

INPUT_DIR = Path("/opt/ml/input")
AIHUB_DIR = INPUT_DIR / "aihub"
CAR_DIR = INPUT_DIR / "car"
ANN_DIR = CAR_DIR / "annotations"
IMG_DIR = CAR_DIR / "images"


if __name__ == "__main__":
    console = Console()
    sizes = []
    for _path in IMG_DIR.glob("*.jpg"):
        img = Image.open(_path)
        sizes.append((img.width, img.height))

    console.print(Counter(sizes))
    # Counter({(1920, 1080): 13313})
