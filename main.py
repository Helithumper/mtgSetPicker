from cardLoader import load_card, save_card
from library import get_set_counts, sort_set_counts
from scryfallAPI import search_card

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
