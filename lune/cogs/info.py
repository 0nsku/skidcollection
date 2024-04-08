import discord, random
import aiohttp
import os
import datetime
from discord.ext import commands
from discord.ui import View, Button
import json
from datetime import datetime, timedelta
import psutil

class info(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot        

   @commands.hybrid_command(description="Check how long Lune has been up for", help="info")
   async def uptime(self, ctx: commands.Context):
     e = discord.Embed(color=self.bot.color, description=f"**{self.bot.ext.uptime}**")
     await ctx.reply(embed=e)

   @commands.hybrid_command(help="info", description="Show Bot Information", aliases=["about", "info", "bi", "sys"]) 
   async def botinfo(self, ctx: commands.Context):
    current_time = datetime.utcnow()

    uptime_str = self.bot.ext.uptime 

    uptime_delta = timedelta()
    time_units = uptime_str.split(', ')
    for unit in time_units:
        value, unit_type = unit.split(' ')
        value = int(value)
        if 'day' in unit_type:
            uptime_delta += timedelta(days=value)
        elif 'hour' in unit_type:
            uptime_delta += timedelta(hours=value)
        elif 'minute' in unit_type:
            uptime_delta += timedelta(minutes=value)
        elif 'second' in unit_type:
            uptime_delta += timedelta(seconds=value)

    uptime_timestamp = (current_time - uptime_delta).timestamp()

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    embed = discord.Embed(color=self.bot.color, description=f"""
    Enhance your **discord experience**, using **lune**                    
    Serving **{len(self.bot.guilds)}** servers with **{sum(g.member_count for g in self.bot.guilds):,}** users

    """)   

    embed.add_field(name="System", value=f"**CPU:** {cpu_usage:.2f}%\n**Memory:** {memory_usage:.2f} GB\n**Launched:** <t:{int(uptime_timestamp)}:R>", inline= True)
    embed.add_field(name="Bot", value=f"**Ping:** {self.bot.latency * 1000:.2f}ms\n**Commands:** {len(set(self.bot.walk_commands()))}\n**Cogs:** {len(self.bot.cogs)}", inline= True)
    embed.set_author(name=self.bot.user.name, icon_url=f"{self.bot.user.avatar.url}")
    embed.set_thumbnail(url=f"{self.bot.user.avatar.url}")

    await ctx.reply(embed=embed)
    
   @commands.hybrid_command(description="Check the bots connection", help="info")
   async def ping(self, ctx):
    await ctx.reply(f"... `{self.bot.ping}ms`")

   @commands.hybrid_command(description="Invite Lune", help="info", aliases=["support", "inv"])
   async def invite(self, ctx):
    avatar_url = self.bot.user.avatar.url
    embed = discord.Embed(color=self.bot.color, description="Add the bot in your server!")
    embed.set_author(name=self.bot.user.name, icon_url=f"{avatar_url}")
    button1 = Button(label="Invite", url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot")
    button2 = Button(label="Support", url="https://discord.gg/UZDrHzqpuC")
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.reply(view=view)

async def setup(bot) -> None:
    await bot.add_cog(info(bot))      
