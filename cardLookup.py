import argparse
from lib.manipulators.card import load_rarities
from lib.manipulators.set import load_rarity_chances, get_card_chances

parser = argparse.ArgumentParser(
                    prog='mtgCardLookup',
                    description='Given a card name, look up the likelyhood it\'s in a given pack.\n' +
                    'This only works with local data, make sure you run setPuller first.',
                    epilog='Created by Jooms')
parser.add_argument('-c', '--set_code', required=True)
parser.add_argument('-p', '--pack_type', required=True)
parser.add_argument('-n', '--name', required=True)
args = parser.parse_args()

print()

# Load pack rarity chances
pack_rarities = load_rarity_chances(args.set_code, args.pack_type)

# Load set cards
set_cards_by_rarity = load_rarities(args.set_code)

# Get chance
ch = get_card_chances(set_cards_by_rarity, pack_rarities, args.name)

print("\n=========================")
print(f"There's a {ch:.2f}% chance that {args.name} is in a {args.pack_type} pack from set {args.set_code}")
print("=========================\n")
