import argparse
import csv
from lib.loaders.card import load_card, save_card
from lib.obj.cardSet import get_set_counts, filter_sets, sort_set_counts
from lib.apis.scryfall import search_card

def process_list(names: list, useCache: bool) -> list:
    list_data = []
    for n in names:
        data = None
        if useCache:
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
        print("Set Name:", v.name, "- Scryfall ID:", k)
        print("\tSet Type:", v.set_type)
        print(f"\tCards: ({len(v.cards)})")
        for c in v.cards:
            p_range = c.price_range()
            print(f"\t\tName: {c.name} - Price: ${p_range[0]} ~ ${p_range[1]}")
        i += 1
        if i >= top_n:
            break
        print("\n")

def load_csv_lines(filename, delimiter=',', strip_newline=True):
    lines = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            line = row[0]
            if strip_newline:
                line = line.rstrip('\n')
            lines.append(line)
    return lines

parser = argparse.ArgumentParser(
                    prog='mtgSetPicker',
                    description='Given a list of cards you want, find the best set to buy.',
                    epilog='Created by Jooms')
parser.add_argument('-c', '--csv', required=True)
parser.add_argument('-t', '--top', type=int, default=5)
parser.add_argument('--nice', default=True, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

cards = load_csv_lines(args.csv)

data = process_list(cards, args.nice)
set_counts = get_set_counts(data)
set_counts = filter_sets(set_counts)
set_counts = sort_set_counts(set_counts)

print_sorted_set(set_counts, args.top)
