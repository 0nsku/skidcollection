import discord
from discord.ext import commands
import datetime
from discord.ui import View, Button
from discord.utils import format_dt

class avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['av', 'ava'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member=None):
        member = ctx.author if not member else member
        avatar_url = member.avatar.url
        embed = discord.Embed(color=0xCCCCCC)
        embed.set_image(url=avatar_url)

        if not embed.author:
            embed.set_author(name=f"{member.name}'s Avatar", icon_url=member.avatar.url)

            avatar_button = Button(label="Avatar", style=5, url=avatar_url)

            view = View()
            view.add_item(avatar_button)

        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(avatar(client))
