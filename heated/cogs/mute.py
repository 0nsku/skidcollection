import discord
from discord.ext import commands
from datetime import timedelta

class mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str, *, reason=None):
        if member == ctx.author:
            embed = discord.Embed(title="Error", description="You cannot mute yourself.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        elif member.top_role >= ctx.author.top_role:
            embed = discord.Embed(title="Error", description="You cannot mute a member with a role equal or higher than yours.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        elif member.is_timed_out():
            embed = discord.Embed(title="Error", description="This member is already timed out.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        unit = duration[-1]
        if unit not in ['m', 'h', 'd', 'w', 'mn']:
            embed = discord.Embed(title="Error", description="Invalid duration unit. Use m for minutes, h for hours, d for days, w for weeks, or mn for months.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        try:
            duration_value = int(duration[:-1])
        except ValueError:
            embed = discord.Embed(title="Error", description="Invalid duration value. Please provide a valid integer.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if duration_value <= 0:
            embed = discord.Embed(title="Error", description="Invalid duration value. Please provide a positive integer.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if unit == 'm':
            duration = timedelta(minutes=duration_value)
        elif unit == 'h':
            duration = timedelta(hours=duration_value)
        elif unit == 'd':
            duration = timedelta(days=duration_value)
        elif unit == 'w':
            duration = timedelta(weeks=duration_value)
        elif unit == 'mn':
            duration = timedelta(days=30 * duration_value)

        await member.timeout(duration, reason=reason)

        embed = discord.Embed(title="Member Muted", color=discord.Color.red())
        embed.add_field(name="Member", value=member.mention)
        embed.add_field(name="Duration", value=f"{duration_value} {unit}")
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Muted by {ctx.author}", icon_url=ctx.author.avatar_url)
    
async def setup(client):
    await client.add_cog(mute(client))