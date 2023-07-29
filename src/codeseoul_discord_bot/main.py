import discord

from os import getenv
from codeseoul_discord_bot.client import CodeSeoulBotClient


def main():
    print("hello world")
    intents = discord.Intents.default()
    intents.message_content = True
    client = CodeSeoulBotClient(intents=intents)
    api_token = getenv("DISCORD_API_TOKEN")
    client.run(api_token)
