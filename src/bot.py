import asyncio
import dotenv
import discord
from discord.ext import commands
import os

dotenv.load_dotenv()

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv("DISCORD_TOKEN"))



if __name__ == "__main__":
   asyncio.run(main())
