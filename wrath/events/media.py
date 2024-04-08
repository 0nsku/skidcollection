import discord
from discord.ext import commands
import yt_dlp
import os

MAX_FILE_SIZE_MB = 100

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'best',
            'outtmpl': 'wrathYouTube.mp4',
            'verbose': False,
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }
            ],
        }

    async def file_size_check(self, ctx: commands.Context, file_path: str) -> bool:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            await ctx.send(embed=discord.Embed(
                description=f"> The file exceeds the **{MAX_FILE_SIZE_MB}MB** upload limit.",
                color=self.bot.color
            ))
            return False
        return True

    @commands.command()
    async def youtube(self, ctx: commands.Context, url: str):
        try:
            print(f"Downloading video from URL: {url}")
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    filename = "wrathYouTube.mp4"
                    print(f"Video downloaded and saved as: {filename}")
                except yt_dlp.utils.FileTooLarge as e:
                    await ctx.send(embed=discord.Embed(
                        description=f"> The video [**{url}**] exceeds the **{MAX_FILE_SIZE_MB}MB** upload limit.",
                        color=self.bot.color
                    ))
                    return

            downloading_embed = discord.Embed(
                description=f"> Downloading your [**video**]({url}), this may take a **while** to process.",
                color=self.bot.color
            )
            downloading_message = await ctx.send(embed=downloading_embed)

            if not await self.file_size_check(ctx, filename):
                os.remove(filename)
                await downloading_message.delete()
                print(f"File {filename} was deleted due to size limit.")
                return

            await ctx.send(file=discord.File(filename))
            os.remove(filename)
            print(f"Uploaded file: {filename}")
            await downloading_message.delete()
            print("Downloading message deleted.")

        except yt_dlp.DownloadError as e:
            if "HTTP Error 413" in str(e):
                await ctx.send(embed=discord.Embed(
                    description=f"> The video [**{url}**] exceeds the **{MAX_FILE_SIZE_MB}MB** upload limit.",
                    color=self.bot.color
                ))
            else:
                await ctx.send(f"An error occurred: {e}")

async def setup(bot: commands.AutoShardedBot) -> None: 
    await bot.add_cog(Media(bot))