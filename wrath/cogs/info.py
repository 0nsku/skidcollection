import discord, random
import aiohttp
import os
import datetime
from discord.ext import commands, tasks
from discord.ui import View, Button
import json
from datetime import datetime, timedelta
import psutil
from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check
import contextlib
import requests
from tools.checks import Perms as utils, Boosts


class info(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot        

   @commands.hybrid_command(description="show the current uptime", help="info")
   async def uptime(self, ctx: commands.Context):
     e = discord.Embed(color=self.bot.color, description=f"> **{self.bot.ext.uptime}**")
     await ctx.reply(embed=e)

   @commands.hybrid_command(help="info", description="info about wrath", aliases=["about", "info", "bi", "sys"]) 
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
    serving **{len(self.bot.guilds)}** servers with **{sum(g.member_count for g in self.bot.guilds):,}** users

    """)   

    embed.add_field(name="system", value=f"**cpu:** {cpu_usage:.2f}%\n**memory:** {memory_usage:.2f} GB\n**launched:** <t:{int(uptime_timestamp)}:R>", inline= True)
    embed.add_field(name="bot", value=f"**ping:** {self.bot.latency * 1000:.2f}ms\n**commands:** {len(set(self.bot.walk_commands()))}\n**cogs:** {len(self.bot.cogs)}", inline= True)
    embed.set_thumbnail(url=f"{self.bot.user.avatar.url}")

    await ctx.reply(embed=embed)
    
   @commands.hybrid_command(description="check ping", help="info")
   async def ping(self, ctx):
    await ctx.reply(f"... `{self.bot.ping}ms`")

   @commands.hybrid_command(description="invite wrath", help="info", aliases=["support", "inv"])
   async def invite(self, ctx):
    button1 = Button(label="invite", url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot")
    view = View()
    view.add_item(button1)
    await ctx.reply(view=view)

   @hybrid_command(description="Change the guild prefix", usage="[prefix]", help="config", brief="manage guild")
   @utils.get_perms("manage_guild")
   async def prefix(self, ctx: Context, prefix: str):      
       if len(prefix) > 3: return await ctx.send_error("That prefix is **too** long")
       check = await self.bot.db.fetchrow("SELECT * FROM prefixes WHERE guild_id = {}".format(ctx.guild.id)) 
       if check is not None: await self.bot.db.execute("UPDATE prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
       else: await self.bot.db.execute("INSERT INTO prefixes VALUES ($1, $2)", ctx.guild.id, prefix)
       return await ctx.send_success(f"The prefix has been **changed** to `{prefix}`")
   
   @hybrid_command(description="set your own prefix", usage="[prefix]", help="config")
   async def selfprefix(self, ctx: Context, prefix: str):      
      if len(prefix) > 3 and prefix.lower() != "none": return await ctx.send_error("That **prefix** is **too long**")
      if prefix.lower() == "none": 
        check = await self.bot.db.fetchrow("SELECT * FROM selfprefix WHERE user_id = {}".format(ctx.author.id)) 
        if check is not None:
          await self.bot.db.execute("DELETE FROM selfprefix WHERE user_id = {}".format(ctx.author.id))
          return await ctx.send_success("Your **selfprefix** has been **removed**")
        elif check is None: return await ctx.send_error("You do not have a **selfprefix**")   
      else:    
        result = await self.bot.db.fetchrow("SELECT * FROM selfprefix WHERE user_id = {}".format(ctx.author.id)) 
        if result is not None: await self.bot.db.execute("UPDATE selfprefix SET prefix = $1 WHERE user_id = $2", prefix, ctx.author.id)
        elif result is None: await self.bot.db.execute('INSERT INTO selfprefix VALUES ($1, $2)', ctx.author.id, prefix)
        return await ctx.send_success(f"Your **selfprefix** is now `{prefix}`") 
      
   @hybrid_command(description="see all roles in the server",)
   async def roles(self, ctx: Context):
        i = 0
        k = 1
        l = 0
        mes = ""
        number = []
        messages = []

        sorted_roles = sorted(ctx.guild.roles, key=lambda x: x.position, reverse=True)

        for role in sorted_roles:
            mes = f"{mes}`{k}` {role.mention} - <t:{int(role.created_at.timestamp())}:R> ({len(role.members)} Members)\n"
            k += 1
            l += 1
            if l == 10:
                messages.append(mes)
                number.append(discord.Embed(color=self.bot.color, title=f"Roles ({len(ctx.guild.roles)})", description=messages[i]))
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = discord.Embed(color=self.bot.color, title=f"Roles ({len(ctx.guild.roles)})", description=messages[i])
        number.append(embed)
        await ctx.paginator(number)

   @hybrid_command(description="see all channels in the server")
   async def channels(self, ctx: Context):
    i = 0
    k = 1
    l = 0
    mes = ""
    number = []
    messages = []

    filtered_channels = [channel for channel in ctx.guild.channels if isinstance(channel, (discord.TextChannel, discord.VoiceChannel))]

    sorted_channels = sorted(filtered_channels, key=lambda x: x.position, reverse=False)

    for channel in sorted_channels:
        if isinstance(channel, discord.TextChannel):
            channel_type = "Text"
        elif isinstance(channel, discord.VoiceChannel):
            channel_type = "Voice"

        category_name = ""
        if channel.category:
            category_name = f" (category: **{channel.category.name}**)"
        
        mes = f"{mes}`{k}` {channel.mention} {category_name}\n"
        k += 1
        l += 1
        if l == 10:
            messages.append(mes)
            number.append(discord.Embed(color=self.bot.color, title=f"Channels ({len(filtered_channels)})", description=messages[i]))
            i += 1
            mes = ""
            l = 0

    messages.append(mes)
    embed = discord.Embed(color=self.bot.color, title=f"Channels ({len(filtered_channels)})", description=messages[i])
    number.append(embed)
    await ctx.paginator(number)
      
async def setup(bot) -> None:
    await bot.add_cog(info(bot))      
