import discord
import asyncio
import json
from discord.ext import commands

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['px', 'pre'])
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix=None):
        if new_prefix is None:
            embed = discord.Embed(
                title='Prefix',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Change the bot\'s server prefix'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}prefix [prefix]\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Current Prefix:',
                value=f'```\n{ctx.prefix}\n```',
                inline=True
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\npre, px\n```',
                inline=True
            )
            embed.add_field(
                name='<:wait:1214258202754154617> Permissions:',
                value=f'```\nAdministrator\n```',
                inline=True
            )
            await ctx.send(embed=embed)
        elif len(new_prefix) > 1:
            embed = discord.Embed(
                title='<:false:1214258281183453254> Fail',
                description='> The prefix cannot be longer than 1 character.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            with open("data/prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = new_prefix

            with open("data/prefixes.json", "w") as f:
                json.dump(prefixes, f)

            embed = discord.Embed(
                title='<:true:1214258277391536158> Success',
                description=f'> Changed the **Server Prefix**.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(prefix(client))