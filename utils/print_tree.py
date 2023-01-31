"""Display a tree of files and directories

Reference:
    https://github.com/textualize/rich/blob/master/examples/tree.py

Example:
    $ python print_tree.py /opt/ml/input/aihub
"""

import os
import pathlib
import sys

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


def walk_directory(directory: pathlib.Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    max_file_count = 6
    count = 0
    for path in paths:
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            label = f"[bold magenta]:open_file_folder: [link file://{path}]" + escape(
                path.name
            )
            branch = tree.add(
                label,
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            count += 1
            if count > max_file_count:
                break

            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")

            icon = "📄 "  # 🗒️📝📄📃🧾
            if path.suffix == ".py":
                icon = "🐍 "
            elif path.suffix in [".jpg", ".png"]:
                icon = "🖼️ "  # 🎨
            elif path.suffix in [".json", ".txt"]:
                icon = "📝 "
            elif path.suffix in [".mp4", ".mkv"]:
                icon = "🎞️ "
            tree.add(Text(icon) + text_filename)


try:
    directory = os.path.abspath(sys.argv[1])
except IndexError:
    print("[b]Usage:[/] python tree.py <DIRECTORY>")
else:
    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        guide_style="bold bright_blue",
    )
    walk_directory(pathlib.Path(directory), tree)
    print(tree)
