import discord
from discord.ext import commands

class lock(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        if ctx.guild and isinstance(ctx.channel, discord.TextChannel):
            current_permissions = ctx.channel.overwrites_for(ctx.guild.default_role)
            current_permissions.send_messages = False
            current_permissions.create_public_threads = False
            current_permissions.create_private_threads = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=current_permissions)

            embed = discord.Embed(
                title="",
                description=f"> <:lock:1216075496673116261>  ***Locked the channel:*** {ctx.channel.mention}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        if ctx.guild and isinstance(ctx.channel, discord.TextChannel):
            current_permissions = ctx.channel.overwrites_for(ctx.guild.default_role)
            current_permissions.send_messages = None
            current_permissions.create_public_threads = None
            current_permissions.create_private_threads = None
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=current_permissions)

            embed = discord.Embed(
                title="",
                description=f"> <:unlock:1216075542256681031>  ***Unlocked the channel:*** {ctx.channel.mention}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(lock(client))