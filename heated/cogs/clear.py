import discord
from discord.ext import commands

class clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        if amount is None:
            embed = discord.Embed(
                title='Clear',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Delete messsages from a channel.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}clear [amount]\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}clear 10\n```',
                inline=True
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\npurge\n```',
                inline=True
            )
            embed.add_field(
                name='<:wait:1214258202754154617> Permissions:',
                value=f'```\nManage Messages\n```',
                inline=True
            )
            await ctx.send(embed=embed)
        else:
            deleted_messages = await ctx.channel.purge(limit=amount + 1)

            embed = discord.Embed(
                title="<:true:1214258277391536158> Success",
                description=f"> Removed {len(deleted_messages) - 1} messages.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(clear(client))