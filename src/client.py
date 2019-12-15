import discord

from time import time
from functions import *
from config import linux_rant
from dictionary import get_definition

client = discord.Client()

last_linux_message_time = 0


@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    if 'define' in content:
        split = content.split()

        if split[0] == 'define' and split[1]:
            if split[1] == 'stebin':
                await message.channel.send('A bicc ass nibba')
            else:
                word = split[1]
                definition = get_definition(word)
                await message.channel.send(definition)

    if 'linux' in content and 'gnu' not in content:
        global last_linux_message_time

        if time() - last_linux_message_time >= 60:
            last_linux_message_time = time()
            await message.channel.send(linux_rant)
            
    # Check to see if message contains one of our domains.
    if any(domain in content for domain in domains):
        initial_media_objects = create_media_objects(message)

        populate_soundcloud = extract_soundcloud(initial_media_objects)

        populated_media_objects = extract_embedded(message, populate_soundcloud)
        
        await send_gathered_data(populated_media_objects)