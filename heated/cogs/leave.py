import discord
from discord.ext import commands

class leave(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.client.get_guild(guild_id)
            if guild is None:
                return await ctx.send("Invalid ID.")

        await guild.leave()
        print(f'Left {guild.name} ({guild.id})')
        
async def setup(client):
    await client.add_cog(leave(client))