import discord
from discord.ext import commands

class restart(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(description="> restarting.", color=0xCCCCCC)
        await ctx.send(embed=embed)
        await self.client.close()
        
        
async def setup(client):
    await client.add_cog(restart(client))