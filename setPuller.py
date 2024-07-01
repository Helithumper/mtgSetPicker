import argparse
from lib.manipulators.card import split_rarities, save_rarities, load_rarities
from lib.apis.scryfall import set_list, set_detail
from lib.loaders.set import load_set, save_set

def get_sets(codes: list, useCache: bool) -> list:
    list_data = []
    for sc in codes:
        data = None
        if useCache:
            data = load_set(sc)
        if data is None:
            data = set_list(sc)
            detail = set_detail(sc)
            data["set_name"] = detail["name"]
            data["set_code"] = sc
            if data is not None:
                save_set(sc, data)
        if data is not None:
            list_data.append(data)
            
    return list_data

def get_rarities(set_codes: list, useCache: bool) -> list:
    rarities = []
    for set_code in set_codes:
        # See if we already have rarities for this set
        rarity_data = None
        if useCache:
            rarity_data = load_rarities(set_code)
        
        if rarity_data is None:
            set_data = get_sets([set_code], useCache)
            
            rarity_data = split_rarities(set_data[0]["data"])
            
            if rarity_data is not None:
                save_rarities(set_code, rarity_data)
        
        if rarity_data is not None:
            rarities.append(rarity_data)
    return rarities

def rarity_code_to_text(code: str) -> str:
    match code:
        case 'm':
            return "mythic"
        case 'r':
            return "rare"
        case 'u':
            return "uncommon"
        case 'c':
            return "common"
    return "unknown"

parser = argparse.ArgumentParser(
                    prog='mtgSetPuller',
                    description='Given a set code, download information about it locally.',
                    epilog='Created by Jooms')
parser.add_argument('-c', '--code', required=True)
parser.add_argument('--nice', default=True, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

rarities = get_rarities([args.code], args.nice)

set_deets = set_detail(args.code)

for set_rarities in rarities:
    print(f"The {set_deets["name"]} set has...")
    
    total = 0
    for rarity_code, cards in set_rarities.items():
        rarity = rarity_code_to_text(rarity_code)
        print(f"\t{len(cards)} {rarity} cards")
        total += len(cards)
    print("\t========")
    print(f"\tTotal: {total} unique card names")
