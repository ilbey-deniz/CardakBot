import discord
import random
from discord.ext import commands
from service.player import Player
from service.royale import Royale



class Royale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_royales = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Royale cog is ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        await ctx.send(error)


    @commands.command()
    async def royale(self, ctx, *opponents: discord.Member):
        # Check the number of mentioned opponents
        if not 1 <= len(opponents) <= 4:
            await ctx.send("You need to mention 1 to 4 opponents to start a royale.")
            return

        # Check if there is an ongoing royale with any of the mentioned opponents
        for opponent in opponents:
            if (ctx.author.id, opponent.id) in self.active_royales:
                await ctx.send(f"You are already in a royale with {opponent.name}.")
                return

        # Initialize players and start the royale for each opponent pair
        for opponent in opponents:
            players = [Player(ctx.author.name, 50), Player(opponent.name, 50)]
            royale_game = Royale(*players)

            # Store the royale in the active royales dictionary
            self.active_royales[(ctx.author.id, opponent.id)] = royale_game

            # Run the royale
            royale_game.start_royale()

        # Remove the royale from the active royales dictionary after completion
        for opponent in opponents:
            del self.active_royales[(ctx.author.id, opponent.id)]

        # Optionally, you can send the result of the royale to the Discord channel 
        await ctx.send("Royale completed!")
        
async def setup(bot):
    await bot.add_cog(Royale(bot))