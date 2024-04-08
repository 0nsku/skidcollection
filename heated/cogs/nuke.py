import discord
from discord.ext import commands

class nuke(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, error=None):
        original_channel = ctx.channel
        channel_name = original_channel.name
        channel_category = original_channel.category
        channel_position = original_channel.position
        overwrites = {o[0]: o[1] for o in original_channel.overwrites.items()}

        if channel_category:
            new_channel = await channel_category.create_text_channel(
                name=channel_name,
                position=channel_position,
                overwrites=overwrites
            )
        else:
            new_channel = await ctx.guild.create_text_channel(
                name=channel_name,
                position=channel_position,
                overwrites=overwrites
            )

        embed = discord.Embed(
            title="",
            description=f"> <:true:1214258277391536158> nuked `{channel_name}`",
            color=discord.Color.green()
        )
        await new_channel.send(embed=embed)

        await original_channel.delete()
        
        
    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> Missing `manage_channels` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(nuke(client))