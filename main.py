import json
import requests

def search_card(name: str) -> dict:
    url = "https://api.scryfall.com/cards/search"
    params = {"q": name, "unique": "prints"}
    req = requests.models.PreparedRequest()
    req.prepare_url(url, params)
    response = requests.get(req.url)

    if response.status_code == 200:
        return response.json()    
    return None

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
        
def process_list(names: list) -> list:
    list_data = []
    for n in names:
        data = load_card(n)
        if data is None:
            data = search_card(n)
            if data is not None:
                save_card(n, data)
        if data is not None:
            list_data.append(data)
            
    return list_data

class card_set:
    def __init__(self):
        self.count = 0
        self.cards = []

    def add(self, name):
        self.count += 1
        self.cards.append(name)

def get_set_counts(card_list: dict) -> dict:
    set_map = {}
    for card in card_list:
        for card_data in card['data']:
            set_id = card_data['set_id']
            if set_id not in set_map.keys():
                set_map[set_id] = card_set()
            set_map[set_id].add(card_data['name'])
    return set_map

def card_set_count(cs: card_set) -> int:
    return cs[1].count

def sort_set_counts(set_counts: dict) -> dict:
    for k, v in sorted(set_counts.items(), key=card_set_count, reverse=True):
        print("k:", k)
        print("v:", v.cards)

cards = ["Ratcatcher", "Swarm of Rats", "Jet Medallion"]

data = process_list(cards)

set_counts = get_set_counts(data)

print(sort_set_counts(set_counts))

# sets = []
# for c in data['data']:
#     sets.append(c['set_id'])

# print(sets)