import discord
import config
from discord.ext import commands

class AutoPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fem')
    @commands.is_owner()
    async def fem(self, ctx):
        f = open('./data/female.txt', 'r')
        for lines in f:
            e = discord.Embed(
                color=config.Colors.default
            )
            e.set_image(url=lines)
            await ctx.send(embed=e)

    @commands.command(name='bnr')
    @commands.is_owner()
    async def bnr(self, ctx):
        f = open('./data/banners.txt', 'r')
        for lines in f:
            e = discord.Embed(
                color=config.Colors.default
            )
            e.set_image(url=lines)
            await ctx.send(embed=e)

    @commands.command(name='mel')
    @commands.is_owner()
    async def mel(self, ctx):
        f = open('./data/males.txt', 'r')
        for lines in f:
            e = discord.Embed(
                color=config.Colors.default
            )
            e.set_image(url=lines)
            await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(AutoPost(bot))