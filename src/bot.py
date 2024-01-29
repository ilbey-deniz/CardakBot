import dotenv
import discord
from discord.ext import commands
import os

dotenv.load_dotenv()

if __name__ == "__main__":
    client = commands.Bot(command_prefix = "-", intents=discord.Intents.all())

    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            client.load_extension("cogs." + f[:-3])

    client.run(os.getenv("DISCORD_TOKEN"))
