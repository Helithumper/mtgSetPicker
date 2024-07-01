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

class card:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class card_set:
    def __init__(self, name, set_type):
        self.name = name
        self.set_type = set_type
        self.count = 0
        self.cards = []

    def add(self, card):
        self.count += 1
        self.cards.append(card)

def get_set_counts(card_list: dict) -> dict:
    set_map = {}
    for c in card_list:
        for card_data in c['data']:
            set_id = card_data['set_id']
            if set_id not in set_map.keys():
                set_map[set_id] = card_set(
                    card_data['set_name'],
                    card_data['set_type']
                )
            set_map[set_id].add( card(
                card_data['name'],
                card_data['prices']['usd'],
            ))
    return set_map

def card_set_count(cs: card_set) -> int:
    return cs[1].count

def sort_set_counts(set_counts: dict) -> dict:
    sorted_set = {}
    for k, v in sorted(set_counts.items(), key=card_set_count, reverse=True):
        sorted_set[k] = v
    return sorted_set

def print_sorted_set(set_counts: dict, top_n: int) -> dict:
    i = 0
    for k, v in set_counts.items():
        print("k:", k)
        print("\tname:", v.name)
        print("\tset_type:", v.set_type)
        print("\tcards:")
        for c in v.cards:
            print("\t\tName:", c.name, "- Price:", c.price)
        i += 1
        if i >= top_n:
            break

cards = ["Ratcatcher", "Swarm of Rats", "Jet Medallion"]

data = process_list(cards)
set_counts = get_set_counts(data)
set_counts = sort_set_counts(set_counts)

print_sorted_set(set_counts, 5)

# sets = []
# for c in data['data']:
#     sets.append(c['set_id'])

# print(sets)