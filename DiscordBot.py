import discord
import requests

from urllib.parse import urlparse

from env import TOKEN

print("Bot started...")

domains = [
    'https://soundcloud.com/',
    'https://www.youtube.com/',
    'https://open.spotify.com/'
]

database_url = 'http://localhost:8000/logger/new'

client = discord.Client()

try:
    client.run(TOKEN)
except KeyboardInterrupt:
    client.logout()


@client.event
async def on_message(message):

    # Check to see if message contains one of our domains
    if any(domain in message.content for domain in domains):

        # Check which domain was found

        # If it's SoundCloud, manually extract the URL
        if domains[0] in message.content:
            extracted = extract_soundcloud(message)
            await send_data(extracted)

        # If it's YouTube or Spotify, then use the 'embeds' property on the message.
        else:
            extracted = extract_embedded(message)
            await send_data(extracted)


def extract_soundcloud(message):
    url = urlparse(message.content).geturl()
    user = message.author.name
    timestamp = message.timestamp
    service = 'Soundcloud'

    data = {
        'url': url,
        'username': user,
        'timestamp': timestamp,
        'service_name': service
    }

    return(data)


def extract_embedded(message):
    for embed in message.embeds:
        url = embed["url"]
        title = embed["title"]
        thumbnail_url = embed["thumbnail"]["url"]
        user = message.author.name
        timestamp = message.timestamp
        service = embed["provider"]["name"]

        data = {
            'url': url,
            'title': title,
            'thumbnail_url': thumbnail_url,
            'username': user,
            'timestamp': timestamp,
            'service_name': service
        }

        return(data)


async def send_data(data):
    r = requests.post(url=database_url, data=data)
    print(r.text)