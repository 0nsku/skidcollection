import discord
import config
import time
from discord.ext import commands
from utils.helpers import *

class OwnerCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='restart')
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        embed = discord.Embed(color=config.Colors.default, description="restarting .")
        ambed = discord.Embed(color=config.Colors.default, description="restarting ..")
        bmbed = discord.Embed(color=config.Colors.default, description="restarting ...")
        message = await ctx.send(embed=embed)
        await message.edit(embed=ambed)
        await message.edit(embed=bmbed)
        await message.edit(embed=embed)
        await message.edit(embed=ambed)
        await message.edit(embed=bmbed)
        k = discord.Embed(color=config.Colors.default, description=f"restarted with the ping of {round(self.bot.latency * 1000)}ms")
        await message.edit(embed=k)
        time.sleep(2)
        restart()


async def setup(bot):
    await bot.add_cog(OwnerCmds(bot))