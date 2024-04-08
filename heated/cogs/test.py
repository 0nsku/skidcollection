import discord
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send("cogs up")
        
async def setup(client):
    await client.add_cog(test(client))