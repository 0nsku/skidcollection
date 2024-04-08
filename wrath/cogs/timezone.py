from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check
import datetime, discord, humanize, os, arrow, uwuipy, humanfriendly, asyncio 
from discord import Embed, File, TextChannel, Member, User, Role 
from deep_translator import GoogleTranslator
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from discord.ext import commands 
import aiohttp
from discord.ui import Button, View
from pytesseract import pytesseract 
from PIL import Image 
from discord.ext import tasks
from aiohttp import ClientResponse
import typing
import sys
from tools.checks import Perms
from aiogtts import aiogTTS
from random import choice
from typing import Union
from io import BytesIO
from pydantic import BaseModel
from typing import Optional, Tuple
from discord.ext.commands import Converter, BadArgument, MemberConverter
import json

class TimezoneSchema(BaseModel):
  timezone: str 
  date: str

class Timezone():
  def __init__(self, bot):
    self.bot = bot
 
    self.week_days = {
      0: 'Monday',
      1: 'Tuesday',
      2: 'Wednesday',
      3: 'Thursday',
      4: 'Friday',
      5: 'Saturday',
      6: 'Sunday'
    }
 
    self.months = {
      1: 'January',
      2: 'February',
      3: 'March',
      4: 'April',
      5: 'May',
      6: 'June',
      7: 'July',
      8: 'August',
      9: 'September',
      10: 'October',
      11: 'November',
      12: 'December'
    }
  
  async def get_lat_long(self, location: str) -> Optional[dict]: 
    params = {
     'q': location,
     'format': 'json'
    }

    results = await self.bot.session.json(
      'https://nominatim.openstreetmap.org/search', 
      params=params
    )
    if len(results) == 0:
     return None 
    
    return {'lat': float(results[0]['lat']), 'lng': float(results[0]['lon'])}
  
  async def get_timezone(self, member: Member) -> str: 
    timezone = await self.bot.db.fetchval("SELECT zone FROM timezone WHERE user_id = $1", member.id)

    if not timezone:
        return ""

    local = arrow.utcnow().to(timezone).naive
    hour = local.strftime("%I:%M %p")
    week_day = self.week_days.get(local.weekday())
    month = self.months.get(local.month)
    day = self.bot.ordinal(local.day)
    return f"{month} {day}, {hour}"

  async def set_timezone(self, member: Member, location: str) -> str:
    obj = TimezoneFinder()
    kwargs = await self.get_lat_long(location)
    
    if not kwargs: 
      raise BadArgument("Wrong location given")
    
    timezone = await asyncio.to_thread(obj.timezone_at, **kwargs)
    local = arrow.utcnow().to(timezone).naive
    check = await self.bot.db.fetchrow("SELECT * FROM timezone WHERE user_id = $1", member.id)
    
    if not check:
      await self.bot.db.execute("INSERT INTO timezone VALUES ($1,$2)", member.id, timezone)
    else:
      await self.bot.db.execute("UPDATE timezone SET zone = $1 WHERE user_id = $2", timezone, member.id)
    
    hour = local.strftime("%I:%M %p")
    week_day = self.week_days.get(local.weekday())
    month = self.months.get(local.month)
    day = self.bot.ordinal(local.day)
 
    payload = {
      'timezone': timezone,
      'date': f"{month} {day}, {hour}"
    }

    return TimezoneSchema(**payload) 

class TimezoneMember(MemberConverter):
  async def convert(self, ctx: commands.Context, argument: str):
   
   if not argument: 
    return None 
   
   try: 
    member = await super().convert(ctx, argument)
   except: 
    raise BadArgument("Member not found")
   
   tz = Timezone(ctx.bot)
   result = await tz.get_timezone(member)
   
   if not result:
    raise BadArgument("Timezone **not** found for this member")
   
   return [member, result]

class TimezoneLocation(Converter):
  async def convert(self, ctx: commands.Context, argument: str):
    tz = Timezone(ctx.bot)
    return await tz.set_timezone(ctx.author, argument) 



class Timezones(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(
    name="timezone",
    usage="<member>",
    aliases=["time", "tz"],
    invoke_without_command=True,
)
    async def timezone(self, ctx: commands.Context, *, member: Member = None):
        """View a member's timezone"""
        member = member or ctx.author

        timezone = await self.bot.db.fetchval("SELECT zone FROM timezone WHERE user_id = $1", member.id)
        if not timezone:
            return await ctx.send_warning(
            f"Your **timezone** hasn't been set, use `{ctx.clean_prefix}timezone set (location)` to set it"
            if member == ctx.author
            else f"**{member}** hasn't set their **timezone**"
            )

        timestamp = await TimezoneMember().convert(ctx, str(member))
        embed = discord.Embed(
        color=self.bot.color,
        description=(
            f"> Your current time is **{timestamp[1]}**"
            if member.id == ctx.author.id
            else f"> **{member.mention}**'s current time is **{timestamp[1]}**"
        )
        )

        await ctx.send(embed=embed)


    @timezone.command(name="set")
    async def timezone_set(self, ctx: commands.Context, *, timezone: TimezoneLocation):
      await ctx.send_success(f"Saved your timezone as **{timezone.timezone}**")
  
    @timezone.command(name="remove")
    async def timezone_remove(self, ctx: commands.Context):

      await self.bot.db.execute(
      """
      DELETE FROM timezone
      WHERE user_id = $1
      """, 
      ctx.author.id
    )

      return await ctx.send_success(f"Succesfully **removed** your timezone") 

async def setup(bot):
    await bot.add_cog(Timezones(bot))        