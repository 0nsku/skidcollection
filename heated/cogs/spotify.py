import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)  

class ListenHere(discord.ui.View):
    def __init__(self, activity):
        super().__init__(timeout=None)
        button = discord.ui.Button(label='Listen Here', style=discord.ButtonStyle.url, url=activity.track_url)
        self.add_item(button)   

class spotify(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['sp'])
    async def spotify(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, discord.Spotify):
                    embed = discord.Embed(
                        title=f"{user.display_name}'s Spotify",
                        description=f"Listening to {activity.title}",
                        color=0x00ff0a
                    )
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text=f"Song started at {activity.created_at.strftime('%H:%M')}")
                    
                    await ctx.reply(embed=embed, view=ListenHere(activity))
                    return
            else:
                embederror = discord.Embed(
                    title="Failed",
                    description=f"{user.mention} is not listening to Spotify right now",
                    color=discord.Color.light_gray()
                )
                await ctx.reply(embed=embederror)
        else:
            embederror = discord.Embed(
                title="Failed",
                description=f"{user.mention} is not listening to Spotify right now",
                color=discord.Color.light_gray()
            )
            await ctx.reply(embed=embederror)



async def setup(client):
    await client.add_cog(spotify(client))