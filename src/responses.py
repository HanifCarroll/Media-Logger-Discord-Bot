import random
from time import time
from config import linux_rant

last_tymen_time = 0
last_linux_message_time = 0


async def send_hehe_tymen(message, content):
    global last_tymen_time

    if message.content.lower() != 'hehe':
        return

    if time() - last_tymen_time <= 30:
        return

    # if message.author.id == 141338854312378368:
    # :stebin:
    if message.author.id == 482708877276610560:
        if random.random() >= 0.8:
            await message.channel.send('noty my mans')
        else:
            await message.channel.send('tymen')
    else:
        await message.channel.send('tymen')

    last_tymen_time = time()


async def send_linux_rant(message, content):
    if 'linux' in content and 'gnu' not in content:
        global last_linux_message_time

        if time() - last_linux_message_time >= 60:
            last_linux_message_time = time()
            await message.channel.send(linux_rant)
