import discord

from functions import *
from config import linux_rant

client = discord.Client()

@client.event
async def on_message(message):
    # Check to see if message contains one of our domains.
    if 'linux' in message.content.lower() and not message.author.bot:
         await message.channel.send(linux_rant)

    if any(domain in message.content for domain in domains):
        initial_media_objects = create_media_objects(message)

        populate_soundcloud = extract_soundcloud(initial_media_objects)

        populated_media_objects = extract_embedded(message, populate_soundcloud)
        
        await send_gathered_data(populated_media_objects)