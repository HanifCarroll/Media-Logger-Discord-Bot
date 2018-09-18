import discord
import aiohttp
import os

from urllib.parse import urlparse

try:
    from env import TOKEN
except ModuleNotFoundError:
    pass

TOKEN = os.environ.get("TOKEN") or TOKEN

BACKEND_URL = os.environ.get(
    "BACKEND_URL") or 'http://localhost:8000/logger/new'

print("Bot started...")

domains = [
    'https://soundcloud.com/',
    'https://www.youtube.com/',
    'https://open.spotify.com/'
]


def extract_soundcloud(message):
    url = urlparse(message.content).geturl()
    track_info = urlparse(url).path.split('/')

    artist = track_info[1]
    title = (' ').join(track_info[2].split('-'))
    user = message.author.name
    timestamp = message.timestamp
    service = 'Soundcloud'

    data = {
        'url': url,
        'username': user,
        'artist': artist,
        'title': title,
        'timestamp': timestamp,
        'service_name': service
    }

    return(data)


def extract_embedded(message):
    embeds = []

    for embed in message.embeds:

        url = embed["url"]
        title = embed["title"]
        thumbnail_url = embed["thumbnail"]["url"]
        user = message.author.name
        timestamp = message.timestamp
        service = embed["provider"]["name"]

        if service == 'YouTube':
            artist = embed["author"]["name"]

        if service == 'Spotify':
            artist = embed["description"].split("by")[1].split("on Spotify")[0]

        data = {
            'url': url,
            'artist': artist,
            'title': title,
            'thumbnail_url': thumbnail_url,
            'username': user,
            'timestamp': timestamp,
            'service_name': service
        }

        embeds.append(data)

    return(embeds)


async def send_data(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(BACKEND_URL, data=data) as response:
            res = await response.text()
            print(res)


client = discord.Client()


@client.event
async def on_message(message):

    # Check to see if message contains one of our domains
    if any(domain in message.content for domain in domains):
        print(message.content)
        print(message.embeds)
        # Check which domain was found

        # If it's SoundCloud, manually extract the URL
        if domains[0] in message.content:
            extracted = extract_soundcloud(message)
            await send_data(extracted)

        # If it's YouTube or Spotify, then use the 'embeds' property on the message.
        else:
            extracted = extract_embedded(message)
            for message_data in extracted:
                await send_data(message_data)


def main():
    try:
        client.run(TOKEN)
    except KeyboardInterrupt:
        client.logout()


main()
