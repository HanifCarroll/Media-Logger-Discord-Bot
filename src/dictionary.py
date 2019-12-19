from config import DICTIONARY_API_KEY, DICTIONARY_APP_ID
import json
import requests

BASE_URL = 'https://od-api.oxforddictionaries.com/api/v2/entries/en-us/'


def get_definition(word):
    if not word:
        return "Something went wrong."

    url = BASE_URL + word.lower() + '?fields=definitions'
    r = requests.get(url, headers={"app_id": DICTIONARY_APP_ID, "app_key": DICTIONARY_API_KEY})
    response = r.json()

    result = ''
    for res in response['results']:
        for lexicalEntry in res['lexicalEntries']:
            for entry in lexicalEntry['entries']:
                for sense in entry['senses']:
                    for definition in sense['definitions']:
                        result += definition.capitalize() + '\n'

    return result


async def send_definition(message, content):
    if 'define' not in content:
        return

    split = content.split()

    if split[0] == 'define' and split[1]:
        if split[1] == 'stebin':
            await message.channel.send('A bicc ass nibba')
        else:
            word = split[1]
            definition = get_definition(word)
            await message.channel.send(definition)

