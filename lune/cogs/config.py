import json, traceback, datetime 
from discord import TextChannel, ChannelType, Embed, Role, Member,  Message, User, SelectOption, Interaction, PartialEmoji, PermissionOverwrite
from discord.ext.commands import Cog, Context, group, hybrid_command, hybrid_group, command, AutoShardedBot as AB
from discord.ui import Select, View, Button 
from typing import Union
from tools.checks import Perms as utils, Boosts
from tools.utils import EmbedBuilder, InvokeClass
from tools.utils import EmbedScript

poj_cache = {}

async def dm_cmds(ctx: Context, embed: str) -> Message:
  res = await ctx.bot.db.fetchrow("SELECT embed FROM dm WHERE guild_id = $1 AND command = $2", ctx.guild.id, ctx.command.name)
  if res:
   name = res['embed']    
   if embed == "none": 
    await ctx.bot.db.execute("DELETE FROM dm WHERE guild_id = $1 AND command = $2", ctx.guild.id, ctx.command.name)
    return await ctx.send_success(f"Deleted the **{ctx.command.name}** custom response")
   elif embed == "view": 
    em = Embed(color=ctx.bot.color, title=f"dm {ctx.command.name} message", description=f"```{name}```")
    return await ctx.reply(embed=em)
   elif embed == name: return await ctx.send_warning(f"This embed is already **configured** as the {ctx.command.name} custom dm")
   else:
      await ctx.bot.db.execute("UPDATE dm SET embed = $1 WHERE guild_id = $2 AND command = $3", embed, ctx.guild.id, ctx.command.name)
      return await ctx.send_success(f"Updated your custom **{ctx.command.name}** message to\n```{embed}```")
  else: 
   await ctx.bot.db.execute("INSERT INTO dm VALUES ($1,$2,$3)", ctx.guild.id, ctx.command.name, embed)
   return await ctx.send_success(f"Added your custom **{ctx.command.name}** direct message to\n```{embed}```")

