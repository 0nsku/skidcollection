import discord, datetime, asyncio
from discord.ext import commands 
import aiohttp
import orjson
import humanize
from bs4 import BeautifulSoup
from typing import Union, Optional, Any
import io
from discord.ext.commands import check, BadArgument 
from discord import AllowedMentions, Message, MessageType, File, Embed, File, TextChannel, Member, User, Role
from tools.utils import PaginatorView
import re
import emoji
from discord.ext.commands import Cog, CooldownMapping, BucketType


class ValidAutoreact(commands.EmojiConverter):
 async def convert(self, ctx: commands.Context, argument: str):
  try: 
    emoj = await super().convert(ctx, argument)
  except commands.BadArgument:
    if not emoji.is_emoji(argument):
        return None
    
    emoj = argument 
  return emoj

def duration(n: int) -> str: 
    uptime = int(n/1000)
    seconds_to_minute   = 60
    seconds_to_hour     = 60 * seconds_to_minute
    seconds_to_day      = 24 * seconds_to_hour

    days    =   uptime // seconds_to_day
    uptime    %=  seconds_to_day

    hours   =   uptime // seconds_to_hour
    uptime    %=  seconds_to_hour

    minutes =   uptime // seconds_to_minute
    uptime    %=  seconds_to_minute

    seconds = uptime
    if days > 0: return ("{} days, {} hours, {} minutes, {} seconds".format(days, hours, minutes, seconds))
    if hours > 0 and days == 0: return ("{} hours, {} minutes, {} seconds".format(hours, minutes, seconds))
    if minutes > 0 and hours == 0 and days == 0: return ("{} minutes, {} seconds".format(minutes, seconds))
    if minutes < 0 and hours == 0 and days == 0: return ("{} seconds".format(seconds))

