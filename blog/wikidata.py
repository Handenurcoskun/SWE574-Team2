# wikidata.py

import requests


def search_wikidata_entities(query):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": query,
    }
    response = requests.get(url, params=params)
    return response.json()["search"]
