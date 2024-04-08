import discord, datetime, humanfriendly, json 
from discord.ext import commands 
from typing import Literal, Optional, Union
from tools.checks import Mod
from cogs.config import InvokeClass
from tools.utils import EmbedBuilder, GoodRole, NoStaff
import asyncio
from tools.checks import Perms
import contextlib

class ClearMod(discord.ui.View): 
  def __init__(self, ctx: commands.Context): 
   super().__init__()
   self.ctx = ctx
   self.status = False

  @discord.ui.button(emoji="✅")
  async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
   if interaction.user.id != self.ctx.author.id: return await interaction.client.ext.send_warning(interaction, "You're **not** the author")
   check = await interaction.client.db.fetchrow("SELECT * FROM mod WHERE guild_id = $1", interaction.guild.id)     
   channelid = check["channel_id"]
   roleid = check["role_id"]
   logsid = check["jail_id"]
   channel = interaction.guild.get_channel(channelid)
   role = interaction.guild.get_role(roleid)
   logs = interaction.guild.get_channel(logsid)
   try: await channel.delete()
   except: pass 
   try: await role.delete()
   except: pass
   try: await logs.delete()
   except: pass 
   await interaction.client.db.execute("DELETE FROM mod WHERE guild_id = $1", interaction.guild.id)
   self.status = True
   return await interaction.response.edit_message(view=None, embed=discord.Embed(color=interaction.client.color, description=f"{interaction.client.yes} {interaction.user.mention}: Disabled jail"))
  
  @discord.ui.button(emoji="❌")
  async def no(self, interaction: discord.Interaction, button: discord.ui.Button): 
    if interaction.user.id != self.ctx.author.id: return await interaction.client.ext.send_warning(interaction, "You're **not** the author")
    await interaction.response.edit_message(embed=discord.Embed(color=interaction.client.color, description="**Aborted**"), view=None)
    self.status = True

  async def on_timeout(self) -> None:
       if self.status == False: 
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self) 

class ModConfig:
 
 async def sendlogs(bot: commands.AutoShardedBot, action: str, author: discord.Member, victim: Union[discord.Member, discord.User], reason: str): 
  check = await bot.db.fetchrow("SELECT channel_id FROM mod WHERE guild_id = $1", author.guild.id)
  if check: 
   res = await bot.db.fetchrow("SELECT count FROM cases WHERE guild_id = $1", author.guild.id)
   case = int(res['count']) + 1 
   await bot.db.execute("UPDATE cases SET count = $1 WHERE guild_id = $2", case, author.guild.id)
   embed = discord.Embed(color=bot.color, title=f"Case #{case}", timestamp=datetime.datetime.now())   
   embed.add_field(name="User", value=f"{victim}\n({victim.id})")
   embed.add_field(name="Moderator", value=f"{author}\n({author.id})")
   embed.add_field(name="Reason", value=reason, inline=False)
   try: await author.guild.get_channel(int(check['channel_id'])).send(embed=embed)
   except: pass
 
 async def send_dm(ctx: commands.Context, member: discord.Member, action: str, reason: str): 
  results = await ctx.bot.db.fetchrow("SELECT * FROM authorize WHERE guild_id = $1", ctx.guild.id)
  if results or ctx.guild.id in ctx.bot.main_guilds: 
   res = await ctx.bot.db.fetchrow("SELECT embed FROM dm WHERE guild_id = $1 AND command = $2", ctx.guild.id, ctx.command.name)   
   if res:
    name = res[0]
    if name.lower() == "off": return
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label=f"sent from {ctx.guild.name}", disabled=True))
    try: 
     x = await EmbedBuilder.to_object(EmbedBuilder.embed_replacement(ctx.author, InvokeClass.invoke_replacement(member, name)).replace("{reason}", reason))
     try: return await member.send(content=x[0], embed=x[1], view=view)
     except: pass
    except Exception as e:
      print(e) 
      try: return await member.send(content=InvokeClass.invoke_replacement(member, EmbedBuilder.embed_replacement(ctx.author, name)).replace('{reason}', reason), embed=None, view=view)    
      except: pass   
   else: 
    embed = discord.Embed(color=ctx.bot.color, title=f"{action}")
    embed.add_field(
       name=f"You have been {action} in",
       value=ctx.guild.name,
       inline=True
    )\
    .add_field(
       name="Reason",
       value={f'Reason: {reason}' if reason != 'No reason provided' else ''},
       inline=True
    )
    try: await member.send(embed=embed)
    except: pass    
  else:
    embed = discord.Embed(color=ctx.bot.color, title=f"{action}")
    embed.add_field(
       name=f"You have been {action} in",
       value=ctx.guild.name,
       inline=True
    )\
    .add_field(
       name="Reason",
       value={f'Reason: {reason}' if reason != 'No reason provided' else ''},
       inline=True
    )
    try: await member.send(embed=embed)
    except: pass

