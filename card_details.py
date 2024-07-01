import json
import unicodedata
import re

def split_rarities(data: dict) -> dict:
    mr = []
    r = []
    uc = []
    c = []
    
    for card in data:
        rarity = card["rarity"]
        match rarity:
            case "mythic":
                mr.append(card)
            case "rare":
                r.append(card)
            case "uncommon":
                r.append(card)
            case "common":
                r.append(card)
            case _:
                print("CARD MISSING RARITY")
    
    return {
        "mr": mr,
        "r": r,
        "uc": uc,
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

def save_rarities(set_name: str, rarities: dict):
    if not rarities:
        return
    
    clean_name = __cleanFileName(set_name)
    
    for rarity, data in rarities.items():
        with open(f"packData/{clean_name}/{rarity}.json", "w") as outfile:
            json.dump(data, outfile, indent=4)