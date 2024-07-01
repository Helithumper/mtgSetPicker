import requests
import time

# Simple pagination handler
def __get_more_pages(data: dict, next_url: str) -> dict:
    response = requests.get(next_url)
    if response.status_code == 200:
        new_data = response.json()
        data["data"].extend(new_data["data"])
        if new_data["has_more"] == True:
            return __get_more_pages(data, new_data["next_page"])
    else:
        print("Issue getting next page!")
    return data

def search_card(name: str) -> dict:
    # Add ratelimit to be nice
    # From: https://scryfall.com/docs/api#rate-limits-and-good-citizenship
    time.sleep(0.1)

    url = "https://api.scryfall.com/cards/search"
    # We want exact names
    name = '!"' + name.strip('"') + '"'
    query_list = [name]
    # Filter out digital cards
    query_list.append("-is:digital")
    # Include things like tokens
    query_list.append("include:extras")

    params = {"q": " ".join(query_list), "unique": "prints"}
    req = requests.models.PreparedRequest()
    req.prepare_url(url, params)
    response = requests.get(req.url)

    if response.status_code == 200:
        data = response.json()
        if data["has_more"] == True:
            data = __get_more_pages(data, data["next_page"])
        return data
    else:
        print("Error querying card list:", response.content)
    return None

def set_list(set_code: str) -> dict:
    # Add ratelimit to be nice
    # From: https://scryfall.com/docs/api#rate-limits-and-good-citizenship
    time.sleep(0.1)

    url = "https://api.scryfall.com/cards/search"
    # We want exact names
    set = 'set:'+set_code
    query_list = [set]
    # Include things like tokens
    query_list.append("include:extras")

    params = {"q": " ".join(query_list)}
    req = requests.models.PreparedRequest()
    req.prepare_url(url, params)
    response = requests.get(req.url)

    if response.status_code == 200:
        data = response.json()
        if data["has_more"] == True:
            data = __get_more_pages(data, data["next_page"])
        return data
    else:
        print("Error getting set list:", response.content)
    return None

def set_detail(set_code: str) -> dict:
    # Add ratelimit to be nice
    # From: https://scryfall.com/docs/api#rate-limits-and-good-citizenship
    time.sleep(0.1)

    url = "https://api.scryfall.com/sets/" + set_code
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting set details:", response.content)
    return None