class Moderation(commands.Cog): 
  def __init__(self, bot: commands.AutoShardedBot): 
    self.bot = bot
    self.pretty_actions: dict = {
            "guild_update": "updated server",
            "channel_create": "created channel",
            "channel_update": "updated channel",
            "channel_delete": "deleted channel",
            "overwrite_create": "created channel permission",
            "overwrite_update": "updated channel permission",
            "overwrite_delete": "deleted channel permission",
            "kick": "kicked member",
            "member_prune": "pruned members",
            "ban": "banned member",
            "unban": "unbanned member",
            "member_update": "updated member",
            "member_role_update": "updated member roles",
            "member_disconnect": "disconnected member",
            "bot_add": "added bot",
            "role_create": "created role",
            "role_update": "updated role",
            "role_delete": "deleted role",
            "invite_create": "created invite",
            "invite_update": "updated invite",
            "invite_delete": "deleted invite",
            "webhook_create": "created webhook",
            "webhook_update": "updated webhook",
            "webhook_delete": "deleted webhook",
            "emoji_create": "created emoji",
            "emoji_update": "updated emoji",
            "emoji_delete": "deleted emoji",
            "message_delete": "deleted message by",
            "message_bulk_delete": "bulk deleted messages in",
            "message_pin": "pinned message by",
            "message_unpin": "unpinned message by",
            "integration_create": "created integration",
            "integration_update": "updated integration",
            "integration_delete": "deleted integration",
            "sticker_create": "created sticker",
            "sticker_update": "updated sticker",
            "sticker_delete": "deleted sticker",
            "thread_create": "created thread",
            "thread_update": "updated thread",
            "thread_delete": "deleted thread",
        }

  
  @commands.Cog.listener('on_member_remove')
  async def on_restore(self, member: discord.Member):
      check = await self.bot.db.fetchrow("SELECT * FROM nodata WHERE user_id = $1 AND state = $2", member.id, "false")
      if check: return
      list = [role.id for role in member.roles if role.is_assignable()]
      sql_as_text = json.dumps(list)
      ch = await self.bot.db.fetchrow("SELECT * FROM restore WHERE user_id = {} AND guild_id = {}".format(member.id, member.guild.id))   
      if ch: return await self.bot.db.execute("UPDATE restore SET roles = $1 WHERE guild_id = $2 AND user_id = $3", sql_as_text, member.guild.id, member.id)
      return await self.bot.db.execute("INSERT INTO restore VALUES ($1,$2,$3)", member.guild.id, member.id, sql_as_text)
   
  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
      check = await self.bot.db.fetchrow("SELECT * FROM mod WHERE guild_id = {}".format(channel.guild.id))
      if check: await channel.set_permissions(channel.guild.get_role(int(check['role_id'])), view_channel=False, reason="Setting permissions for jail")

  @commands.command(description="Disable moderation in your server", help="moderation")
  @Perms.get_perms("administrator")
  async def removejail(self, ctx: commands.Context): 
   check = await self.bot.db.fetchrow("SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id)
   if not check: return await ctx.send_warning( "The **jail module** is __not__ **setup**") 
   view = ClearMod(ctx)
   view.message = await ctx.reply(view=view, embed=discord.Embed(color=self.bot.color, description=f"{ctx.author.mention} Are you **sure** you want to **disable** jail?")) 

  @commands.command(description="Strip roles with __dangerous__ permissions from a user", brief="manage roles", usage="[member]", help="moderation")
  @Perms.get_perms("manage_roles")
  async def strip(self, ctx: commands.Context, *, member: NoStaff): 
   roles = [
    role for role in member.roles
    if role.is_assignable()
    and not self.bot.is_dangerous(role)
    or role == ctx.guild.premium_subscriber_role
   ]

   await member.edit(roles=roles, reason=f"member stripped by {ctx.author}")
   return await ctx.send_success(f"Stripped {member.mention}'s roles")


  @commands.command(description="Enable jail in your server", help="moderation")
  @Perms.get_perms("administrator")
  async def setupjail(self, ctx: commands.Context): 
    
   check = await self.bot.db.fetchrow("SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id)
   if check: return await ctx.send_warning( "The **jail module** is **already setup**")
   await ctx.typing()
   await ctx.send(embed = discord.Embed(description=f"> {ctx.author.mention}: Setting up channel permissions for **jail**, please wait.", color=self.bot.color))
   role = await ctx.guild.create_role(name="lune-jail")
   for channel in ctx.guild.channels: await channel.set_permissions(role, view_channel=False)
   overwrite = {role: discord.PermissionOverwrite(view_channel=True), ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
   over = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
   category = await ctx.guild.create_category(name="lune mod", overwrites=over)
   text = await ctx.guild.create_text_channel(name="mod-logs", overwrites=over, category=category)
   jai = await ctx.guild.create_text_channel(name="jail", overwrites=overwrite, category=category)
   await self.bot.db.execute("INSERT INTO mod VALUES ($1,$2,$3,$4)", ctx.guild.id, text.id, jai.id, role.id)
   await self.bot.db.execute("INSERT INTO cases VALUES ($1,$2)", ctx.guild.id, 0)
   return await ctx.message.edit("The **jail module** has been setup.") 
  
  @commands.command(description="HardBan someone from the server", usage="[user]")
  @Perms.get_perms("administrator")
  async def hardban(self, ctx: commands.Context, *, member: Union[discord.Member, discord.User]): 
    if isinstance(member, discord.Member):
      if member == ctx.message.author: return await ctx.send_warning("You cannot hardban **yourself**")
      if member.id == self.bot.user.id: return await ctx.send_warning("You cannot hardban **me** ;p")
      if await Mod.check_hieracy(ctx, member):   
       che = await self.bot.db.fetchrow("SELECT * FROM hardban WHERE guild_id = {} AND banned = {}".format(ctx.guild.id, member.id))
       if che is not None: return await ctx.send_success(f"**{member}** has been hardbanned by **{await self.bot.fetch_user(che['author'])}**")
       await ctx.guild.ban(member, reason="hardbanned by {}".format(ctx.author))
       await self.bot.db.execute("INSERT INTO hardban VALUES ($1,$2,$3)", ctx.guild.id, member.id, ctx.author.id)

  @commands.command(description="Un-HardBan someone from the server", usage="[user]")
  @Perms.get_perms("administrator")
  async def hardunban(self, ctx: commands.Context, *, member: discord.User):     
      che = await self.bot.db.fetchrow("SELECT * FROM hardban WHERE guild_id = {} AND banned = {}".format(ctx.guild.id, member.id))      
      if che is None: return await ctx.send_warning(f"{member} is **not** hardbanned") 
      await self.bot.db.execute("DELETE FROM hardban WHERE guild_id = {} AND banned = {}".format(ctx.guild.id, member.id))
      await ctx.guild.unban(member, reason="unhardbanned by {}".format(ctx.author)) 
      return await ctx.send_success(f"{member} has been unbanned")   

  @commands.command(description="Delete & Clone a channel", help="moderation", brief="server owner")
  @Perms.get_perms("administrator")
  async def nuke(self, ctx: commands.Context): 
   embed = discord.Embed(color=self.bot.color, description=f"Are you sure you want to **nuke** {ctx.channel.mention}?")
   yes = discord.ui.Button(label="Yes")
   no = discord.ui.Button(label="No")

   async def yes_callback(interaction: discord.Interaction): 
    if not interaction.user == ctx.author: return await self.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True)
    c = await interaction.channel.clone()
    await c.edit(position=ctx.channel.position)
    await ctx.channel.delete()
    await c.send("first")
   
   async def no_callback(interaction: discord.Interaction): 
    if not interaction.user == ctx.author: return await self.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True)
    await interaction.response.edit_message(embed=discord.Embed(color=self.bot.color, description="**Aborted**"), view=None)
   
   yes.callback = yes_callback
   no.callback = no_callback 
   view = discord.ui.View()
   view.add_item(yes)
   view.add_item(no)
   await ctx.reply(embed=embed, view=view)
  
  @commands.hybrid_command(aliases=["setnick", "nick"], description="change an user's nickname", usage="[member] <nickname>", help="moderation")
  @Perms.get_perms("manage_nicknames")
  async def nickname(self, ctx, member: NoStaff, *, nick: str=None):
    if nick == None or nick.lower() == "none": return await ctx.send_success(f"Cleared **{member.name}'s** nickname")
    await member.edit(nick=nick)
    return await ctx.send_success(f"Changed **{member.name}'s** nickname to **{nick}**")    
  
  @commands.group(
    name="forcenick",
    usage="(member) (text)",
    invoke_without_command=True,
  )
  @Perms.get_perms("manage_nicknames")
  async def forcenick(self, ctx: commands.Context, member: NoStaff, *, nick: str):
               check = await self.bot.db.fetchrow("SELECT * FROM forcenick WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))               
               if check is None: await self.bot.db.execute("INSERT INTO forcenick VALUES ($1,$2,$3)", ctx.guild.id, member.id, nick)
               else: await self.bot.db.execute("UPDATE forcenick SET nickname = '{}' WHERE user_id = {} AND guild_id = {}".format(nick, member.id, ctx.guild.id))  
               await member.edit(nick=nick)
               await ctx.send_success(f"Now **forcing nickname** for **{member.mention}**")  

  @forcenick.command(
        name="cancel",
        usage="(member)",
        aliases=["remove", "stop", "end"]
    )
  @Perms.get_perms("manage_nicknames")
  async def forcenick_cancel(self, ctx: commands.Context, member: NoStaff, *, nick: str = None):
        check = await self.bot.db.fetchrow("SELECT * FROM forcenick WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))               

        if check is not None:
            await self.bot.db.execute("DELETE FROM forcenick WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id)) 

            if member:
                await member.edit(nick=None)

            await ctx.send_success(f"No longer **forcing nickname** for {member.mention}")
        else:
            await ctx.send_warning(f"Not **forcing nickname** for **{member}**")
               
  @commands.command(description="Kick someone from your server", help="moderation", brief="kick members", usage="[member] <reason>")
  @Perms.get_perms("kick_members")
  async def kick(self, ctx: commands.Context, member: NoStaff, *, reason: str="No reason provided"):
    
    await ctx.guild.kick(user=member, reason=reason + " | {}".format(ctx.author))
    await ModConfig.send_dm(ctx, member, "kicked", reason)
    if not await InvokeClass.invoke_send(ctx, member, reason): await ctx.send_success(f"**{member}** has been kicked for **{reason}**")

  @commands.hybrid_command(description="Ban someone from your server", help="moderation", brief="ban members", usage="[member] <reason>")
  @Perms.get_perms("ban_members")
  async def ban(self, ctx: commands.Context, member: NoStaff, *, reason: str="No reason provided"):

        await ctx.guild.ban(user=member, reason=reason + " | {}".format(ctx.author))
        await ModConfig.send_dm(ctx, member, "banned", reason)
        if not await InvokeClass.invoke_send(ctx, member, reason):
            await ctx.send_success(f"**{member}** has been banned for **{reason}**")

  @commands.hybrid_command(description="Mute someone in your server", help="moderation", brief="moderate members", usage="[member] [time] <reason>", aliases=["timeout"])
  @Perms.get_perms("moderate_members")
  async def mute(self, ctx: commands.Context, member: NoStaff, time: str="60s", *, reason="No reason provided"): 

        tim = humanfriendly.parse_timespan(time)
        until = discord.utils.utcnow() + datetime.timedelta(seconds=tim)
        await member.timeout(until, reason=reason + " | {}".format(ctx.author))
        if not await InvokeClass.invoke_send(ctx, member, reason):
            await ctx.send_success(f"**{member}** has been muted for {humanfriendly.format_timespan(tim)}, muted for **{reason}**")
        await ModConfig.send_dm(ctx, member, "muted", reason + " | " + humanfriendly.format_timespan(tim))
  
  @commands.command(description="Unban someone in your server", help="moderation", usage="[member] [reason]")
  @Perms.get_perms("ban_members")
  async def unban(self, ctx: commands.Context, member: discord.User, *, reason: str="No reason provided"):
    try:
     await ctx.guild.unban(user=member, reason=reason + f" | unbanned by {ctx.author}")
     if not await InvokeClass.invoke_send(ctx, member, reason): await ctx.send_success(f"**{member}** has been unbanned")
    except discord.NotFound: return await ctx.send_warning( f"No ban found for **{member}**") 
  
  @commands.command(description="Ban someone then instantly unban them", help="moderation", usage="[member] [reason]")
  @Perms.get_perms("ban_members")
  async def softban(self, ctx: commands.Context, member: NoStaff, *, reason: str="No reason provided"): 

        await member.ban(reason=reason + f" banned by {ctx.author}")
        await ctx.guild.unban(user=member)
        await ctx.send_success(f"Softbanned **{member}**")

  @commands.hybrid_command(description="Unmute someone in your server", help="moderation", brief="moderate members", usage="[member] <reason>", aliases=["untimeout"])
  @Perms.get_perms("moderate_members")
  async def unmute(self, ctx: commands.Context, member: NoStaff, * , reason: str="No reason provided"): 
    if not member.is_timed_out(): return await ctx.send_warning( f"**{member}** is not muted")
    await member.edit(timed_out_until=None, reason=reason + " | {}".format(ctx.author))
    if not await InvokeClass.invoke_send(ctx, member, reason): await ctx.send_success(f"**{member}** has been unmuted")
  
  @commands.command(aliases=['vcmute'], description="Mute someone in a voice channel", brief="moderate members", usage="[member]", help="moderation")
  @Perms.get_perms("moderate_members")  
  async def voicemute(self, ctx: commands.Context, *, member: NoStaff): 

        if not member.voice.channel:
            return await ctx.send_warning(f"**{member}** is **not** in a voice channel")

        if member.voice.self_mute:
            return await ctx.send_warning(f"**{member}** is **already** voice muted")

        await member.edit(mute=True, reason=f"Voice muted by {ctx.author}")
        return await ctx.send_success(f"Voice muted **{member}**")
 
  @commands.command(aliases=['vcunmute'], description="Unmute someone in a voice channel", brief="moderate members", usage="[member]", help="moderation")
  @Perms.get_perms("moderate_members")  
  async def voiceunmute(self, ctx: commands.Context, *, member: NoStaff): 
      if not member.voice.channel: return await ctx.send_warning( f"**{member}** is **not** in a voice channel")
      if not member.voice.self_mute: return await ctx.send_warning( f"**{member}** is **not** voice muted")
      await member.edit(mute=True, reason=f"Voice muted by {ctx.author}")
      return await ctx.send_success(f"Voice muted **{member}**")
  
  @commands.group(name="clear", invoke_without_command=True)
  async def mata_clear(self, ctx): 
    return await ctx.create_pages()
  
  @mata_clear.command(help="moderation", description="Clear certain messages with word contained in it", usage="[word]", brief="manage messages")
  async def contains(self, ctx: commands.Context, *, word: str): 
   messages = [message async for message in ctx.channel.history(limit=300) if word in message.content]
   if len(messages) == 0: return await ctx.send_warning(f"No messages containing **{word}** in this channel")
   await ctx.channel.delete_messages(messages)

  @commands.group(aliases=['c'], description="Purge messages", help="moderation", brief="manage messages", usage="[messages]")  
  @Perms.get_perms("manage_messages")  
  async def purge(self, ctx: commands.Context, amount: int, *, member: NoStaff=None):
   if member is None: 
    await ctx.channel.purge(limit=amount+1, bulk=True, reason=f"purge invoked by {ctx.author}")
    return await ctx.send_success(f"Purged `{amount}` messages", delete_after=2) 

  @commands.command(name="purgeuser", aliases=['cu'])
  @commands.has_permissions(manage_messages=True)
  async def purge_user(self, ctx, target: Union[discord.Member, int], amount: int = 100):
    amount = min(amount, 100)

    if amount == 0:
        await ctx.send_warning("Amount cannot be 0.")
        return

    if isinstance(target, int):
        try:
            target = await ctx.guild.fetch_member(target)
        except discord.NotFound:
            await ctx.send_warning("User not found.")
            return 

    messages = await ctx.channel.purge(limit=amount + 1, check=lambda m: m.author == target)
  
  @commands.command(description="Bulk delete bot messages", help="moderation", usage="[amount]", aliases=["bc", "botclear"])
  @Perms.get_perms("manage_messages")  
  async def botpurge(self, ctx: commands.Context, amount: int = 100):    
     mes = [] 
     async for message in ctx.channel.history(): 
       if len(mes) == amount: break 
       if message.author.bot: mes.append(message)

       amount = min(amount, 100)

       if amount == 101:
        return await ctx.send_warning("You can only purge up to **100** messages.")

     mes.append(ctx.message)       
     await ctx.channel.delete_messages(mes)   
     await ctx.send(embed = discord.Embed(description=f"> {ctx.author.mention}: Purged `{amount}` messages from **bots**", color=self.bot.color), delete_after=2)

  @purge.command(
    name="after",
    usage="(message)",
    example="dscord.com/chnls/999/..",
    aliases=["upto", "to"],
)
  @commands.has_permissions(manage_messages=True)
  async def purge_after(self, ctx: commands.Context, message: discord.Message):
    """Purge messages after a specified message"""

    if message.channel != ctx.channel:
        return await ctx.send_warning("That **message** isn't in this channel")

    def check(msg):
        return msg.created_at > message.created_at

    try:
        await ctx.message.delete()
    except discord.HTTPException:
        pass

    await ctx.channel.purge(
        limit=300,
        check=check,
        after=message,
        before=ctx.message,
        bulk=True,
        reason=f"{ctx.author}: Purge after",
    )
  @commands.group(invoke_without_command=True)
  @Perms.get_perms("manage_messages")
  async def warn(self, ctx: commands.Context, member: NoStaff=None, *, reason: str="No reason provided"):

        if member is None:
            return await ctx.create_pages()

        date = datetime.datetime.now()
        await self.bot.db.execute("INSERT INTO warns VALUES ($1,$2,$3,$4,$5)", ctx.guild.id, member.id, ctx.author.id, f"{date.day}/{f'0{date.month}' if date.month < 10 else date.month}/{str(date.year)[-2:]} at {datetime.datetime.strptime(f'{date.hour}:{date.minute}', '%H:%M').strftime('%I:%M %p')}", reason)

        if not await InvokeClass.invoke_send(ctx, member, reason):
            await ctx.send_success(f"Warned **{member}** for **{reason}**")

        await ModConfig.send_dm(ctx, member, "warned", reason)

  @warn.command(description="Remove all warns from someone", help="moderation", usage="[member]", brief="manage messages")
  @Perms.get_perms("manage_messages")
  async def clear(self, ctx: commands.Context, *, member: NoStaff): 
      check = await self.bot.db.fetch("SELECT * FROM warns WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)   
      if len(check) == 0: return await ctx.send_warning( f"**{member.name}** has **no** warnings".capitalize())
      await self.bot.db.execute("DELETE FROM warns WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)
      await ctx.send_success(f"Cleared **{member.name}'s** warnings")

  @warn.command(name="list", description="Show warns of someone", help="moderation", usage="[member]")
  async def list(self, ctx: commands.Context, *, member: discord.Member): 
      check = await self.bot.db.fetch("SELECT * FROM warns WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)  
      if len(check) == 0: return await ctx.send_warning( f"**{member.name}** has **no** warnings".capitalize())
      i=0
      k=1
      l=0
      mes = ""
      number = []
      messages = []
      for result in check:
              mes = f"{mes}`{k}` {result['time']} by **{await self.bot.fetch_user(result['author_id'])}** - {result['reason']}\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=self.bot.color, title=f"Warnings ({len(check)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
      messages.append(mes)
      embed = discord.Embed(color=self.bot.color, title=f"Warnings ({len(check)})", description=messages[i]).set_footer(text="Timezone: GMT")
      number.append(embed)
      await ctx.paginator(number)

  @commands.command(description="Show all warns of someone", help="moderation", usage="[member]")
  async def warns(self, ctx: commands.Context, *, member: discord.Member): 
    return await ctx.invoke(self.bot.get_command('warn list'), member=member)

  @commands.command(description="Jail someone", usage="[member]", help="moderation", brief="manage channels")
  @Perms.get_perms("manage_channels")
  @Mod.is_mod_configured()
  async def jail(self, ctx: commands.Context, member: NoStaff, *, reason: str = "No reason provided"):

        check = await self.bot.db.fetchrow("SELECT * FROM jail WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)
        if check:
            return await ctx.send_warning(f"**{member}** is **already** jailed")

        if reason == None:
            reason = "No reason provided"

        roles = [r.id for r in member.roles if r.name != "@everyone" and r.is_assignable()]
        sql_as_text = json.dumps(roles)
        await self.bot.db.execute("INSERT INTO jail VALUES ($1,$2,$3)", ctx.guild.id, member.id, sql_as_text)

        chec = await self.bot.db.fetchrow("SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id)
        roleid = chec["role_id"]

        try:
            jail = ctx.guild.get_role(roleid)
            new = [r for r in member.roles if not r.is_assignable()]
            new.append(jail)

            if not await InvokeClass.invoke_send(ctx, member, reason):
                await member.edit(roles=new, reason=f"jailed by {ctx.author} for {reason}")

            await ctx.send_success(f"**{member}** was jailed for **{reason}**")
            await ModConfig.sendlogs(self.bot, "jail", ctx.author, member, reason)
            await ModConfig.send_dm(ctx, member, "jailed", reason)

            c = ctx.guild.get_channel(int(chec['jail_id']))
            if c:
                await c.send(f"{member.mention}, you have been jailed for **{reason}**")
        except:
            return await ctx.send_error(f"Encountered error whilst jailing **{member}**")

  @commands.command(description="Unjail someoje", usage="[member] [reason]", help="moderation", brief="manage channels")
  @Perms.get_perms("manage_channels")
  @Mod.is_mod_configured()
  async def unjail(self, ctx: commands.Context, member: discord.Member, *, reason: str="No reason provided"):   
      check = await self.bot.db.fetchrow("SELECT * FROM jail WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)      
      if not check: return await ctx.send_warning( f"**{member}** is **not** jailed")     
      sq = check['roles']
      roles = json.loads(sq)
      try: await member.edit(roles=[ctx.guild.get_role(role) for role in roles if ctx.guild.get_role(role)], reason=f"unjailed by {ctx.author}")
      except: pass
      await self.bot.db.execute("DELETE FROM jail WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))
      if not await InvokeClass.invoke_send(ctx, member, reason): await ctx.send_success(f"Unjailed **{member}**")
      await ModConfig.sendlogs(self.bot, "unjail", ctx.author, member, reason)
  
  @commands.command(aliases=["sm"], description="Add slowmode to a channel", help="moderation", usage="[seconds] <channel>", brief="manage channelss")  
  @Perms.get_perms("manage_channels")
  async def slowmode(self, ctx: commands.Context, seconds: str, channel: discord.TextChannel=None):
    chan = channel or ctx.channel
    tim = humanfriendly.parse_timespan(seconds)
    await chan.edit(slowmode_delay=tim, reason="slowmode by {}".format(ctx.author))
    return await ctx.send_success(f"Slowmode for {channel.mention} set to **{humanfriendly.format_timespan(tim)}**")

  @commands.command(description="Lock a channel", help="moderation", usage="<channel>", brief="manage channels")
  @Perms.get_perms("manage_channels")
  async def lock(self, ctx: commands.Context, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    return await ctx.send_success(f"Locked {channel.mention}")

  @commands.command(description="Unlock a channel", help="moderation", usage="<channel>", brief="manage channels")
  @Perms.get_perms("manage_channels")
  async def unlock(self, ctx: commands.Context, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    return await ctx.send_success(f"Unlocked {channel.mention}")       
    
  @commands.group(invoke_without_command=True, description="Manage roles", help="moderation", aliases=["r"])
  @Perms.get_perms("manage_roles")
  async def role(self, ctx: commands.Context, user: discord.Member=None, *, role : GoodRole=None):  
    if role == None or user == None: return await ctx.create_pages()
    if role in user.roles:
      await user.remove_roles(role)
      return await ctx.send_success(f"Removed {role.mention} from **{user.mention}**")
    else: 
      await user.add_roles(role)
      return await ctx.send_success(f"Added {role.mention} to **{user.mention}**")
    
  @role.command(description="Restore someones roles", brief="manage roles", usage="[member]", help="moderation")
  @Perms.get_perms("manage_roles")
  async def restore(self, ctx: commands.Context, *, member: discord.Member):    
    async with ctx.message.channel.typing():
      result = await self.bot.db.fetchrow(f"SELECT * FROM restore WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")         
      if result is None: return await ctx.send_warning(f"Cant to find **saved roles** for **{member}**")
      to_dump = json.loads(result['roles'])
      roles = [ctx.guild.get_role(r) for r in to_dump if ctx.guild.get_role(r) is not None]
      succeed = ', '.join([f"{r.mention}" for r in roles if r.is_assignable()])
      failed = ', '.join([f"<@&{r.id}>" for r in roles if not r.is_assignable()])
      await member.edit(roles=[r for r in roles if r.position < ctx.guild.get_member(self.bot.user.id).top_role.position and r != ctx.guild.premium_subscriber_role and r != '@everyone'])
      await self.bot.db.execute(f"DELETE FROM restore WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
      embed = discord.Embed(color=self.bot.color, description=f"{member} Added roles to {member}: " 'none' if succeed == ', ' else succeed or "none")
      return await ctx.reply(embed=embed)
    
  @role.command(description="Add a role to someone", help="moderation", usage="[user] [role]", name="add", brief="manage roles")
  @Perms.get_perms("manage_roles")
  async def role_add(self, ctx: commands.Context, user: discord.Member, *, role: GoodRole):
    if role in user.roles: return await ctx.send_error( f"**{user}** has this role already") 
    await user.add_roles(role)
    return await ctx.send_success(f"Added {role.mention} to **{user.name}**")
   
  @role.command(name="remove", help="moderation", brief="manage roles", description="remove a role from a member")
  @Perms.get_perms("manage_roles")
  async def role_remove(self, ctx: commands.Context, user: discord.Member, *, role: GoodRole):
    if not role in user.roles: return await ctx.send_error( f"**{user}** doesn't have this role")
    await user.remove_roles(role)
    return await ctx.send_success(f"Removed {role.mention} from **{user.name}**")   

  @role.command(description="Create a role", help="moderation", usage="[name]", brief="manage roles")
  @Perms.get_perms("manage_roles")
  async def create(self, ctx: commands.Context, *, name: str): 
    role = await ctx.guild.create_role(name=name, reason=f"changed role name by {ctx.author}")
    return await ctx.send_success(f"Created role {role.mention}") 
   
  @role.command(description="Delete a role", help="moderation", usage="[role]", brief="manage roles")
  @Perms.get_perms("manage_roles")
  async def delete(self, ctx: commands.Context, *, role: GoodRole): 
      await role.delete()
      return await ctx.send_success("Deleted the role") 
   
  @role.group(invoke_without_command=True, help="moderation", description="edit a role")
  async def edit(self, ctx: commands.Context): 
   return await ctx.create_pages()
   
  @edit.command(description="Make a role hoisted or not", brief="manage roles", help="moderation", usage="[role] [bool <true or false>]")
  @Perms.get_perms("manage_roles")
  async def hoist(self, ctx: commands.Context, role: GoodRole, state: str): 
     if not state.lower() in ["true", "false"]: return await ctx.send_error( f"**{state}** can be only **true** or **false**")
     await role.edit(hoist=bool(state.lower() == "true"))
     return await ctx.send_success(f"{f'The role is **now** hoisted' if role.hoist is True else 'The role is **not** hoisted anymore'}")

  @edit.command(aliases=["pos"], description="Change a roles position", help="moderation", usage="[role] [base role]", brief="manage roles")
  @Perms.get_perms("manage_roles")
  async def position(self, ctx: commands.Context, role: GoodRole, position: GoodRole):
     await role.edit(position=position.position)
     return await ctx.send_success(f"Role position **changed** to `{position.position}`")

  @edit.command(description="Change a roles icon", brief="manage roles", help="moderation", usage="[role] <emoji>")
  @Perms.get_perms("manage_roles")
  async def icon(self, ctx: commands.Context, role: GoodRole, emoji: Union[discord.PartialEmoji, str]):      
      if isinstance(emoji, discord.PartialEmoji): 
       by = await emoji.read()
       await role.edit(display_icon=by)      
      elif isinstance(emoji, str): await role.edit(display_icon=str(emoji))
      return await ctx.send_success("Changed role **icon**")
  
  @edit.command(brief="manage roles", description="Change a roles name", help="moderation", usage="[role] [name]")
  @Perms.get_perms("manage_roles")
  async def name(self, ctx: commands.Context, role: GoodRole, *, name: str): 
     await role.edit(name=name, reason=f"role edited by {ctx.author}")
     return await ctx.send_success(f"Edited the role's name to **{name}**")

  @edit.command(description="Change a roles color", help="moderation", usage="[role] [color]")
  @Perms.get_perms("manage_roles")
  async def color(self, ctx: commands.Context, role: GoodRole, *, color: str):  
    try: 
      color = color.replace("#", "")
      await role.edit(color=int(color, 16), reason=f"role edited by {ctx.author}")
      return await ctx.reply(embed=discord.Embed(color=role.color, description=f"> {ctx.author.mention}: Changed role's color"))
    except: return await ctx.send_error( "Unable to change the role's color")  
  
  @role.group(invoke_without_command=True, name="humans", description="mass add or remove roles from members", help="moderation")  
  async def rolehumans(self, ctx: commands.Context):
    return await ctx.create_pages()
  
  @rolehumans.command(name="remove", description="Remove a role from all humans", help="moderation", usage='[role]', brief="manage_roles")
  @Perms.get_perms("manage_roles")
  async def rolehumansremove(self, ctx: commands.Context, *, role: GoodRole):
      embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention} Removing {role.mention} from all humans, please wait")
      message = await ctx.reply(embed=embed)
      try:
         for member in [m for m in ctx.guild.members if not m.bot]: 
            if not role in member.roles: continue
            await member.remove_roles(role)

         await message.edit(embed=discord.Embed(color=self.bot.color, description=f"> {ctx.author.mention}: Removed {role.mention} from all humans"))
      except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to remove {role.mention} from all humans"))  
  
  @rolehumans.command(name="add", description="Add a role to all humans", help="moderation", usage='[role]', brief="manage_roles")  
  @Perms.get_perms("manage_roles")
  async def rolehumansadd(self, ctx: commands.Context, *, role: GoodRole):  
    embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention}: Adding {role.mention} to all humans, please wait")
    message = await ctx.reply(embed=embed)
    try:
     for member in [m for m in ctx.guild.members if not m.bot]: 
       if role in member.roles: continue
       await member.add_roles(role)

     await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all humans"))
    except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all humans")) 

  @role.group(invoke_without_command=True, name="bots", description="mass add or remove roles from members", help="moderation")  
  async def rolebots(self, ctx: commands.Context):
    return await ctx.create_pages()
  
  @rolebots.command(name="remove", description="Remove a role from all bots", help="moderation", usage='[role]', brief="manage_roles")
  @Perms.get_perms("manage_roles")
  async def rolebotsremove(self, ctx: commands.Context, *, role: GoodRole):
      embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention} Removing {role.mention} from all bots, please wait.")
      message = await ctx.reply(embed=embed)
      try:
         for member in [m for m in ctx.guild.members if m.bot]: 
            if not role in member.roles: continue
            await member.remove_roles(role)

         await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {ctx.author.mention}: Removed {role.mention} from all bots"))
      except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to remove {role.mention} from all bots"))  
  
  @rolebots.command(name="add", description="Add a role to all bots", help="moderation", usage='[role]', brief="manage_roles")  
  @Perms.get_perms("manage_roles")
  async def rolebotsadd(self, ctx: commands.Context, *, role: GoodRole):  
    embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention}: Adding {role.mention} to all bots, please wait.")
    message = await ctx.reply(embed=embed)
    try:
     for member in [m for m in ctx.guild.members if m.bot]: 
       if role in member.roles: continue
       await member.add_roles(role)

     await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all bots"))
    except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all bots"))    

  @role.group(invoke_without_command=True, name="all", description="mass add or remove roles from members", help="moderation")  
  async def roleall(self, ctx: commands.Context):
    return await ctx.create_pages()
  
  @roleall.command(name="remove", description="Remove a role from all members", help="moderation", usage='[role]', brief="manage_roles")
  @Perms.get_perms("manage_roles")
  async def roleallremove(self, ctx: commands.Context, *, role: GoodRole):
      embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention} Removing {role.mention} from all members, please wait.")
      message = await ctx.reply(embed=embed)
      try:
         for member in ctx.guild.members: 
            if not role in member.roles: continue
            await member.remove_roles(role)

         await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {ctx.author.mention}: Removed {role.mention} from all members"))
      except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to remove {role.mention} from all members"))  
  
  @roleall.command(name="add", description="Add a role to all members", help="moderation", usage='[role]', brief="manage_roles")  
  @Perms.get_perms("manage_roles")
  async def rolealladd(self, ctx: commands.Context, *, role: GoodRole):  
    embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention}: Adding {role.mention} to all members, please wait.")
    message = await ctx.reply(embed=embed)
    try:
     for member in ctx.guild.members: 
       if role in member.roles: continue
       await member.add_roles(role)

     await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all members"))
    except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all members")) 

  @commands.command(name='reactionmute', aliases=['reactmute','rmute','rm'], description="Mute or unmute a member from reacting", brief='member', usage='<user>', extras={'perms':'Moderate Members'})
  @commands.has_permissions(moderate_members=True)
  async def reactionmute(self, ctx, *, member: discord.Member):
    if member == ctx.guild.owner:
      return await ctx.send_warning(f"You cannot **reaction mute** the **owner**")
    if ctx.author != ctx.guild.owner:
      if member.top_role.position >= ctx.author.top_role.position:
        return await ctx.send_warning(f"You cannot **reaction mute** {member.mention}")
    if member in ctx.channel.overwrites:
      try:
        await ctx.channel.set_permissions(member, overwrite=None, reason=f"reaction mute undone by {ctx.author}")
        return await ctx.send_success(f"{member.mention} can now **add reactions** again")
      except:
        return await ctx.send_warning(f"Unable to undo **reaction mute** on {member.mention}")
    else:
      try:
        await ctx.channel.set_permissions(member, overwrite=discord.PermissionOverwrite(add_reactions=False), reason=f"reaction muted by {ctx.author}")
        return await ctx.send_success(f"Successfully **reaction muted** {member.mention}")
      except:
        return await ctx.send_warning(f"Unable to **reaction mute** {member.mention}")
      
  @commands.command(
    name="audit",
    usage="<user> <action>",
    example="@joyclens ban",
)
  @commands.has_permissions(view_audit_log=True)
  async def audit(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None, action: Optional[str] = None):
    """View audit log entries"""

    if action and not self.pretty_actions.get(action.lower().replace(" ", "_")):
        return await ctx.send_warning(f"`{action}` isn't a recognized **action**")

    entries = []
    METHOD = (
        ctx.guild.audit_logs(limit=100, user=user, action=getattr(discord.AuditLogAction, action.lower().replace(" ", "_")))
        if action and user
        else ctx.guild.audit_logs(limit=100, user=user)
        if user
        else ctx.guild.audit_logs(limit=100, action=getattr(discord.AuditLogAction, action.lower().replace(" ", "_")))
        if action
        else ctx.guild.audit_logs(limit=100)
    )

    async for entry in METHOD:
        pretty_action = self.pretty_actions.get(entry.action.name)
        if not pretty_action:
            continue

        target = None
        with contextlib.suppress(TypeError):
            if target := getattr(entry, "target", None):
                if type(target) is discord.TextChannel:
                    target = f"#{target.name}"
                elif type(target) is discord.Role:
                    target = f"@{target.name}"
                elif type(target) is discord.Emoji:
                    target = target.name
                else:
                    if isinstance(target, discord.Object):
                        target = target.id
                    else:
                        target = str(target)

        timestamp_unix = int(entry.created_at.timestamp())
        timestamp_discord = f"<t:{timestamp_unix}:R>"
        entries.append(f"> **{entry.user.mention}** {pretty_action}" + (f" **`{target}`**" if target else "") + f" {timestamp_discord}")

    if not entries:
        return await ctx.send_warning("No **audit log** entries found")


    embed = discord.Embed(
        title="Audit Log",
        description="\n".join(entries[:5]),
        color=self.bot.color,
    )
    await ctx.send(embed=embed)

  @commands.command(name="auditvariables", aliases=["avariables"], description="View audit log variables", brief="audit")
  async def audit_variables(self, ctx: commands.Context):
     """View audit log variables"""
     embed = discord.Embed(color=self.bot.color)
     embed.add_field(name="Variables", value=f"```{', '.join(self.pretty_actions.keys())}```", inline = False)
     embed.add_field(name="Examples", value=f"```{ctx.clean_prefix}audit @joyclens ban\n{ctx.clean_prefix}audit @joyclens role_create\n{ctx.clean_prefix}audit @joyclens guild_update```", inline = False)
     await ctx.send(embed=embed)

async def setup(bot: commands.Bot): 
    await bot.add_cog(Moderation(bot))      