import argparse
from card_details import split_rarities, save_rarities
from scryfallAPI import set_list, set_detail
from setLoader import load_set, save_set

def get_sets(codes: list, useCache: bool) -> list:
    list_data = []
    for sc in codes:
        data = None
        # TODO: refactor this to not require a web call just to load locally. Perhaps re-org files?
        detail = set_detail(sc)
        if useCache:
            data = load_set(detail["name"], sc)
        if data is None:
            data = set_list(sc)
            data["set_name"] = detail["name"]
            if data is not None:
                save_set(detail["name"], sc, data)
        if data is not None:
            list_data.append(data)
            
    return list_data

parser = argparse.ArgumentParser(
                    prog='mtgPackLoader',
                    description='Given a set code, download information about it locally.',
                    epilog='Created by Jooms')
parser.add_argument('-c', '--code', required=True)
parser.add_argument('--nice', default=True, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

cards = get_sets([args.code], args.nice)

print(len(cards[0]["data"]))

rarities = split_rarities(cards[0]["data"])

# print(cards["set_name"], rarities)
save_rarities(cards[0]["set_name"], rarities)