import discord
from discord.ext import commands
from service.royale_logic import RoyaleLogic


class Royale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Royale cog is online")


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        await ctx.send(error)
    

    @commands.command(aliases=["r"])
    async def royale(self, ctx, *players: discord.Member):
        
        players = list(players)
        player_names = [player.global_name for player in players]

        for player in player_names:
            await ctx.send(f"{player} has joined the game")

        result = RoyaleLogic(player_names).start_game()

        for message in result:
            await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Royale(bot))