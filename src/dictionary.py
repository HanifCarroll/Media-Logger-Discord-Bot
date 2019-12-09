from config import DICTIONARY_API_KEY, DICTIONARY_APP_ID
import json
import requests

BASE_URL = f'https://od-api.oxforddictionaries.com/api/v2/entries/en-us/'

def getDefinition(word):
    if not word:
        return "Something went wrong."

    url = BASE_URL + word.lower() + '?fields=definitions'
    r = requests.get(url, headers = {"app_id": DICTIONARY_APP_ID, "app_key": DICTIONARY_API_KEY})
    response = r.json()

    result = ''
    for res in response['results']:
        for lexicalEntry in res['lexicalEntries']:
            for entry in lexicalEntry['entries']:
                for sense in entry['senses']:
                    for definition in sense['definitions']:
                        result += definition.capitalize() + '\n'

    return result