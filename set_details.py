import json
import unicodedata
import re

# Based on Django's slugify
def __cleanFileName(name: str) -> str:
    name = str(name)
    value = (
        unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def load_rarity_chances(set_code: str, pack_type: str) -> dict:
    clean_code = __cleanFileName(set_code)
    clean_pack_name = __cleanFileName(pack_type)

    data = None
    with open(f"packData/{clean_code}/{clean_pack_name}.json", "r") as f:
        data = json.load(f)

    odds = {}
    for rarity_type, chance in data["types"].items():
        odds[rarity_type] = {}
        for count, pct in chance.items():
            odds[rarity_type][int(count)] = pct
    return odds

def get_card_chances(set_card_rarities: dict, pack_rarity_chances: dict, card_name: str) -> float:
    chance = 0
    for rarity, cards in set_card_rarities.items():
        for card in cards:
            # If card is found in this rarity
            if card["name"] == card_name:
                print(f"{card_name} found in {rarity} category in set.")
                # Increase chance by chance of that rarity divide by count in rarity.
                for pr_type in pack_rarity_chances:
                    div = 0
                    card_cat_count = 0
                    if pr_type == rarity:
                        div = 1 / len(set_card_rarities[rarity])
                        card_cat_count = len(set_card_rarities[rarity])
                    elif pr_type == "mr":
                        # Total number of cards in m or r
                        if rarity == "m" or rarity == "r":
                            # rares are printed twice as often as mythics?
                            div = 1 / (len(set_card_rarities["m"]) + (len(set_card_rarities["r"]) * 2))
                            card_cat_count = len(set_card_rarities["m"]) + len(set_card_rarities["r"])
                    elif pr_type == "ucc":
                        if rarity == "u" or rarity == "c":
                            # commons are printed twice as often as uncommons????
                            div = 1 / (len(set_card_rarities["u"]) + (len(set_card_rarities["c"]) * 2))
                            card_cat_count = len(set_card_rarities["u"]) + len(set_card_rarities["c"])
            
                    # TODO: Handle wildcard
                    # TODO: Handle tal (token, ad, list)
                    if div == 0:
                        continue
                        
                    chance_rarity = 0
                    # Sum up chances of seeing N of these cards.
                    # TODO: Can a card show up in multiple rarities in a single set?
                    for cnt, pct in pack_rarity_chances[pr_type].items():
                        chance_rarity += cnt * pct * 100
                        print(f"\t{pct * 100:.0f}% chance that {cnt} cards of rarity {pr_type} are in this pack.")
                    print(f"\t\t{chance_rarity:.1f}% chance of {pr_type} in pack")
                    print(f"\t\t{card_cat_count} cards in this rarity")
                    print(f"\t\t{chance_rarity * div:.2f}% chance card is found in this slot")
                    chance += chance_rarity * div
                    print()
    return chance
