import discord
from discord.ext import commands
from discord.ui import View, Button

class spotify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send("cogs up")

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        spotify_activity = None
        for activity in user.activities:
            if isinstance(activity, discord.Spotify):
                spotify_activity = activity
                break
        if spotify_activity is None:
            embed = discord.Embed(title=f"{user.display_name} is not listening to a song.", color=0x2b2d31)
            await ctx.send(embed=embed)
        else:
            song_link = f"[{spotify_activity.title}]({spotify_activity.track_url})"
            embed = discord.Embed(title=f"{user.display_name} is listening to...", color=0xCCCCCC)
            embed.add_field(name="Song", value=song_link)
            embed.add_field(name="Artist", value=spotify_activity.artist)
            embed.set_thumbnail(url=spotify_activity.album_cover_url)
            button = discord.ui.Button(style=discord.ButtonStyle.link, label="Listen Along", url=spotify_activity.track_url)
            view = discord.ui.View()
            view.add_item(button)
            await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(spotify(client))
    None