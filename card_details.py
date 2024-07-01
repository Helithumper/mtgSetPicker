import json
import unicodedata
import re


def split_rarities(data: dict) -> dict:
    m = []
    r = []
    u = []
    c = []

    for card in data:
        rarity = card["rarity"]
        match rarity:
            case "mythic":
                m.append(card)
            case "rare":
                r.append(card)
            case "uncommon":
                u.append(card)
            case "common":
                c.append(card)
            case _:
                print("CARD MISSING RARITY")

    return {
        "m": m,
        "r": r,
        "u": u,
        "c": c,
    }


# Based on Django's slugify
def __cleanFileName(name: str) -> str:
    name = str(name)
    value = (
        unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def save_rarities(set_code: str, rarity_data: dict) -> None:
    if not rarity_data:
        return

    clean_code = __cleanFileName(set_code)

    for rarity, data in rarity_data.items():
        with open(f"packData/{clean_code}/{rarity}.json", "w") as outfile:
            json.dump(data, outfile, indent=4)


def load_rarities(set_code: str) -> dict:
    clean_code = __cleanFileName(set_code)

    rarities = {
        "m": None,
        "r": None,
        "u": None,
        "c": None,
    }

    for rarity in rarities:
        print("Reading", f"packData/{clean_code}/{rarity}.json")
        with open(f"packData/{clean_code}/{rarity}.json", "r") as f:
            rarities[rarity] = json.load(f)

    return rarities
