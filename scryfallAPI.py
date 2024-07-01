import requests
import time

def search_card(name: str) -> dict:
    # Add ratelimit to be nice
    # From: https://scryfall.com/docs/api#rate-limits-and-good-citizenship
    time.sleep(0.1)
    
    url = "https://api.scryfall.com/cards/search"
    params = {"q": name, "unique": "prints"}
    req = requests.models.PreparedRequest()
    req.prepare_url(url, params)
    response = requests.get(req.url)

    if response.status_code == 200:
        return response.json()    
    return None