from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check
import datetime, discord, humanize, os, arrow, uwuipy, humanfriendly, asyncio 
from discord import Embed, File, TextChannel, Member, User, Role 
from deep_translator import GoogleTranslator
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from discord.ext import commands 
import aiohttp
from discord.ui import Button, View
from discord.ext import tasks
from aiohttp import ClientResponse
import typing
import sys
from tools.checks import Perms
from aiogtts import aiogTTS
from random import choice
from io import BytesIO
import requests
import random
from typing import Optional, Tuple, Union

def is_afk():
  async def predicate(ctx: commands.Context):
    check = await ctx.bot.db.fetchrow("SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    return check is None 
  return check(predicate)

DISCORD_API_LINK = "https://discord.com/api/invite/"

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def human_format(number):
    if number > 999: return humanize.naturalsize(number, False, True) 
    return number 
  
class Utility(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.hs = {
			"aquarius": {
				"name": "Aquarius",
				"emoji": ":aquarius:",
				"date_range": "Jan 20 - Feb 18",
			},
			"pisces": {
				"name": "Pisces",
				"emoji": ":pisces:",
				"date_range": "Feb 19 - Mar 20",
			},
			"aries": {
				"name": "Aries",
				"emoji": ":aries:",
				"date_range": "Mar 21 - Apr 19",
			},
			"taurus": {
				"name": "Taurus",
				"emoji": ":taurus:",
				"date_range": "Apr 20 - May 20",
			},
			"gemini": {
				"name": "Gemini",
				"emoji": ":gemini:",
				"date_range": "May 21 - Jun 20",
			},
			"cancer": {
				"name": "Cancer",
				"emoji": ":cancer:",
				"date_range": "Jun 21 - Jul 22",
			},
			"leo": {
				"name": "Leo",
				"emoji": ":leo:",
				"date_range": "Jul 23 - Aug 22",
			},
			"virgo": {
				"name": "Virgo",
				"emoji": ":virgo:",
				"date_range": "Aug 23 - Sep 22",
			},
			"libra": {
				"name": "Libra",
				"emoji": ":libra:",
				"date_range": "Sep 23 - Oct 22",
			},
			"scorpio": {
				"name": "Scorpio",
				"emoji": ":scorpius:",
				"date_range": "Oct 23 - Nov 21",
			},
			"sagittarius": {
				"name": "Sagittarius",
				"emoji": ":sagittarius:",
				"date_range": "Nov 22 - Dec 21",
			},
			"capricorn": {
				"name": "Capricorn",
				"emoji": ":capricorn:",
				"date_range": "Dec 22 - Jan 19",
			},
		}       

    async def bday_send(self, ctx: Context, message: str) -> discord.Message: 
      return await ctx.reply(embed=discord.Embed(color=self.bot.color, description=f"{self.cake} {ctx.author.mention}: {message}"))
    
    async def do_again(self, url: str):
     re = await self.make_request(url)
     if re['status'] == "converting": return await self.do_again(url)
     elif re['status'] == "failed": return None
     else: return tuple([re['url'], re['filename']]) 

    async def make_request(self, url: str, action: str="get", params: dict=None): 
       r = await self.bot.session.get(url, params=params)
       if action == "get": return await r.json()
       if action == "read": return await r.read()
    
    @hybrid_command(description="Clear **ALL** snipe data", help="utility", brief="manage messages", aliases=['cs'])
    @Perms.get_perms("manage_messages")
    async def clearsnipes(self, ctx: Context): 
      lis = ["snipe", "reactionsnipe", "editsnipe"]
      for l in lis: await self.bot.db.execute(f"DELETE FROM {l} WHERE guild_id = $1", ctx.guild.id)
      return await ctx.send_success("**All** snipes have been **cleared**") 

    @hybrid_command(description="Check if I saw a member", help="utility", usage="[member]")
    async def seen(self, ctx, *, member: Member):
        check = await self.bot.db.fetchrow("SELECT * FROM seen WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id))
        if check is None: return await ctx.send_warning( f"I didn't see **{member}**, maybe my glasses were foggy. ")
        ts = check['time']
        await ctx.reply(embed=Embed(color=self.bot.color, description="{}: **{}** was last seen <t:{}:R>".format(ctx.author.mention, member, ts)))   

    @hybrid_command(help="utility", description="Let everyone know you are away", usage="<reason>")
    async def afk(self, ctx: Context, *, reason="AFK"):      
       ts = int(datetime.datetime.now().timestamp())   
       result = await self.bot.db.fetchrow("SELECT * FROM afk WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, ctx.author.id)) 
       if result is None:
        await self.bot.db.execute("INSERT INTO afk VALUES ($1,$2,$3,$4)", ctx.guild.id, ctx.author.id, reason, ts)
        await ctx.send_success(f"You're now AFK with the status: **{reason}**")

    @hybrid_command(aliases=["es"], description="Snipe the most recent edited message", help="utility", usage="<number>")
    async def editsnipe(self, ctx: Context, number: int=1): 
     results = await self.bot.db.fetch("SELECT * FROM editsnipe WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, ctx.channel.id)
     if len(results) == 0: return await ctx.send_warning( "There are **no** edit snipes in this **channel**")
     if number > len(results): return await ctx.send_warning( f"snipe limit is **{len(results)}**")
     sniped = results[::-1][number-1]
     embed = Embed(color=self.bot.color)
     embed.set_author(name=sniped['author_name'], icon_url=sniped["author_avatar"])
     embed.add_field(name="before", value=sniped['before_content'])
     embed.add_field(name="after", value=sniped['after_content'])
     embed.set_footer(text=f"{number}/{len(results)}")
     await ctx.reply(embed=embed)

    @hybrid_command(aliases=["rs"], description="Snipe the most recent removed reaction", help="utility", usage="number")
    async def reactionsnipe(self, ctx: Context, number: int=1):
     results = await self.bot.db.fetch("SELECT * FROM reactionsnipe WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, ctx.channel.id)
     if len(results) == 0: return await ctx.send_warning( "There are **no** reaction snipes in this **channel**")
     if number > len(results): return await ctx.send_warning( f"snipe limit is **{len(results)}**") 
     sniped = results[::-1][number-1]
     message = await ctx.channel.fetch_message(sniped['message_id'])
     embed = Embed(color=self.bot.color, description=f"{sniped['emoji_name']} was removed from [this message]({message.jump_url if message else 'https://lunebot.wtf'})")
     embed.set_author(name=sniped['author_name'], icon_url=sniped['author_avatar'])
     embed.set_image(url=sniped['emoji_url'])
     embed.set_footer(text=f"{number}/{len(results)}")
     await ctx.reply(embed=embed)

    @hybrid_command(aliases=["s"], description="Snipe the latest deleted message", usage="<number>", help="utility")
    async def snipe(self, ctx: Context, *, number: int=1):
        check = await self.bot.db.fetch("SELECT * FROM snipe WHERE guild_id = {} AND channel_id = {}".format(ctx.guild.id, ctx.channel.id))
        if len(check) == 0: return await ctx.send_warning( "There are **no** deleted messages in this channel") 
        if number > len(check): return await ctx.send_warning( f"snipe limit is **{len(check)}**".capitalize()) 
        sniped = check[::-1][number-1]
        em = Embed(color=self.bot.color, description=sniped['content'], timestamp=sniped['time'])
        em.set_author(name=sniped['author'], icon_url=sniped['avatar']) 
        em.set_footer(text="{}/{}".format(number, len(check)))
        if sniped['attachment'] != "none":
         if ".mp4" in sniped['attachment'] or ".mov" in sniped['attachment']:
          url = sniped['attachment']
          r = await self.bot.session.read(url)
          bytes_io = BytesIO(r)
          file = File(fp=bytes_io, filename="video.mp4")
          return await ctx.reply(embed=em, file=file)
         else:
           try: em.set_image(url=sniped['attachment'])
           except: pass 
        return await ctx.reply(embed=em)
    
    @hybrid_command(aliases=["mc"], description="View the current membercount", help="utility")
    async def membercount(self, ctx: Context):
      b=len(set(b for b in ctx.guild.members if b.bot))
      h=len(set(b for b in ctx.guild.members if not b.bot))
      embed = Embed(color=self.bot.color)
      embed.set_author(name=f"{ctx.guild.name}'s member count", icon_url=ctx.guild.icon)
      embed.add_field(name=f"Members", value=h)
      embed.add_field(name="Total", value=ctx.guild.member_count) 
      embed.add_field(name="Bots", value=b)
      await ctx.reply(embed=embed)

    @hybrid_command(description="See user's avatar", help="utility", usage="<user>", aliases=["av"])
    async def avatar(self, ctx: Context, *, member: Union[Member, User] = None):
        if member is None:
            member = ctx.author

        if isinstance(member, Member):
            embed = Embed(color=self.bot.color, title=f"{member.name}'s avatar", url=member.avatar.url)
            embed.set_image(url=member.avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(member, User):
            embed = Embed(color=self.bot.color, title=f"{member.name}'s avatar", url=member.avatar.url)
            embed.set_image(url=member.avatar.url)
            await ctx.reply(embed=embed)
    
    @hybrid_command(description="See user's avatar", help="utility", usage="<user>", aliases=["sav"])
    async def serveravatar(self, ctx: Context, *, member: Union[Member, User]=None):
        if member is None:
            member = ctx.author

        if isinstance(member, Member) and member.guild_avatar:
            embed = Embed(color=self.bot.color, title=f"{member.name}'s server avatar", url=member.guild_avatar.url)
            embed.set_image(url=member.guild_avatar.url)
            await ctx.reply(embed=embed)
        elif isinstance(member, User) and member.avatar:
            embed = Embed(color=self.bot.color, title=f"{member.name}'s server avatar", url=member.avatar.url)
            embed.set_image(url=member.avatar.url)
            await ctx.reply(embed=embed)
        else:
            await ctx.send_warning("No **server avatar** found")
    
    @command(description="See role information", usage="[role]", help="utility", aliases=["ri"])
    async def roleinfo(self, ctx: Context, *, role: Union[Role, str]): 
      if isinstance(role, str): 
        role = ctx.find_role(role)
        if role is None: return await ctx.send_warning( "Unable to **find** that **role**")

      perms = ", ".join([str(p[0]) for p in role.permissions if bool(p[1]) is True]) if role.permissions else "None"
      embed = Embed(color=role.color, title=f"@{role.name}", description="`{}`".format(role.id), timestamp=role.created_at)
      embed.set_thumbnail(url=role.display_icon if not isinstance(role.display_icon, str) else None)
      embed.add_field(name="Members", value=str(len(role.members)))
      embed.add_field(name="Permissions", value=f"```{perms}```", inline=False)
      await ctx.reply(embed=embed)
       
    @command(description="See all members in a role", help="utility", usage="[role]")
    async def inrole(self, ctx: Context, *, role: Union[Role, str]):
            if isinstance(role, str): 
              role = ctx.find_role(role)
              if role is None: return await ctx.send_warning( "Unable to **find** that **role**")

            if len(role.members) == 0: return await ctx.send_error("**Nobody** has **this role**") 
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in role.members:
              mes = f"{mes}`{k}` {member} - ({member.id})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=self.bot.color, title=f"Members in {role.name} [{len(role.members)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=self.bot.color, title=f"Members in {role.name} [{len(role.members)}]", description=messages[i])
            number.append(embed)
            await ctx.paginator( number)
    
    @command(description="See all members joined today", help="utility")
    async def joins(self, ctx: Context): 
      members = [m for m in ctx.guild.members if (datetime.datetime.now() - m.joined_at.replace(tzinfo=None)).total_seconds() < 3600*24]      
      if len(members) == 0: return await ctx.send_error("**Nobody** joined **today**")
      members = sorted(members, key=lambda m: m.joined_at)
      i=0
      k=1
      l=0
      mes = ""
      number = []
      messages = []
      for member in members[::-1]: 
        mes = f"{mes}`{k}` {member} - {discord.utils.format_dt(member.joined_at, style='R')}\n"
        k+=1
        l+=1
        if l == 10:
         messages.append(mes)
         number.append(Embed(color=self.bot.color, title=f"Joined Today [{len(members)}]", description=messages[i]))
         i+=1
         mes = ""
         l=0
    
      messages.append(mes)
      embed = Embed(color=self.bot.color, title=f"Joined Today [{len(members)}]", description=messages[i])
      number.append(embed)
      await ctx.paginator( number) 

    @command(description="See all muted mebmers", help="utility")
    async def muted(self, ctx: Context): 
            members = [m for m in ctx.guild.members if m.is_timed_out()]
            if len(members) == 0: return await ctx.send_error("**Nobody** is **muted** in this **server**")
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in members: 
              mes = f"{mes}`{k}` {member} - <t:{int(member.timed_out_until.timestamp())}:R> \n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=self.bot.color, title=f"{ctx.guild.name} Muted Members [{len(members)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=self.bot.color, title=f"{ctx.guild.name} Muted Members [{len(members)}]", description=messages[i])
            number.append(embed)
            await ctx.paginator( number)     
    
    @command(description="See all banned users", help="utility")
    async def bans(self, ctx: Context): 
     banned = [m async for m in ctx.guild.bans()]
     if len(banned) == 0: return await ctx.send_warning( "**Nobody** is **banned** in this **server**")  
     i=0
     k=1
     l=0
     mes = ""
     number = []
     messages = []
     for m in banned: 
       mes = f"{mes}`{k}` **{m.user}** - `{m.reason or 'No reason provided'}` \n"
       k+=1
       l+=1
       if l == 10:
        messages.append(mes)
        number.append(Embed(color=self.bot.color, title=f"Banned ({len(banned)})", description=messages[i]))
        i+=1
        mes = ""
        l=0
    
     messages.append(mes)
     embed = Embed(color=self.bot.color, title=f"Banned ({len(banned)})", description=messages[i])
     number.append(embed)
     await ctx.paginator( number) 

    @group(invoke_without_command=True, description="See people who are boosting the server", help="utility")
    async def boosters(self, ctx: Context):
            if not ctx.guild.premium_subscriber_role or len(ctx.guild.premium_subscriber_role.members) == 0: return await ctx.send_warning( "this server has **no** boosts".capitalize())
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for member in ctx.guild.premium_subscriber_role.members: 
              mes = f"{mes}`{k}` {member} - <t:{int(member.premium_since.timestamp())}:R> \n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=self.bot.color, title=f"Boosters [{len(ctx.guild.premium_subscriber_role.members)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=self.bot.color, title=f"Boosters [{len(ctx.guild.premium_subscriber_role.members)}]", description=messages[i])
            number.append(embed)
            await ctx.paginator( number) 
    
    @boosters.command(name="lost", description="Show boosters lost", help="utility")
    async def boosters_lost(self, ctx: Context): 
      results = await self.bot.db.fetch("SELECT * FROM boosterslost WHERE guild_id = $1", ctx.guild.id)
      if len(results) == 0: return await ctx.send_warning( "TThere are **no** lost boosters :tada:")
      i=0
      k=1
      l=0
      mes = ""
      number = []
      messages = []
      for result in results[::-1]: 
          mes = f"{mes}`{k}` <@!{int(result['user_id'])}> - <t:{result['time']}:R> \n"
          k+=1
          l+=1
          if l == 10:
           messages.append(mes)
           number.append(Embed(color=self.bot.color, title=f"Boosters Lost [{len(results)}]", description=messages[i]))
           i+=1
           mes = ""
           l=0
    
      messages.append(mes)
      embed = Embed(color=self.bot.color, title=f"Boosters Lost [{len(results)}]", description=messages[i])
      number.append(embed)
      await ctx.paginator( number) 

    @command(description="See all roles in the server", help="utility")
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
                number.append(Embed(color=self.bot.color, title=f"Roles [{len(ctx.guild.roles)}]", description=messages[i]))
                i += 1
                mes = ""
                l = 0

        messages.append(mes)
        embed = Embed(color=self.bot.color, title=f"Roles [{len(ctx.guild.roles)}]", description=messages[i])
        number.append(embed)
        await ctx.paginator(number)

    @command(description="See all bots in the server", help="utility")
    async def bots(self, ctx: Context):
            i=0
            k=1
            l=0
            b=len(set(b for b in ctx.guild.members if b.bot))
            mes = ""
            number = []
            messages = []
            for member in ctx.guild.members:
             if member.bot:   
              mes = f"{mes}`{k}` {member} - ({member.id})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=self.bot.color, title=f"Bots [{b}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            embed = Embed(color=self.bot.color, title=f"{ctx.guild.name} Bots [{b}]", description=messages[i])
            number.append(embed)
            await ctx.paginator( number)
    

    @hybrid_command(description="Show user information", help="utility", usage="<user>", aliases=["whois", "ui", "user"])
    async def userinfo(self, ctx: Context, *, member: Union[Member, User]=None):
     await ctx.typing()
     if member is None: member = ctx.author           
     user = await self.bot.fetch_user(member.id)

     def vc(mem: Member):
        if mem.voice: 
          channelname = mem.voice.channel.name 
          deaf = "<:deafen:1180540803072925696>" if mem.voice.self_deaf or mem.voice.deaf else "<:undeafen:1180541568608911480>"
          mute = "<:muted:1180540840540639232>" if mem.voice.self_mute or mem.voice.mute else "<:unmuted:1180541565802922085>"
          stream = "<:pc:1180541173685821580>" if mem.voice.self_stream else ""
          video = "<:videocamera:1180541176651194489>" if mem.voice.self_video else ""
          channelmembers = f"with {len(mem.voice.channel.members)-1} Other member{'s' if len(mem.voice.channel.members) > 2 else ''}" if len(mem.voice.channel.members) > 1 else ""
          return f"{deaf} {mute} {stream} {video} **In voice channel** {channelname} {channelmembers}"
        return ""  

     e = Embed(color=self.bot.color, title=str(user))        
     if isinstance(member, Member): 
      e.description = f""
      members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
      ordinal = self.bot.ordinal(int(members.index(member)+1))    
      e.set_author(name=f"{member}", icon_url=member.display_avatar.url)
      e.add_field(name="Dates", value=f"**Joined:** {self.bot.convert_datetime(member.joined_at)}\n**Created:** {self.bot.convert_datetime(member.created_at)}\n{f'**Boosted:** {self.bot.convert_datetime(member.premium_since)}' if self.bot.convert_datetime(member.premium_since) else ''}", inline=False)     
      roles = member.roles[1:][::-1]
      if len(roles) > 0: e.add_field(name=f"Roles ({len(roles)})", value=' '.join([r.mention for r in roles]) if len(roles) < 5 else ' '.join([r.mention for r in roles[:4]]) + f" - {len(roles)-4} more")
     elif isinstance(member, User): e.add_field(name="Dates", value=f"**Created:** {self.bot.convert_datetime(member.created_at)}", inline=False)     
     e.set_thumbnail(url=member.display_avatar.url)
     try: e.set_footer(text='ID: ' + str(member.id) + f" | {len(member.mutual_guilds)} mutual server(s)")
     except: e.set_footer(text='ID: ' + str(member.id)) 
     await ctx.reply(embed=e)
    
    @command(help="utility", description="Get the servers banner", aliases=["guildbanner"])
    async def serverbanner(self, ctx: Context): 
      return await ctx.invoke(self.bot.get_command("server banner"))
    
    @command(help="utility", description="Get the servers icon", aliases=["guildicon", "guildavatar"])
    async def servericon(self, ctx: Context): 
      return await ctx.invoke(self.bot.get_command("server icon"))

    @command(help="utility", description="Get the servers splash", aliases=["guildsplash"])
    async def serversplash(self, ctx: Context): 
      return await ctx.invoke(self.bot.get_command("server splash"))  

    @commands.hybrid_command(aliases=['si'])
    async def serverinfo(self, ctx: Context, invite: discord.Invite=None): 
        """
        Get the information about a server
        """
    
        if invite:
          embed = discord.Embed(
        color=self.bot.color,
        title=f"{invite.code}"
      )\

          if invite.guild: 
           embed.description = invite.guild.description or ''
           embed.set_thumbnail(
        url=invite.guild.icon
      )\
           .add_field(
        name="Information", 
        value=f"**ID:** `{invite.guild.id}`\n**Members:** {invite.approximate_member_count:,}\n**Created**: {discord.utils.format_dt(invite.created_at, style='R') if invite.created_at else 'N/A'}"
      )
       
        else:
          servers = sorted(self.bot.guilds, key=lambda g: g.member_count, reverse=True)
          embed = discord.Embed(
        color=self.bot.color, 
        title=ctx.guild.name, 
        description=f"{ctx.guild.description or ''}"
      )\
          .set_author(
        name=f"{ctx.guild.name} ({ctx.guild.id})", 
        icon_url=ctx.guild.icon
      )\
          .set_thumbnail(
        url=ctx.guild.icon
      )\
      .add_field(
         name="Information",
         value=f">>> **Owner:** {ctx.guild.owner}\n**Vanity:** {ctx.guild.vanity_url_code or 'N/A'}\n**Created:** {discord.utils.format_dt(ctx.guild.created_at, style='D')}"
      )\
          .add_field(
        name="Statistics", 
        value=f">>> **Members:** {ctx.guild.member_count:,}\n**Boosts:** {ctx.guild.premium_subscription_count:,} (`Level {ctx.guild.premium_tier}`)\n**Roles:** {len(ctx.guild.roles):,}"
      )\
    
        await ctx.send(embed=embed)
   
    @command(description="Gets the banner of a server", help="utility", usage="[invite code]")
    async def sbanner(self, ctx, *, link: str = None):
        if link:
            try:
                invite = await self.bot.fetch_invite(link)
            except discord.errors.NotFound:
                invite = None

            if invite:
                guild = invite.guild
            else:
                return await ctx.send_warning("That server **does** not **exist!**")
        else:
            guild = ctx.guild

        if guild.banner:
            embed = discord.Embed(color=self.bot.color, title=f"{guild.name}'s banner")
            embed.set_image(url=guild.banner.url)
            await ctx.reply(embed=embed)
        else:
            await ctx.send_warning("This server has no **banner**")


    @command(description="Gets the splash of a server", help="utility", usage="[invite code]")
    async def splash(self, ctx, *, link: str = None):
        if link:
            try:
                invite = await self.bot.fetch_invite(link)
            except discord.errors.NotFound:
                invite = None

            if invite:
                guild = invite.guild
            else:
                return await ctx.send_warning("That server **does** not **exist!**")
        else:
            guild = ctx.guild

        if guild.splash:
            format = "png" 
            embed = discord.Embed(color=self.bot.color, title=f"{guild.name}'s splash")
            embed.set_image(url=guild.splash.url)
            await ctx.reply(embed=embed)
        else:
            await ctx.send_warning("This server has no **splash image**")

    @command(description="Gets the icon of a server", help="utility", usage="[invite code]")
    async def sicon(self, ctx, *, link: str = None):
        if link:
            try:
                invite = await self.bot.fetch_invite(link)
            except discord.errors.NotFound:
                invite = None

            if invite:
                guild = invite.guild
            else:
                return await ctx.send_warning("That server **does** not **exist!**")

        else:
            guild = ctx.guild

        format = "gif" if guild.icon.is_animated() else "png"
        embed = discord.Embed(color=self.bot.color, title=f"{guild.name}'s icon")
        embed.set_image(url=guild.icon.url)
        await ctx.reply(embed=embed)

    @hybrid_command(aliases=["firstmsg"], description="Grab the first message in a channel", help="utility", usage="<channel>")
    async def firstmessage(self, ctx: Context, *, channel: TextChannel=None):
     channel = channel or ctx.channel 
     messages = [mes async for mes in channel.history(oldest_first=True, limit=1)]
     message = messages[0]
     embed = Embed(color=self.bot.color, title="First message in #{}".format(channel.name), description=message.content, timestamp=message.created_at)
     view = View()
     view.add_item(Button(label="Message", url=message.jump_url))
     await ctx.reply(embed=embed, view=view)  
    
    @hybrid_command(
        name="banner",
        usage="<user>",
        aliases=["ub"],
    )
    async def banner(self, ctx: Context, *, user: Member | User = None):
        """View a user's banner"""

        user = user or ctx.author
        user = await self.bot.fetch_user(user.id)

        if user.banner:
            url = user.banner.url
            description = f"{user.name}'s banner"
        else:
            url = f"https://singlecolorimage.com/get/{user.accent_color or discord.Color(0).value:06x}/400x100"
            description = "You have no **banner**" if user == ctx.author else f"{user.mention} has no **banner**"

        embed = discord.Embed(url=url, title=description, color=self.bot.color)
        embed.set_image(url=url)

        if "You have no banner" in description or f"{user.mention} has no **banner**" in description:
            await ctx.send_warning(description)
        else:
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))   
