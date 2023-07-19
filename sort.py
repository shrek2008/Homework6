import sys
from pathlib import Path
import uuid
import shutil

from normalize import normalize

CATEGORIES = {"Audio": [".mp3", ".ogg", ".wav", ".amr"],
              "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", ".mp4", ".mov", ".mkv"],
              "Archives": [".zip", ".gz", ".tar"]}

def move_file(file: Path, root_dir: Path, category: str) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()
    new_name = file.replace(target_dir.joinpath(normalize(file.stem), file.suffix))
    if new_name.exists():
        new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)

def unpack_archives(path: Path):
    for item in path.glob("**/*"):
        if item.suffix.lower() in CATEGORIES["Archives"]:
            archive_name = item.stem
            extraction_dir = path.joinpath("archives", normalize(archive_name))
            if not extraction_dir.exists():
                print(f"Make {extraction_dir}")
                extraction_dir.mkdir()
            shutil.unpack_archive(item, extraction_dir)

def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def delete_empty_folders(path: Path):
    for folder in path.glob("**/"):
        if folder.is_dir() and not any(folder.iterdir()):
            print(f"Removing empty folder: {folder}")
            folder.rmdir()

def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} does not exist"

    sort_folder(path)
    delete_empty_folders(path)
    unpack_archives(path)
    return "All ok"

if __name__ == "__main__":
    print(main())
