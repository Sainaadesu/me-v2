import os


def load_txt_file(path):

    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл олдсонгүй: {path}")

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return text