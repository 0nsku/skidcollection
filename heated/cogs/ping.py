import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    def get_ping_emoji(self, latency):
        if latency < 50:
            return "<:good:1214258219619192882>"
        elif latency < 100:
            return "<:okay:1214258223901581402>"
        else:
            return "<:bad:1214258227189911623>"
        
    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)
        emoji = self.get_ping_emoji(latency)

        embed = discord.Embed(
            title=f"{emoji} Pong!",
            description=f"Latency: {latency}ms",
            color=0xCCCCCC
        )
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(ping(client))