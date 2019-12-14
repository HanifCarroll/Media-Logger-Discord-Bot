#!/usr/bin/env python3

import discord

from config import TOKEN
from client import client


def main():
    try:
        print('Bot started...')
        client.run(TOKEN)
    except KeyboardInterrupt:
        client.logout()


main()
