import asyncio
import dotenv
import discord
from discord.ext import commands
import os

dotenv.load_dotenv()

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
cog_dir = os.path.join(os.path.dirname(__file__), "cogs")

async def load_extensions():
    try:
        for filename in os.listdir(cog_dir):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await client.load_extension(f"cogs.{filename[:-3]}")
    except Exception as e:
        print(f"Failed to load cogs: {e}")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv("DISCORD_TOKEN"))



if __name__ == "__main__":
   asyncio.run(main())
