import discord
import random
import responses
import dictionary
import media_logger


client = discord.Client()


@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    await responses.send_hehe_tymen(message, content)
    await responses.send_linux_rant(message, content)
    await dictionary.send_definition(message, content)
    await media_logger.collect_media_data(message, content)