def is_afk():
  async def predicate(ctx: commands.Context):
    check = await ctx.bot.db.fetchrow("SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    return check is None 
  return check(predicate)

def afk_ratelimit(self, message: discord.Message) -> Optional[int]:
    """
    Cooldown for the afk message event
    """

    bucket = self.afk_cd.get_bucket(message)
    return bucket.update_rate_limit()

class Messages(commands.Cog): 
    def __init__(self, bot: commands.AutoShardedBot): 
      self.bot = bot
      self.snipes = {}
      self._ccd = CooldownMapping.from_cooldown(4, 6, BucketType.channel)
      self.edit_snipes = {}
      self.afk_cd = commands.CooldownMapping.from_cooldown(3, 3, commands.BucketType.channel)
      self.autoreact_cd = CooldownMapping.from_cooldown(4, 6, BucketType.channel)

    async def get_autoreact_cd(self, message: Message) -> Optional[int]:

        bucket = self.autoreact_cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def get_ratelimit(self, message: Message) -> Optional[int]: 

         bucket = self._ccd.get_bucket(message)
         return bucket.update_rate_limit()

    @commands.Cog.listener("on_message")
    async def reposter(self, message: discord.Message):
        if not message.guild:
            return
        if message.author.bot:
            return
        args = message.content.split(" ")
        if args[0] == "lune":
            url = args[1]
            check = await self.bot.db.execute("SELECT * FROM nodata WHERE user_id = $1 AND state = $2",
                                             message.author.id, "true")
            if not check:
                return
            if "tiktok" in url:
                async with message.channel.typing():
                    x = await self.bot.session.json("https://tikwm.com/api/", params={"url": url})
                    if x.get("data").get("images"):
                        try:
                            embeds = []
                            for img in x['data']['images']:
                                embed = discord.Embed(color=self.bot.color,
                                                      description=f"page {x['data']['images'].index(img)+1}/{len(x['data']['images'])}").set_author(
                                    name=f"@{x['data']['author']['unique_id']}", icon_url=x["data"]["author"]["avatar"],
                                    url=url)
                                embed.set_image(url=img)
                                embeds.append(embed)
                            v = PaginatorView(await self.bot.get_context(message), embeds)
                            try:
                                await message.delete()
                            except:
                                pass
                            return await message.channel.send(embed=embeds[0], view=v)
                        except:
                            pass
                    else:
                        video = x["data"]["play"]
                        file = discord.File(fp=await self.bot.getbyte(video), filename="lune.mp4")
                        embed = discord.Embed(color=self.bot.color, description=f"[{x['data']['title']}]({url})").set_author(
                            name=f"@{x['data']['author']['unique_id']}", icon_url=x["data"]["author"]["avatar"])
                        x = x["data"]
                        await message.channel.send(embed=embed, file=file)
                        try:
                            await message.delete()
                        except:
                            pass

    @commands.Cog.listener('on_message')
    async def boost_listener(self, message: discord.Message): 
     if "MessageType.premium_guild" in str(message.type):
      if message.guild.id == 1170234585414643742: 
       member = message.author
       check = await self.bot.db.fetchrow("SELECT * FROM donor WHERE user_id = $1", member.id)
       if check: return 
       ts = int(datetime.datetime.now().timestamp())
       await self.bot.db.execute("INSERT INTO donor VALUES ($1,$2)", member.id, ts)  
       return await message.channel.send(f"{member.mention}, thanks for boosting. you now have premium :)")     

    @commands.Cog.listener("on_message")
    async def seen_listener(self, message: discord.Message): 
      if not message.guild: return 
      if message.author.bot: return
      check = await self.bot.db.fetchrow("SELECT * FROM seen WHERE guild_id = {} AND user_id = {}".format(message.guild.id, message.author.id))
      if check is None: return await self.bot.db.execute("INSERT INTO seen VALUES ($1,$2,$3)", message.guild.id, message.author.id, int(datetime.datetime.now().timestamp()))  
      ts = int(datetime.datetime.now().timestamp())
      await self.bot.db.execute("UPDATE seen SET time = $1 WHERE guild_id = $2 AND user_id = $3", ts, message.guild.id, message.author.id)
 

    @commands.Cog.listener('on_message')
    async def afk_listener(self, message: discord.Message):
        if message.is_system():
          return
    
        if not message.guild: 
          return 
    
        if not message.author: 
          return
    
        if message.author.bot: 
          return

        if check := await self.bot.db.fetchrow("SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2", message.guild.id, message.author.id):
          ctx = await self.bot.get_context(message)
          time = check['time']
          time_datetime = datetime.datetime.utcfromtimestamp(time)
          delta = humanize.precisedelta(time_datetime, format="%0.0f")
          che = await self.bot.db.fetchrow("SELECT * from afk where guild_id = $1 AND user_id = $2", message.guild.id, message.author.id)
          await self.bot.db.execute("DELETE FROM afk WHERE guild_id = $1 AND user_id = $2", message.guild.id, message.author.id)
          embed = discord.Embed(
        color=self.bot.color,
        description=f"> {ctx.author.mention}: Welcome back, you went AFK **{self.bot.ext.relative_time(datetime.datetime.fromtimestamp(int(che['time'])))}**"
          )
          return await ctx.send(embed=embed)
    
        for mention in message.mentions:
         check = await self.bot.db.fetchrow("SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2", message.guild.id, mention.id)
         if check:

          ctx = await self.bot.get_context(message)
          time = check['time']
          time_datetime = datetime.datetime.fromtimestamp(time)
          timestamp_format = f"<t:{int(time_datetime.timestamp())}:R>"
          embed = discord.Embed(
        color=self.bot.color,
        description=f"> {ctx.author.mention}: **{mention.name}** is AFK: **{check['reason']}** - {timestamp_format}"
          )
          return await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
     if not message.guild: return 
     if message.author.bot: return
     invites = ["discord.gg/", ".gg/", "discord.com/invite/"]
     if any(invite in message.content for invite in invites):
       check = await self.bot.db.fetchrow("SELECT * FROM antiinvite WHERE guild_id = $1", message.guild.id)
       if check: return

     attachment = message.attachments[0].url if message.attachments else "none"
     author = str(message.author)
     content = message.content
     avatar = message.author.display_avatar.url 
     await self.bot.db.execute("INSERT INTO snipe VALUES ($1,$2,$3,$4,$5,$6,$7)", message.guild.id, message.channel.id, author, content, attachment, avatar, datetime.datetime.now())
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message): 
     if not before.guild: return 
     if before.author.bot: return 
     await self.bot.db.execute("INSERT INTO editsnipe VALUES ($1,$2,$3,$4,$5,$6)", before.guild.id, before.channel.id, before.author.name, before.author.display_avatar.url, before.content, after.content)   

async def setup(bot: commands.AutoShardedBot) -> None: 
  await bot.add_cog(Messages(bot))     
