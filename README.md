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

```sh
python main.py -c cardLists/want.csv
```

This will use the provided csv to search for cards, you can update that csv or point to your own. The name of the card you are searching for **must** be the first column of the csv.

This tool only searches using the card name, all other fields are ignored.

## Bonus Features

1. Cache data from scryfall so I don't overwhelp their API.
1. Rate-limit scryfall calls because they asked nicely (https://scryfall.com/docs/api#rate-limits-and-good-citizenship).

