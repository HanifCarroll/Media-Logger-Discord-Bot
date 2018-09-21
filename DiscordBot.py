import discord
import aiohttp
import asyncio
import os
import time

from urllib.parse import urlparse

try:
    from env import TOKEN
except ModuleNotFoundError:
    pass

TOKEN = os.environ.get('TOKEN') or TOKEN

BACKEND_URL = os.environ.get(
    'BACKEND_URL') or 'http://localhost:8000/logger/new'

print('Bot started...')

domains = [
    'https://soundcloud.com/',
    'https://www.youtube.com/',
    'https://youtu.be/',
    'https://open.spotify.com/'
]


def correct_name(service):

    # Format the name to something the database can work with.

    if 'youtube' in service or 'youtu.be' in service:
        return 'YouTube'

    if 'spotify' in service:
        return 'Spotify'

    if 'soundcloud' in service:
        return 'Soundcloud'


def create_media_objects(message):

    # Create a 'base' media object that has all the properties
    # we can gather without relying on buggy 'message.embed' contents.

    username = message.author.name
    timestamp = message.timestamp
    URLs = urlparse(message.content).geturl().split()
    media_objects = []
    for URL in URLs:
        # Protects against Soundcloud shares from mobile.
        if 'https://' in URL:
            service = urlparse(URL).netloc
            media_objects.append({
                'username': username,
                'timestamp': timestamp,
                'url': URL,
                'service_name': correct_name(service)
            })

    return media_objects


def extract_soundcloud(media_objects):

    # Add details specific to Soundcloud URLs to our media_objects.

    for media_object in media_objects:
        if media_object['service_name'] == 'Soundcloud':
            track_info = urlparse(media_object['url']).path.split('/')
            artist = track_info[1]
            title = (' ').join(track_info[2].split('-'))

            media_object.update({
                'artist': artist.title(),
                'title': title.title()
            })

    return(media_objects)


def extract_embedded(message, media_objects):

    # Add details specific to the embedded objects to our media_objects.

    # We didn't find any embeds in the message (Thanks, Discord), so
    # return the original list.
    if message.embeds == []:
        return media_objects

    # Embeds were found, so let's extract some data from them.
    for media_object in media_objects:
        for embed in message.embeds:

            # Check to see if we're assigning to the right media_object.
            if embed['url'] == media_object['url']:
                title = embed['title']
                thumbnail_url = embed['thumbnail']['url']

                if media_object['service_name'] in ['YouTube', 'Soundcloud']:
                    artist = embed['author']['name']

                if media_object['service_name'] == 'Spotify':
                    artist = embed['description'].split(
                        'by')[1].split('on Spotify')[0]

                media_object.update({
                    'title': title,
                    'thumbnail_url': thumbnail_url,
                    'artist': artist
                })

    return media_objects


async def send_data(media_object):
    async with aiohttp.ClientSession() as session:
        async with session.post(BACKEND_URL, data=media_object) as response:
            res = await response.text()
            print(res)


async def send_gathered_data(media_objects):
    tasks = []

    async with aiohttp.ClientSession():
        if media_objects:
            for media_object in media_objects:
                task = asyncio.ensure_future(send_data(media_object))
                tasks.append(task)

        await asyncio.gather(*tasks)


client = discord.Client()


@client.event
async def on_message(message):
    # Check to see if message contains one of our domains.
    if any(domain in message.content for domain in domains):
        initial_media_objects = create_media_objects(message)

        populate_soundcloud = extract_soundcloud(initial_media_objects)

        populated_media_objects = extract_embedded(
            message, populate_soundcloud)

        await send_gathered_data(populated_media_objects)


def main():
    try:
        client.run(TOKEN)
    except KeyboardInterrupt:
        client.logout()


main()
