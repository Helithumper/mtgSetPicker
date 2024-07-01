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


def load_set(name: str, code: str) -> dict:
    clean_name = __cleanFileName(name)
    clean_code = __cleanFileName(code)
    data = {}
    try:
        dir = f"packData/{clean_name}"
        f = open(f"{dir}/{clean_code}.json", "w")
        data = json.load(f)
        f.close()
    except:
        return None
    return data


def save_set(name: str, code: str, data: dict) -> None:
    if data is None:
        return

    clean_name = __cleanFileName(name)
    clean_code = __cleanFileName(code)

    dir = f"packData/{clean_name}"
    os.makedirs(dir, exist_ok=True)
    with open(f"{dir}/{clean_code}.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
