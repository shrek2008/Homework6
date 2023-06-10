import sys
from pathlib import Path
import uuid
import shutil

from normalize import normalize


CATEGORIES = {
    "Audio": [".mp3", ".ogg", ".wav", ".amr"],
    "Archives": [".zip", ".gz", ".tar"],
    "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
    "Images": [".jpeg", ".png", ".jpg", ".svg"],
    "Videos": [".avi", ".mp4", ".mov", ".mkv"],
}


def move_file(file: Path, root_dir: Path, category: str) -> None:
    target_dir = root_dir.joinpath(category)
    target_dir.mkdir(exist_ok=True)  # Create target directory if it doesn't exist
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    shutil.move(file, new_name)


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def delete_empty_folders(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def unpack_archive(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file() and item.suffix.lower() in [".zip", ".gz", ".tar"]:
            target_dir = item.with_suffix("")  # Remove the archive extension from the target directory name
            target_dir.mkdir(exist_ok=True)  # Create target directory if it doesn't exist
            shutil.unpack_archive(str(item), str(target_dir))
            item.unlink()  # Remove the archive file after unpacking


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} doesn't exist."

    sort_folder(path)
    delete_empty_folders(path)
    unpack_archive(path)

    return "All ok"


if __name__ == "__main__":
    print(main())
