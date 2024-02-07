import discord
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Hello cog is ready")
    

    

    @commands.command(aliases=["hi"])
    async def hello(self, ctx):
        await ctx.send("Hello!" + str(ctx.author.mention))

async def setup(bot):
    await bot.add_cog(Hello(bot))