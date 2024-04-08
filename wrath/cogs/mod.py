import discord, random
import aiohttp
import os
import datetime
from discord.ext import commands
from discord import TextChannel, ChannelType, Embed, Role, Member,  Message, User, SelectOption, Interaction, PartialEmoji, PermissionOverwrite
from discord.ui import View, Button
import json
from datetime import datetime, timedelta
import psutil
from tools.checks import Perms
import asyncio
import tracemalloc
from tools.utils import EmbedBuilder, GoodRole, NoStaff
from tools.checks import Perms as utils
from typing import Union

from io import BytesIO
import requests


tracemalloc.start()


class mod(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot        

   @commands.group(name='thread', invoke_without_command=True)
   async def thread(self, ctx):
        await ctx.send_help()

   @thread.command(name='lock')
   @utils.get_perms("administrator")
   async def close_thread(self, ctx):
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.send_warning("This command can only be used in threads")
        
        if not ctx.channel.permissions_for(ctx.author).manage_threads:
            return await ctx.send_warning("You don't have permission to lock this thread")
        
        try:
            await ctx.send_success(f"{ctx.channel.mention} has been **locked**")
            await ctx.channel.edit(archived=True)
        except discord.Forbidden:
            await ctx.send_warning("I don't have permission to lock this thread")

   @thread.command(name='unlock')
   @utils.get_perms("administrator")
   async def open_thread(self, ctx):
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.send_warning("This command can only be used in threads")
        
        if not ctx.channel.permissions_for(ctx.author).manage_threads:
            return await ctx.send_warning("You don't have permission to unlock this thread")
        
        try:
            await ctx.send_success(f"{ctx.channel.mention} has been **unlocked**")
            await ctx.channel.edit(archived=False)
        except discord.Forbidden:
            await ctx.send_warning("I don't have permission to unlock this thread")
    
   @thread.command(name='delete')
   @utils.get_perms("administrator")
   async def delete_thread(self, ctx, channel: discord.Thread = None):
        if channel is None:
            channel = ctx.channel
        elif not isinstance(channel, discord.Thread):
            return await ctx.send_warning("Please mention a thread channel")

        if channel != ctx.channel and not ctx.channel.permissions_for(ctx.author).manage_threads:
            return await ctx.send_warning("You don't have permission to close this thread")

        try:
            message = await ctx.send(embed=discord.Embed(
                description=f"> {channel.mention} will be deleted in **5** seconds",
                color=self.bot.color
            ))
            await asyncio.sleep(5)
            await channel.delete()
        except discord.Forbidden:
            await ctx.send_warning("I don't have permission to close this thread")
        else:
            if channel != ctx.channel:
                await message.edit(embed=discord.Embed(
                    description=f"> The thread **`{channel.name}`** has been deleted by {ctx.author.mention}",
                    color=self.bot.color
                ))

   @thread.command(name='delall')
   @utils.get_perms("administrator")
   async def delete_all_threads_in_channel(self, ctx, channel: discord.Thread = None):
    if channel is None:
        channel = ctx.channel
    elif not isinstance(channel, discord.Thread):
        return await ctx.send_warning("Please mention a thread channel")

    threads = channel.threads

    if not threads:
        return await ctx.send_warning(f"There are no threads in {channel.mention}")

    deleted_thread_info = []
    for thread in threads:
        creator = thread.owner.mention if thread.owner else "Unknown"
        deleted_thread_info.append(f"**{thread.name}** by **{creator}**")

        try:
            await thread.delete()
        except discord.Forbidden:
            await ctx.send_warning("I don't have permission to delete threads in this channel")
        except Exception as e:
            await ctx.send_warning(f"An error occurred while deleting threads: {e}")

    deleted_thread_info_str = '\n'.join(deleted_thread_info)
    await ctx.send_success(f"Deleted `{len(threads)}` threads from {channel.mention}\n\n>>> {deleted_thread_info_str}")

   @thread.command(name='open', aliases=['create'])
   
   async def create_thread(self, ctx, name=None):
        if name is None:
            name = ctx.author.name

        try:
            message = ctx.message 
            thread = await message.create_thread(name=name, auto_archive_duration=1440)  
            await ctx.send_success(f"Thread **{thread.mention}** created successfully")

            await thread.add_user(ctx.author)

        except discord.Forbidden:
            await ctx.send_warning("I don't have permission to create a thread in this channel.")
        except Exception as e:
            await ctx.send_warning(f"An error occurred: {e}")

   @thread.command(name='delafter')
   @utils.get_perms("administrator")
   async def delete_inactive_threads(self, ctx, duration: int):
    duration = min(duration, 5)
    
    inactive_threshold = discord.utils.utcnow() - timedelta(days=duration)

    inactive_threads = []
    for guild in ctx.bot.guilds:
        for channel in guild.text_channels:
            threads = channel.threads
            if threads:
                inactive_threads.extend([thread for thread in threads if thread.last_message.created_at < inactive_threshold])

    for thread in inactive_threads:
        try:
            await thread.delete()
        except discord.Forbidden:
            await ctx.send_warning("I don't have permission to delete threads in this channel.")
        except Exception as e:
            await ctx.send_warning(f"An error occurred while deleting threads: {e}")

    await ctx.send_success(f"Deleted **{len(inactive_threads)}** inactive threads for **{duration}** days of inactivity")

   @thread.command(name="list")
   async def list_threads(self, ctx, channel: discord.Thread = None):
       if channel is None:
           channel = ctx.channel
       elif not isinstance(channel, discord.Thread):
           return await ctx.send_warning("Please mention a thread channel.")

       threads = channel.threads
       if not threads:
           return await ctx.send_warning(f'There are no active threads in {channel.mention}.')

       thread_list = '\n'.join([f'`{i+1}.` **{thread.mention}** by **{thread.owner.mention}**, created **<t:{int(thread.created_at.timestamp())}:R>**' for i, thread in enumerate(threads)])
       embed = discord.Embed(
              title=f"Threads in #{channel.name}",
        description=f"{thread_list}",
           color=self.bot.color
       )
       await ctx.send(embed=embed)

   @commands.group(name="server", invoke_without_command=True)
   async def server(self, ctx):
            await ctx.send_help()

   @server.command(name="seticon")
   async def server_set_icon(self, ctx, *, image=None):
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send_warning("You don't have permission to use this command.")
        return

    if image is None and len(ctx.message.attachments) == 0:
        await ctx.send_warning("Please provide an image attachment or a link.")
        return

    try:
        if image is None:
            image_url = ctx.message.attachments[0].url
        else:
            image_url = image.strip('<>')

        image_data = BytesIO(requests.get(image_url).content)
        await ctx.guild.edit(icon=image_data.read())
        await ctx.send_success(f"Server icon has been updated to [**this image**]({image_url}) successfully!")
    except Exception as e:
        await ctx.send_warning(f"Failed to update server icon: {e}")

   @server.command(name="setbanner")
   async def server_set_banner(self, ctx, *, image=None):
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send_warning("You don't have permission to use this command.")
        return

    if image is None and len(ctx.message.attachments) == 0:
        await ctx.send_warning("Please provide an image attachment or a link.")
        return

    try:
        if image is None:
            image_url = ctx.message.attachments[0].url
        else:
            image_url = image.strip('<>')

        image_data = BytesIO(requests.get(image_url).content)
        await ctx.guild.edit(banner=image_data.read())
        await ctx.send_success(f"Server banner has been updated to [**this image**]({image_url}) successfully!")
    except Exception as e:
        await ctx.send_warning(f"Failed to update server banner: {e}")

   @server.command(name="setsplash")
   async def server_set_splash(self, ctx, *, image=None):
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send_warning("You don't have permission to use this command.")
        return

    if image is None and len(ctx.message.attachments) == 0:
        await ctx.send_warning("Please provide an image attachment or a link.")
        return

    try:
        if image is None:
            image_url = ctx.message.attachments[0].url
        else:
            image_url = image.strip('<>')

        image_data = BytesIO(requests.get(image_url).content)
        await ctx.guild.edit(splash=image_data.read())
        await ctx.send_success(f"Server banner has been updated to [**this image**]({image_url}) successfully!")
    except Exception as e:
        await ctx.send_warning(f"Failed to update server splash: {e}")


   @commands.command(name="nick", aliases=['nickname', 'n'])
   async def set_nickname(self, ctx, member: discord.Member, *, name: str):
        if not ctx.author.guild_permissions.manage_nicknames:
            await ctx.send_warning("You don't have permission to change nicknames.")
            return
        
        try:
            await member.edit(nick=name)
            await ctx.send_success(f"Nickname for {member.mention} has been set to **{name}**")
        except Exception as e:
            await ctx.send_warning(f"Failed to set nickname: {e}")

   @commands.command(name="resetnick", aliases=['resetnickname', 'rn'])
   async def reset_nickname(self, ctx, member: discord.Member = None):
        if not ctx.author.guild_permissions.manage_nicknames:
            await ctx.send_warning("You don't have permission to change nicknames.")
            return

        if member is None:
            member = ctx.author

        try:
            await member.edit(nick=None)
            await ctx.send_success(f"Nickname for {member.mention} has been reset.")
        except Exception as e:
            await ctx.send_warning(f"Failed to reset nickname: {e}")

   @commands.command(name="resetnickall", aliases=['resetnicknameall', 'rna'])
   async def reset_all_nicknames(self, ctx):
    if not ctx.author.guild_permissions.manage_nicknames:
        await ctx.send_warning("You don't have permission to change nicknames.")
        return

    wait_message = await ctx.send_warning("Please wait whilst I reset **everyones** nicknames, this may **take a while.**")

    success_count = 0
    failed_count = 0
    success_list = []
    failed_list = []

    try:
        for member in ctx.guild.members:
            if member.nick:
                try:
                    old_nick = member.nick
                    await member.edit(nick=None)
                    success_count += 1
                    success_list.append(f"> {member.mention} from `{old_nick}` to `{member.display_name}`")
                except Exception as e:
                    failed_count += 1
                    failed_list.append((member.display_name, str(e)))

        success_message = f"> **{success_count}** nicknames have been reset successfully:"
        failed_message = f"Failed to reset **{failed_count}** nicknames:"

        if success_list:
            success_message += "\n" + "\n".join(success_list)
        if failed_list:
            failed_message += "\n" + "\n".join([f"{member}: {reason}" for member, reason in failed_list])

        if success_count > 0:
            embed = discord.Embed(
                description=success_message,
                color=self.bot.color
            )
            await ctx.send(embed=embed)
        if failed_count > 0:
            await ctx.send_warning(failed_message)

    except Exception as e:
        await ctx.send_warning(f"An unexpected error occurred: {e}")

    await wait_message.delete()

    # basic moderation 

   @commands.command()
   async def ban(self, ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send_warning("You don't have permission to ban members.")

    try:
        embed = discord.Embed(
            title=f"Banned",
            color=self.bot.color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Moderator", value="autobanned by wrath", inline=True)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Contact an admin to dispute this moderation action")
        await member.send(embed=embed)
        ban_reason = f"{reason} | autobanned by wrath" if reason else f"autobanned by wrath"
        await member.ban(reason=ban_reason)
        if reason:
            await ctx.send_success(f"{member.mention} has been banned for: **{reason}**")
        else:
            await ctx.send_success(f"**{member.mention}** has been banned")
    except Exception as e:
        await ctx.send_warning(f"Failed to ban {member}: {e}")

   @commands.command()
   async def kick(self, ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.kick_members:
        return await ctx.send_warning("You don't have permission to kick members.")

    try:
        embed = discord.Embed(
            title=f"Kicked",
            color=self.bot.color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.name, inline=True)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Contact an admin to dispute this moderation action")
        kick_reason = f"{reason} | kicked by {ctx.author.name}" if reason else f"kicked by {ctx.author.name}"
        await member.send(embed=embed)
        await member.kick(reason=kick_reason)
        if reason:
            await ctx.send_success(f"{member.mention} has been kicked for: **{reason}**")
        else:
            await ctx.send_success(f"**{member.mention}** has been kicked")
    except Exception as e:
        await ctx.send_warning(f"Failed to kick {member}: {e}")

   @commands.command(name="unbanall", aliases=["ua"])
   async def unban_all(self, ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send_warning("You don't have permission to run this command.")

    try:
        server = ctx.guild
        
        wait_message = await ctx.send_warning("Please wait whilst I unban **all** users, this may **take a while.**")

        async for ban_entry in server.bans():
            user = ban_entry.user
            await server.unban(user)

        await wait_message.delete()
        await ctx.send_success("All users have been unbanned.")
    
    except Exception as e:
        await ctx.send_warning(f"Failed to unban all users: {e}")

   @commands.command()
   async def unban(self, ctx, user: discord.User, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send_warning("You don't have permission to unban members.")

    try:
        unban_reason = f"{reason} | unbanned by {ctx.author.name}" if reason else f"unbanned by {ctx.author.name}"
        await ctx.guild.unban(user, reason=unban_reason)
        if reason:
            await ctx.send_success(f"**{user}** has been unbanned for: **{reason}**")
        else:
            await ctx.send_success(f"**{user}** has been unbanned")
    except Exception as e:
        await ctx.send_warning(f"Failed to unban {user}: {e}")

   @commands.command()
   async def softban(self, ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send_warning("You don't have permission to ban members.")
    
    try:
        embed = discord.Embed(
            title=f"Softbanned",
            color=self.bot.color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Server", value=ctx.guild.name, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.name, inline=True)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Contact an admin to dispute this moderation action")
        await member.send(embed=embed)
        await member.ban(reason=reason)
        softbanned_reason = f"{reason} | softbanned by {ctx.author.name}" if reason else f"softbanned by {ctx.author.name}"
        await member.unban(reason=softbanned_reason)
        
        if reason:
            await ctx.send_success(f"{member.mention} has been softbanned for: **{reason}**")
        else:
            await ctx.send_success(f"**{member.mention}** has been softbanned")
    
    except Exception as e:
        await ctx.send_warning(f"Failed to softban {member}: {e}")

   @commands.command(description="Lock a channel", help="moderation", usage="<channel>", brief="manage channels")
   @Perms.get_perms("manage_channels")
   async def lock(self, ctx: commands.Context, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    return await ctx.send_success(f"Locked {channel.mention}, use **{ctx.clean_prefix}unlock** `#{channel.name}` to unlock this channel")
   
   @commands.command(description="Unlock a channel", help="moderation", usage="<channel>", brief="manage channels")
   @Perms.get_perms("manage_channels")
   async def unlock(self, ctx: commands.Context, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    return await ctx.send_success(f"Unlocked {channel.mention} - check permissions if previously hidden")   
   
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

   @commands.Cog.listener()
   async def on_member_remove(self, member):
    if member.guild.me.guild_permissions.kick_members:
        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
            if entry.target == member:
                kicker = entry.user
                reason = entry.reason

                embed = discord.Embed(
                    description=f"> You were kicked from `{member.guild.name}` by **{kicker.mention}** manually",
                    color=self.bot.color
                )
                try:
                    await member.send(embed=embed)
                except discord.Forbidden:
                    print(f"Failed to send DM to {member} after being kicked from {member.guild.name}")


   @commands.command(name="roleall", description="Add a role to all members")  
   @commands.has_permissions(administrator=True)
   async def rolealladd(self, ctx: commands.Context, *, role: GoodRole):  
    embed = discord.Embed(color=self.bot.color, description=f"{ctx.author.mention}: Adding {role.mention} to all members, please wait.")
    message = await ctx.reply(embed=embed)
    try:
     for member in ctx.guild.members: 
       if role in member.roles: continue
       await member.add_roles(role)

     await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {ctx.author.mention}: Added {role.mention} to all members"))
    except Exception: await message.edit(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: Unable to add {role.mention} to all members")) 

   @commands.group(invoke_without_command=True)
   async def autorole(self, ctx): 
      await ctx.create_pages()

   @autorole.command(name="add", description="Add a role to new joining members", help="config", usage="[role]", brief="manage_guild")
   @commands.has_permissions(manage_guild=True)
   async def autorole_add(self, ctx: commands.Context, *, role: Union[Role, str]): 
      if isinstance(role, str): 
        role = ctx.find_role( role)
        if role is None: return await ctx.send_error(f"Unable to find role **{ctx.message.clean_content[-len(ctx.clean_prefix)+11:]}**")         
      
      if self.bot.is_dangerous(role): return await ctx.send_warning("This role **cannot** be added to **autorole*")
      check = await self.bot.db.fetchrow("SELECT * FROM autorole WHERE guild_id = {} AND role_id = {}".format(ctx.guild.id, role.id))
      if check is not None: return await ctx.send_error(f"{role.mention} **already exists**")
      await self.bot.db.execute("INSERT INTO autorole VALUES ($1,$2)", role.id, ctx.guild.id)      
      return await ctx.send_success(f"**Added** {role.mention} to autorole")
    
   @autorole.command(name="remove", description="Remove a role from being added to new joining members", help="config", usage="<role>", brief="manage_guild")
   @commands.has_permissions(manage_guild=True)
   async def autorole_remove(self, ctx: commands.Context, *, role: Union[Role, str]=None): 
      if isinstance(role, str): 
        role = ctx.find_role( role)
        if role is None: return await ctx.send_error(f"Unable to find a role called **{ctx.message.clean_content[-len(ctx.clean_prefix)+14:]}**")         
      if role is not None:
        check = await self.bot.db.fetchrow("SELECT * FROM autorole WHERE guild_id = {} AND role_id = {}".format(ctx.guild.id, role.id))
        if check is None: return await ctx.send_error(f"{role.mention} **isn't** added")
        await self.bot.db.execute("DELETE FROM autorole WHERE guild_id = {} AND role_id = {}".format(ctx.guild.id, role.id))
        return await ctx.send_success(f"**Removed** {role.mention} from autorole")

      check = await self.bot.db.fetch("SELECT * FROM autorole WHERE guild_id = {}".format(ctx.guild.id))
      if check is None: return await ctx.send_error("there is **no** role".capitalize())    
      await self.bot.db.execute("DELETE FROM autorole WHERE guild_id = {}".format(ctx.guild.id))
      return await ctx.send_success("**All** roles were **removed**")
    
   @autorole.command(name="list", description="List all the roles being added to new joining members", help="config")
   async def autorole_list(self, ctx: commands.Context): 
          i=0
          k=1
          l=0
          mes = ""
          number = []
          messages = []
          results = await self.bot.db.fetch("SELECT * FROM autorole WHERE guild_id = {}".format(ctx.guild.id))
          if not results: return await ctx.send_warning("**No** autoroles **exist** for this **guild**")
          for result in results:
              mes = f"{mes}`{k}` {ctx.guild.get_role(int(result[0])).mention if ctx.guild.get_role(int(result[0])) else result[0]}\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=self.bot.color, title=f"Autoroles ({len(results)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
          messages.append(mes)
          number.append(discord.Embed(color=self.bot.color, title=f"Autoroles ({len(results)})", description=messages[i]))
          return await ctx.paginator(number)


async def setup(bot) -> None:
    await bot.add_cog(mod(bot))      
