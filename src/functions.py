import aiohttp
import asyncio
import os

from urllib.parse import urlparse
from config import BACKEND_URL, linux_rant

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
    timestamp = message.created_at
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

    return media_objects


def extract_embedded(message, media_objects):

    # Add details specific to the embedded objects to our media_objects.

    # We didn't find any embeds in the message (Thanks, Discord), so
    # return the original list.
    if not message.embeds:
        return media_objects

    # Embeds were found, so let's extract some data from them.
    for media_object in media_objects:
        for embed in message.embeds:

            # Check to see if we're assigning to the right media_object.
            if embed.url == media_object['url']:
                title = embed.title
                thumbnail_url = embed.thumbnail.url

                if media_object['service_name'] in ['YouTube', 'Soundcloud']:
                    artist = embed.author.name

                if media_object['service_name'] == 'Spotify':
                    artist = embed.description.split(
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
