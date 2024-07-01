import json

def load_card(name: str) -> dict:
    noSpaceName = name.replace(" ", "")
    data = {}
    try: 
        f = open(f'cardData/{noSpaceName}.json')
        data = json.load(f)
        f.close()
    except:
        return None
    return data

def save_card(name : str, data: dict) -> None:
    if data is None:
        return
    
    noSpaceName = name.replace(" ", "")
    
    with open(f"cardData/{noSpaceName}.json", "w") as outfile: 
        json.dump(data, outfile, indent=4)