import json
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


def load_card(name: str) -> dict:
    clean_name = __cleanFileName(name)
    data = {}
    try:
        data = None
        with open(f"cardData/{clean_name}.json", "r") as f:
            data = json.load(f)
    except:
        return None
    return data


def save_card(name: str, data: dict) -> None:
    if data is None:
        return

    clean_name = __cleanFileName(name)

    with open(f"cardData/{clean_name}.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
