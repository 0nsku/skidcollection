import discord
from discord.ext import commands

class kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            embed = discord.Embed(
                title='Kick',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Kick a user.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}kick [@user] (reason)\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}kick @rip.rive swearing\n```',
                inline=True
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\nk\n```',
                inline=True
            )
            embed.add_field(
                name='<:wait:1214258202754154617> Permissions:',
                value=f'```\nKick Members\n```',
                inline=True
            )
            await ctx.send(embed=embed)
        else:
            if reason is None:
                reason = "None"
                
            try:
                kick_embed = discord.Embed(
                    title="<:punishment:1216075459889205299> You've been kicked.",
                    color=0xCCCCCC
                )
                kick_embed.add_field(name="From:", value=f"> {ctx.guild.name}", inline=True)
                kick_embed.add_field(name="By:", value=f"{ctx.author.mention}", inline=True)
                kick_embed.add_field(name="Reason:", value=f"{reason}", inline=True)
                await member.send(embed=kick_embed)
            except discord.Forbidden:
                pass

            await member.kick(reason=reason)

            embed = discord.Embed(
                title="<:true:1214258277391536158> Success",
                description=f"",
                color=discord.Color.green()
            )
            embed.add_field(name="Kicked:", value=f"> {member.mention} was kicked by {ctx.author.mention}.")
            embed.add_field(name="Reason:", value=f"> {reason}" or 'None', inline=False)
            await ctx.send(embed=embed)
            
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> Missing `kick_members` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(kick(client))