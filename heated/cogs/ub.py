import discord
from discord.ext import commands

class ub(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['userbanner'])
    async def banner(self, ctx, user: discord.User = None):
        user = user or ctx.author
        
        try:
            user = await self.client.fetch_user(user.id)
            banner_url = user.banner.url if user.banner else None
        except discord.NotFound:
            banner_url = None

        embed = discord.Embed(color=0xCCCCCC)

        if banner_url:
            embed.set_image(url=banner_url)
            embed.set_author(name=f"{user.name}'s Banner", icon_url=user.avatar.url)
            banner_button = discord.ui.Button(label="Banner", style=5, url=banner_url)
            view = discord.ui.View()
            view.add_item(banner_button)
            await ctx.send(embed=embed, view=view)
        else:
            embed.description = f"> <:false:1214258281183453254> {user.name} doesn't have a banner or it's not accessible."
            await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(ub(client))