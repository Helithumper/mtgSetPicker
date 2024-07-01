class card:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class card_set:
    def __init__(self, name: str, set_type: str):
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
        for card_data in c["data"]:
            set_id = card_data["set_id"]
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


__ignore_set_list = ["The List", "Secret Lair Drop"]


def filter_sets(set_counts: dict) -> dict:
    filtered_sets = {}
    for set_id, sc in set_counts.items():
        if sc.name not in __ignore_set_list:
            filtered_sets[set_id] = sc
    return filtered_sets


def sort_set_counts(set_counts: dict) -> dict:
    sorted_set = {}
    for k, v in sorted(set_counts.items(), key=card_set_count, reverse=True):
        sorted_set[k] = v
    return sorted_set
