from dotenv import load_dotenv
import os
import discord

from client import JPEGBot
from google_image import GoogleImage


if __name__ == '__main__':
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    client = JPEGBot(intents=intents)
    client.run(os.environ['TOKEN'])
