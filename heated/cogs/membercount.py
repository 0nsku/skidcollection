import discord
from discord.ext import commands

class membercount(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["mc"])
    async def membercount(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.client.get_guild(guild_id)
            if guild is None:
                return await ctx.send("didnt find id. *embed not finished.*")

        total = guild.member_count
        bots = sum(1 for member in guild.members if member.bot)
        humans = total - bots

        embed = discord.Embed(
            title="",
            description=f"**{guild.name}'s** members",
            color=0xCCCCCC
        )
        embed.add_field(name="<:minus:1203037065705562153> <:users:1214258272735858728> Total", value=f"<:rp:1197985417908191452> `{total}`", inline=True)
        embed.add_field(name="<:minus:1203037065705562153> <:bot:1214258194201706606> Bots", value=f"<:rp:1197985417908191452> `{bots}`", inline=True)
        embed.add_field(name="<:minus:1203037065705562153> <:members:1215982956334809180> Humans", value=f"<:rp:1197985417908191452> `{humans}`", inline=True)

        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(membercount(client))