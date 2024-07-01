import json
import unicodedata
import re

def load_card(name: str) -> dict:
    clean_name = __cleanFileName(name)
    data = {}
    try: 
        f = open(f'cardData/{clean_name}.json')
        data = json.load(f)
        f.close()
    except:
        return None
    return data

# Based on Django's slugify
def __cleanFileName(name: str) -> str:
    name = str(name)
    value = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def save_card(name : str, data: dict) -> None:
    if data is None:
        return
    
    clean_name = __cleanFileName(name)
    
    with open(f"cardData/{clean_name}.json", "w") as outfile: 
        json.dump(data, outfile, indent=4)