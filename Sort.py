from shutil import move
from pathlib import Path
from threading import Thread
import logging

EXT_FOLDER = {
    ("mp3", "ogg", "waw", "amr"): "audio",
    ("avi", "mp4", "mov", "mkv", "flv"): "video",
    ("jpeg", "png", "jpg", "svg"): "images",
    ("doc", "docx", "txt", "xlsx", "xls", "pptx", "csv"): "documents",
    ("djvu", "djv", "pdf", "tiff"): "books",
    ("zip", "gz", "tar", "7z", "rar"): "archives",
    ("vhdx", "iso"): "disk_images",  # для великих файлів
}

""" ============================= Функці =================================="""


# Конфігурація логування
logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


def get_file_category(file: str):
    """Функція повертає назву категорії у відповідності до імені вхідного файлу."""

    the_path = Path(file)
    ext = the_path.suffix.lstrip(".")

    for exts in EXT_FOLDER.keys():
        if ext in exts:
            return EXT_FOLDER[exts]
    return None


def create_folders(root):
    """Створює папки каталогів у root"""

    for folder in EXT_FOLDER.values():
        Path(root).joinpath(folder).mkdir(exist_ok=True)


def organize_files(path, level=0):
    """Функція фасує файли по відповідним папкам."""

    the_path = Path(path)
    if level == 0:
        global root_path
        root_path = the_path.resolve()

    threads = []

    for item in the_path.iterdir():
        if item.is_dir() and item.name not in EXT_FOLDER.values():
            organize_files(item.resolve(), level + 1)
        else:
            category = get_file_category(item.name)
            if category:
                destination_path = Path(root_path).joinpath(category, item.name)
                thread = Thread(target=move, args=(item, destination_path))
                thread.start()
                threads.append(thread)
                logging.info(f"Moving {item.name} to {destination_path}")

    # Очікуємо завершення всіх потоків
    for thread in threads:
        thread.join()

    return None


def remove_empty(path):
    """Видаляє порожні папки."""

    the_path = Path(path)
    empty = True
    for item in the_path.glob("*"):
        if item.is_file():
            empty = False
        if item.is_dir() and not remove_empty(item):
            empty = False

    if empty:
        path.rmdir()
    return empty


""" ======================== Основна програма =============================="""


def sort_folder(root):
    path = Path(root)
    if not path.is_dir():
        return f"Warning! The {root} is not a valid path!"

    agreement = input(
        f"WARNING! Are you sure you want to sort the files in CATALOG {root}? (y/n): "
    )

    if agreement not in ("y", "Y", "yes", "Yes", "YES"):
        return "Operation approved!"

    create_folders(root)
    organize_files(root)
    remove_empty(root)

    return f"Folder {root} sorted!"


if __name__ == "__main__":
    root = "d:\\Different\\Garbage\\"
    result = sort_folder(root)
    print(result)
