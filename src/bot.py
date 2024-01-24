import dotenv
import discord
import os

dotenv.load_dotenv()

if __name__ == "__main__":
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print("Logged in as")
        print(client.user.name)
        print(client.user.id)
        print("------------------")

    @client.event
    async def on_message(message):
        if message.content.startswith("!hello"):
            await message.channel.send("Hello World!")
        else:
            print("Message received: " + message.content)

    client.run(os.getenv("DISCORD_TOKEN"))
