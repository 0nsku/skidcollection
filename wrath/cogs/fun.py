import discord
import random
from discord.ext import commands
from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check
from compliment import Compliment
import aiohttp

c = Compliment()

class fun(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def urban(self, ctx, *, word):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.urbandictionary.com/v0/define?term={word}") as resp:
                if resp.status != 200:
                    return await ctx.send_warning('Could not fetch the data.')

                data = await resp.json()

                if not data['list']:
                    return await ctx.send_warning('Word not found.')

                definition = data['list'][0]['definition']
                example = data['list'][0]['example']

                embed = discord.Embed(title=word.title(), color=self.bot.color)
                embed.add_field(name='Definition', value=definition, inline=False)
                embed.add_field(name='Example', value=example, inline=False)

                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(fun(bot))