import discord
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alias=["hi"])
    async def hello(self, ctx):
        await ctx.send("Hello!" + str(ctx.author.mention))

    def setup(bot):
        bot.add_cog(Hello(bot))