# MTG Set Picker

This is a simple set picker tool for magic the gathering.

## Objective

I have a list of cards I'd like to get. I could buy singles,
but that's no fun. I'd rather buy packs and find what I can.

The same card can be in multiple sets. I don't care which
version of a card I get, only that I have the card.

So:
What set contains the largest number of cards that I'm
looking for?

## Usage

Update cardLists/want.csv with the list of cards you want to search for. The first
column **must** be the **exact** card name. No other columns are processed.
```sh
python main.py --csv cardLists/want.csv
```

### Flags

| flag     | Usage                      | Description                                                      |
| -------- | -------------------------- | ---------------------------------------------------------------- |
| `--csv`  | `--csv cardLists/want.csv` | The list of card names to search for.                            |
| `--top`  | `--top 3`                  | The number of sets to output.                                    |
| `--nice` | `--no-nice`                | If nice, use a local cache. If not, hit scryfall for every card. |

Example complex usage:
```sh
python main.py -c cardLists/want.csv -t 7 --no-nice
```


## Bonus Features

1. Cache data from scryfall so I don't overwhelp their API.
1. Rate-limit scryfall calls because they asked nicely (https://scryfall.com/docs/api#rate-limits-and-good-citizenship).

