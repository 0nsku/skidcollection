import discord
import json
from discord.ext import commands

class on_guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("data/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = ";"
        with open("data/prefixes.json", "w") as f:
            json.dump(prefixes,f)
            
    @commands.command()
    @commands.is_owner()
    async def fix(self, ctx):
        for guild in self.client.guilds:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(guild.id)] = ";"

            with open("data/prefixes.json", "w") as f:
                json.dump(prefixes,f)

        embed = discord.Embed(description=f'> **Successfully** fixed all **Prefixes**')
        await ctx.send(embed=embed)
            
async def setup(client):
    await client.add_cog(on_guild(client))