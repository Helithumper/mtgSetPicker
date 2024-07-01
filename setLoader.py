import json
import os
import unicodedata
import re


# Based on Django's slugify
def __cleanFileName(name: str) -> str:
    name = str(name)
    value = (
        unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def load_set(code: str) -> dict:
    clean_code = __cleanFileName(code)
    data = {}
    try:
        dir = f"packData/{clean_code}"
        data = None
        with open(f"{dir}/set-list.json", "r") as f:
            data = json.load(f)
    except:
        return None
    return data


def save_set(code: str, data: dict) -> None:
    if data is None:
        return

    clean_code = __cleanFileName(code)

    dir = f"packData/{clean_code}"
    os.makedirs(dir, exist_ok=True)
    with open(f"{dir}/set-list.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
