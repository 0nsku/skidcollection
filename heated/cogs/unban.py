import discord
from discord.ext import commands

class unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ub"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_id: int = None, *, reason=None):
        if member_id is None:
            embed = discord.Embed(
                title='Unban',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Unban a user.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}unban [@user] (reason)\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}unban @rip.rive appealed\n```',
                inline=True
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\nub\n```',
                inline=True
            )
            embed.add_field(
                name='<:wait:1214258202754154617> Permissions:',
                value=f'```\nBan Members\n```',
                inline=True
            )
            await ctx.send(embed=embed)
            return

        try:
            banned_user = await self.client.fetch_user(member_id)
        except discord.NotFound:
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> User is **not** banned.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        await ctx.guild.unban(banned_user, reason=reason)

        unban_embed = discord.Embed(
            title="<:true:1214258277391536158> Success",
            description=f"",
            color=discord.Color.green()
        )
        unban_embed.add_field(name="Unbanned:", value=f"> {banned_user.mention} was unbanned by {ctx.author.mention}.")
        unban_embed.add_field(name="Reason:", value=f"> {reason}" or 'None', inline=False)
        await ctx.send(embed=unban_embed)

        try:
            unban_dm_embed = discord.Embed(
                title="<:punishment:1216075459889205299> You've been unbanned.",
                color=0xCCCCCC
            )
            unban_dm_embed.add_field(name="From:", value=f"> {ctx.guild.name}", inline=True)
            unban_dm_embed.add_field(name="By:", value=f"{ctx.author.mention}", inline=True)
            unban_dm_embed.add_field(name="Reason:", value=f"{reason}", inline=True)
            await banned_user.send(embed=unban_dm_embed)
        except discord.Forbidden:
            pass

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> Missing `ban_members` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.UserNotFound):
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> User is **not** banned.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(unban(client))