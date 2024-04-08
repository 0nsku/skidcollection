import discord
from discord.ext import commands

class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["clap", "b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            embed = discord.Embed(
                title='Ban',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Ban a user.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}ban [@user] (reason)\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}ban @rip.rive swearing\n```',
                inline=True
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\nclap, b\n```',
                inline=True
            )
            embed.add_field(
                name='<:wait:1214258202754154617> Permissions:',
                value=f'```\nBan Members\n```',
                inline=True
            )
            await ctx.send(embed=embed)
        else:
            if reason is None:
                reason = "None"
                
            try:
                ban_embed = discord.Embed(
                    title="<:punishment:1216075459889205299> You've been banned.",
                    color=0xCCCCCC
                )
                ban_embed.add_field(name="From:", value=f"> {ctx.guild.name}", inline=True)
                ban_embed.add_field(name="By:", value=f"{ctx.author.mention}", inline=True)
                ban_embed.add_field(name="Reason:", value=f"{reason}", inline=True)
                await member.send(embed=ban_embed)
            except discord.Forbidden:
                pass

            await ctx.guild.ban(member)

            embed = discord.Embed(
                title="<:true:1214258277391536158> Success",
                description=f"",
                color=discord.Color.green()
            )
            embed.add_field(name="Banned:", value=f"> {member.mention} was banned by {ctx.author.mention}.")
            embed.add_field(name="Reason:", value=f"> {reason}" or 'None', inline=False)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(ban(client))