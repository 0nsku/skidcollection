import json, discord
from discord.ext import commands 
owners = [1199023426434760716, 1111622383271419904, 1057310810440994967]

class Boosts: 
 
  def get_level(boosts: int): 
   async def predicate(ctx: commands.Context): 
    if ctx.guild.premium_subscription_count < boosts: await ctx.send_warning( f"{ctx.guild.name} needs **{boosts}** boosts to use this command") 
    return ctx.guild.premium_subscription_count >= boosts 
   return commands.check(predicate)

class Mod: 

  def is_mod_configured(): 
   async def predicate(ctx: commands.Context): 
    check = await ctx.bot.db.fetchrow("SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id)
    if not check: 
     await ctx.send_warning( f"Jail is **not** **setup** in this server, please use `{ctx.clean_prefix}setupjail` to initialize it")
     return False
    return True
   return commands.check(predicate)

  async def check_role_position(ctx: commands.Context, role: discord.Role) -> bool: 
   if (role.position >= ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id) or not role.is_assignable(): 
    await ctx.send_warning( "Unable to **manage** this role")
    return False 
   return True

  async def check_hieracy(ctx: commands.Context, member: discord.Member) -> bool: 
   if member.id == ctx.bot.user.id: 
    if ctx.command.name != "nickname":
     await ctx.reply("why") 
     return False
   if (ctx.author.top_role.position <= member.top_role.position and ctx.guild.owner_id != ctx.author.id) or ctx.guild.me.top_role <= member.top_role or (member.id == ctx.guild.owner_id and ctx.author.id != member.id): 
    await ctx.send_warning( "You're unable to perform this action on **{}**".format(member))
    return False  
   return True 
  
class Messages: 

  
  def good_message(message: discord.Message, trigger: str) -> bool:
        if not message.guild or message.author.bot or message.content == "":
            return False

        content_lower = message.content.lower()

        trigger_lower = trigger.lower()

        if trigger_lower in content_lower:
            return True

        return False

class Owners: 
  def check_owners(): 
   async def predicate(ctx: commands.Context): 
    return ctx.author.id in owners
   return commands.check(predicate)   

class Perms: 

  def server_owner(): 
   async def predicate(ctx: commands.Context): 
    if ctx.author.id != ctx.guild.owner_id: 
      await ctx.send_warning( f"Only the **guild owner** can use this command") 
      return False 
    return True   
   return commands.check(predicate)   
  
  def check_whitelist(module: str):
   async def predicate(ctx: commands.Context):
    if ctx.guild is None: return False 
    if ctx.author.id == ctx.guild.owner.id: return True
    check = await ctx.bot.db.fetchrow("SELECT * FROM whitelist WHERE guild_id = $1 AND object_id = $2 AND mode = $3 AND module = $4", ctx.guild.id, ctx.author.id, "user", module)   
    if check is None: 
     await ctx.send_warning( f"Whitelist not found for **{module}**") 
     return False      
    return True
   return commands.check(predicate) 

  def get_perms(perm: str=None):
   async def predicate(ctx: commands.Context):  
    if perm is None: return True 
    if ctx.guild.owner == ctx.author: return True
    if ctx.author.guild_permissions.administrator: return True
    for r in ctx.author.roles:
     if perm in [str(p[0]) for p in r.permissions if p[1] is True]: return True 
     check = await ctx.bot.db.fetchrow("SELECT permissions FROM fake_permissions WHERE role_id = $1 and guild_id = $2", r.id, r.guild.id)
     if check is None: continue 
     permissions = json.loads(check[0])
     if perm in permissions or "administrator" in permissions: return True
    raise commands.MissingPermissions([perm])
   return commands.check(predicate)  

  async def has_perms(ctx: commands.Context, perm: str=None): 
    if perm is None: return True 
    if ctx.guild.owner == ctx.author: return True
    if ctx.author.guild_permissions.administrator: return True
    for r in ctx.author.roles:
     if perm in [str(p[0]) for p in r.permissions if p[1] is True]: return True 
     check = await ctx.bot.db.fetchrow("SELECT permissions FROM fake_permissions WHERE role_id = $1 and guild_id = $2", r.id, r.guild.id)
     if check is None: continue 
     permissions = json.loads(check[0])
     if perm in permissions or "administrator" in permissions: return True
    return False   