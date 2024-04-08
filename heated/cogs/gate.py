import discord
from discord.ext import commands

class gate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel_id = 1215723904035725352
        channel = self.client.get_channel(channel_id)
        
        embed = discord.Embed(
            title=f"",
            description=f"",
            color=0xCCCCCC
        )
        embed.add_field(name="Joined:", value=f"<:rp:1197985417908191452> ***` {guild.name} `***", inline=True)
        embed.add_field(name="Members:", value=f"<:rp:1197985417908191452> ***` {guild.member_count} `***", inline=True)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel_id = 1215723904035725352
        channel = self.client.get_channel(channel_id)
        
        embed = discord.Embed(
            title=f"",
            description=f"",
            color=0xCCCCCC
        )
        embed.add_field(name="Left:", value=f"<:rp:1197985417908191452> ***` {guild.name} `***", inline=True)
        embed.add_field(name="Members:", value=f"<:rp:1197985417908191452> ***` {guild.member_count} `***", inline=True)
        await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(gate(client))