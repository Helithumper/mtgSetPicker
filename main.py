import argparse
import csv
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
        print(f"\tcards: ({len(v.cards)})")
        for c in v.cards:
            print("\t\tName:", c.name, "- Price:", c.price)
        i += 1
        if i >= top_n:
            break

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
args = parser.parse_args()

cards = load_csv_lines(args.csv)

data = process_list(cards)
set_counts = get_set_counts(data)
set_counts = sort_set_counts(set_counts)

print_sorted_set(set_counts, 5)