class config(Cog):
    def __init__(self, bot: AB):
        self.bot = bot 
        
    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot: return   
        results = await self.bot.db.fetch("SELECT * FROM pingonjoin WHERE guild_id = $1", member.guild.id)
        members = [m for m in member.guild.members if (datetime.datetime.now() - m.joined_at.replace(tzinfo=None)).total_seconds() < 180]
        for result in results: 
         channel = member.guild.get_channel(int(result[0]))
         if channel: 
          if len(members) < 10: 
            try: await channel.send(member.mention, delete_after=6)
            except: continue    
          else:           
           if not poj_cache.get(str(channel.id)): poj_cache[str(channel.id)] = []
           poj_cache[str(channel.id)].append(f"{member.mention}")
           if len(poj_cache[str(channel.id)]) == 10: 
            try: 
             await channel.send(' '.join([m for m in poj_cache[str(channel.id)]]), delete_after=6) 
             poj_cache[str(channel.id)] = []
            except:
             poj_cache[str(channel.id)] = [] 
             continue 
    
    @Cog.listener()
    async def on_message(self, message: Message):
      if not message.guild: return
      if isinstance(message.author, User): return
      if message.author.guild_permissions.manage_guild: return 
      if message.author.bot: return 
      if message.attachments: return       
      check = await self.bot.db.fetchrow("SELECT * FROM mediaonly WHERE channel_id = $1", message.channel.id)
      if check: 
        try: await message.delete()
        except: pass 

    @hybrid_command(name="createembed", aliases=['ce'], help="config", description="create embed", usage="[code]")
    async def createembed(self, ctx: Context,  *, code: EmbedScript):
     await ctx.send(**code)


    @hybrid_command(description="set your own prefix", usage="[prefix]", help="config")
    async def selfprefix(self, ctx: Context, prefix: str):      
      if len(prefix) > 3 and prefix.lower() != "none": return await ctx.send_error("That **prefix** is **too long**")
      if prefix.lower() == "none": 
        check = await self.bot.db.fetchrow("SELECT * FROM selfprefix WHERE user_id = {}".format(ctx.author.id)) 
        if check is not None:
          await self.bot.db.execute("DELETE FROM selfprefix WHERE user_id = {}".format(ctx.author.id))
          return await ctx.send_success("**Selfprefix** has been **removed**")
        elif check is None: return await ctx.send_error("no **selfprefix** found".capitalize())   
      else:    
        result = await self.bot.db.fetchrow("SELECT * FROM selfprefix WHERE user_id = {}".format(ctx.author.id)) 
        if result is not None: await self.bot.db.execute("UPDATE selfprefix SET prefix = $1 WHERE user_id = $2", prefix, ctx.author.id)
        elif result is None: await self.bot.db.execute('INSERT INTO selfprefix VALUES ($1, $2)', ctx.author.id, prefix)
        return await ctx.send_success(f"updated your **selfprefix** to `{prefix}`".capitalize()) 
   
    @hybrid_group(invoke_without_command=True, aliases=["poj"])
    async def pingonjoin(self, ctx): 
      await ctx.create_pages()

    @pingonjoin.command(name="add", description="Ping new members in a certain channel once they join", help="config", usage="[channel]", brief="manage_guild")
    @utils.get_perms("manage_guild")
    async def poj_add(self, ctx: Context, *, channel: TextChannel): 
        check = await self.bot.db.fetchrow("SELECT * FROM pingonjoin WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
        if check is not None: return await ctx.send_warning(f"{channel.mention} is **already** added")
        elif check is None: await self.bot.db.execute("INSERT INTO pingonjoin VALUES ($1,$2)", channel.id, ctx.guild.id)
        return await ctx.send_success(f"I will now **ping** joining members in {channel.mention}")  
    
    @pingonjoin.command(name="remove", description="Remove a channel from ping on join", help="config", usage="<channel>", brief="manage_guild")
    @utils.get_perms("manage_guild")
    async def poj_remove(self, ctx: Context, *, channel: TextChannel=None): 
      if channel is not None: 
        check = await self.bot.db.fetchrow("SELECT * FROM pingonjoin WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
        if check is None: return await ctx.send_error(f"{channel.mention} is **not** added")
        elif check is not None: await self.bot.db.execute("DELETE FROM pingonjoin WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
        return await ctx.send_success(f"I will now **ping** joining members in {channel.mention}")

      check = await self.bot.db.fetch("SELECT * FROM pingonjoin WHERE guild_id = {}".format(ctx.guild.id))
      if check is None: return await ctx.send_error("They is **no channel** added")
      elif check is not None:  await self.bot.db.execute("DELETE FROM pingonjoin WHERE guild_id = {}".format(ctx.guild.id))
      return await ctx.send_success("I will now **not** ping any new members joining") 
    
    @pingonjoin.command(name="list", description="List all of your ping on join channels", help="config")
    async def poj_list(self, ctx: Context): 
          i=0
          k=1
          l=0
          mes = ""
          number = []
          messages = []
          results = await self.bot.db.fetch("SELECT * FROM pingonjoin WHERE guild_id = {}".format(ctx.guild.id))
          if results is None: return await ctx.send_error("There are **no** ping on join channels for this guild")
          for result in results:
              mes = f"{mes}`{k}` {ctx.guild.get_channel(int(result['channel_id'])).mention if ctx.guild.get_channel(result['channel_id']) else result['channel_id']}\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(Embed(color=self.bot.color, title=f"Channels ({len(results)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
          messages.append(mes)
          number.append(Embed(color=self.bot.color, title=f"Channels ({len(results)})", description=messages[i]))
          await ctx.paginator(number)

    @group(invoke_without_command=True)
    async def autorole(self, ctx): 
      await ctx.create_pages()

    @autorole.command(name="add", description="Add a role to new joining members", help="config", usage="[role]", brief="manage_guild")
    @utils.get_perms("manage_guild")
    async def autorole_add(self, ctx: Context, *, role: Union[Role, str]): 
      if isinstance(role, str): 
        role = ctx.find_role( role)
        if role is None: return await ctx.send_error(f"Unable to find role **{ctx.message.clean_content[-len(ctx.clean_prefix)+11:]}**")         
      
      if self.bot.is_dangerous(role): return await ctx.send_warning("This role **cannot** be added to **autorole*")
      check = await self.bot.db.fetchrow("SELECT * FROM autorole WHERE guild_id = {} AND role_id = {}".format(ctx.guild.id, role.id))
      if check is not None: return await ctx.send_error(f"{role.mention} **already exists**")
      await self.bot.db.execute("INSERT INTO autorole VALUES ($1,$2)", role.id, ctx.guild.id)      
      return await ctx.send_success(f"**Added** {role.mention} to autorole")
    
    @autorole.command(name="remove", description="Remove a role from being added to new joining members", help="config", usage="<role>", brief="manage_guild")
    @utils.get_perms("manage_guild")
    async def autorole_remove(self, ctx: Context, *, role: Union[Role, str]=None): 
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
    async def autorole_list(self, ctx: Context): 
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
               number.append(Embed(color=self.bot.color, title=f"Autoroles ({len(results)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
          messages.append(mes)
          number.append(Embed(color=self.bot.color, title=f"Autoroles ({len(results)})", description=messages[i]))
          return await ctx.paginator(number)
    
    
    @command(aliases=["dcmd"], description="Disable a command in your server", help="config", usage="[command name]")  
    @utils.get_perms("administrator")          
    async def disablecommand(self, ctx: Context, *, cmd: str): 
     found_command = self.bot.get_command(cmd)
     if found_command is None: return await ctx.send_warning(f"Command **{cmd}** not found")
     if found_command.name in ["ping", "help", "uptime", "disablecommand", "disablecmd", "enablecommand", "enablecmd"]: return await ctx.send_warning("This command can't be disabled")
     check = await self.bot.db.fetchrow("SELECT * FROM disablecommand WHERE command = $1 AND guild_id = $2", found_command.name, ctx.guild.id)
     if check: return await ctx.send_error("This command is **already** disabled")
     await self.bot.db.execute("INSERT INTO disablecommand VALUES ($1,$2)", ctx.guild.id, found_command.name)     
     await ctx.send_success(f"Disabled command **{found_command.name}**")

    @command(aliases=["ecmd"], help="Enable a previously disabled command", description="config", usage="[command name]")
    @utils.get_perms("administrator")
    async def enablecommand(self, ctx: Context, *, cmd: str): 
     found_command = self.bot.get_command(cmd)
     if found_command is None: return await ctx.send_warning(f"Command **{cmd}** not found")
     check = await self.bot.db.fetchrow("SELECT * FROM disablecommand WHERE command = $1 AND guild_id = $2", found_command.name, ctx.guild.id)
     if not check: return await ctx.send_error("This command is **not** disabled")
     await self.bot.db.execute("DELETE FROM disablecommand WHERE guild_id = $1 AND command = $2", ctx.guild.id, found_command.name)     
     await ctx.send_success(f"Enabled command **{found_command.name}**")

    
    @hybrid_command(description="Change the **guild** prefix", usage="[prefix]", help="config", brief="manage guild")
    @utils.get_perms("manage_guild")
    async def prefix(self, ctx: Context, prefix: str):      
       if len(prefix) > 3: return await ctx.send_error("That prefix is **too** long")
       check = await self.bot.db.fetchrow("SELECT * FROM prefixes WHERE guild_id = {}".format(ctx.guild.id)) 
       if check is not None: await self.bot.db.execute("UPDATE prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
       else: await self.bot.db.execute("INSERT INTO prefixes VALUES ($1, $2)", ctx.guild.id, prefix)
       return await ctx.send_success(f"prefix **changed** to `{prefix}`".capitalize())
    
    
async def setup(bot): 
    await bot.add_cog(config(bot))        