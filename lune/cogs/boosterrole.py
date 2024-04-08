import asyncio
from discord.ext import commands 
from discord import Interaction, Embed, Role, PartialEmoji, Member
from discord.ext.commands import Cog, Context, group, hybrid_command, hybrid_group, command, AutoShardedBot as AB, has_guild_permissions 
import matplotlib
from discord.ext.commands import (
  Converter, 
  BadArgument, 
  MemberConverter, 
  RoleConverter, 
  BotMissingPermissions,
  check
)
import string
from typing import Union
from pydantic import BaseModel

def boosted_to(level: int):
  async def predicate(ctx: Context):
   if ctx.guild.premium_tier < level: 
    await ctx.send_warning(f"The server has to be boosted to level **{level}** to be able to use this command")
   return ctx.guild.premium_tier >= level
  return check(predicate)

def br_is_configured():
  async def predicate(ctx: Context):
    check = await ctx.bot.db.fetchrow('SELECT * FROM booster_module WHERE guild_id = $1', ctx.guild.id)
    if not check: 
      await ctx.send_warning("Booster roles are **not** configured")
    return check is not None 
  return check(predicate)  

def has_br_role():
  async def predicate(ctx: Context): 
    check = await ctx.bot.db.fetchrow("SELECT * FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    if not check: 
      await ctx.send_warning(f"You do not have a booster role set\nPlease use `{ctx.clean_prefix}br create` to create a booster role") 
    return check is not None 
  return check(predicate)

class ColorSchema(BaseModel):
  """
  Schema for colors
  """

  hex: str 
  value: int

class HexColor(Converter): 
 async def convert(self, ctx: Context, argument: str) -> ColorSchema: 
    if argument in ['pfp', 'avatar']:
      dominant = await ctx.bot.dominant_color(ctx.author.display_avatar)
      payload = {
        "hex": hex(dominant).replace("0x", "#"), 
        "value": dominant
      }
    else:
      color = matplotlib.colors.cnames.get(argument)
      
      if not color: 
        color = argument.replace("#", "")
        digits = set(string.hexdigits)
        if not all(c in digits for c in color):
          raise BadArgument("This is not a hex code")
      
      color = color.replace("#", "") 
      payload = {
        'hex': f"#{color}", 
        'value': int(color, 16)
      }
    
    return ColorSchema(**payload)

class Boosterrole(Cog): 
  def __init__(self, bot: commands.AutoShardedBot):
    self.bot = bot 
    self.description = "Manage your personal booster role"
  
  @Cog.listener('on_guild_role_delete')
  async def br_award_deleted(self, role: Role):
      await self.bot.db.execute("DELETE FROM br_award WHERE role_id = $1", role.id)
  
  @Cog.listener('on_member_update')
  async def give_br_award(self, before: Member, after: Member):
    if not before.guild.premium_subscriber_role in before.roles and before.guild.premium_subscriber_role in after.roles: 
      if results := await self.bot.db.fetchrow("SELECT role_id FROM br_award WHERE guild_id = $1", before.guild.id):
        roles = [after.guild.get_role(result['role_id']) for result in results if after.guild.get_role(result['role_id']).is_assignable()]
        await asyncio.gather(*[after.add_roles(role, reason="Booster role awarded given") for role in roles])
    elif before.guild.premium_subscriber_role in before.roles and not after.guild.premium_subscriber_role in after.roles: 
      if results := await self.bot.db.fetchrow("SELECT role_id FROM br_award WHERE guild_id = $1", before.guild.id):
        roles = [
          after.guild.get_role(result['role_id']) for result in results 
          if after.guild.get_role(result['role_id']).is_assignable()
          and after.guild.get_role(result['role_id']) in after.roles
        ]

        await asyncio.gather(*[after.remove_roles(role, reason="Removing booster awards from this member") for role in roles])

  @group(invoke_without_command=True, aliases=['br']) 
  async def boosterrole(self, ctx):
    await ctx.create_pages()

  @boosterrole.command(name="setup", brief="manage guild")
  @has_guild_permissions(manage_guild=True)
  async def br_setup(self, ctx: Context):
    """
    Setup the booster role module
    """

    if await self.bot.db.fetchrow("SELECT * FROM booster_module WHERE guild_id = $1", ctx.guild.id):
      return await ctx.send_warning("Booster Role is **already** setup!")

    await self.bot.db.execute("INSERT INTO booster_module (guild_id) VALUES ($1)", ctx.guild.id)
    return await ctx.send_success("Booster Role is now **setup**!")

  @boosterrole.command(name="reset", brief="manage guild")
  @has_guild_permissions(manage_guild=True)
  @br_is_configured()
  async def br_reset(self, ctx: Context): 
    """
    Disable the booster role module
    """

    async def yes_callback(interaction: Interaction):
      await self.bot.db.execute("DELETE FROM booster_module WHERE guild_id = $1", ctx.guild.id)
      await self.bot.db.execute("DELETE FROM booster_roles WHERE guild_id = $1", ctx.guild.id)        
      return await interaction.response.edit_message(
        embed=Embed(color=self.bot.yes_color, description=f"{self.bot.yes} {ctx.author.mention}: Booster Role has been **fully cleared**."), 
        view=None
      )

    async def no_callback(interaction: Interaction): 
      return await interaction.response.edit_message(
        embed=Embed(color=self.bot.yes_color, description="Cancelled Action."),
        view=None
      ) 

    await ctx.confirmation_send(
      "Are you sure you want to unset the boosterrole? You are **unable** to **revert this!**",
      yes_callback, 
      no_callback
    )     

  @boosterrole.command(name="base", brief="manage guild")
  @has_guild_permissions(manage_guild=True)
  @br_is_configured()
  async def br_base(self, ctx: Context, *, role: Role=None):
    """
    Create the booster roles above the given role
    """

    check = await self.bot.db.fetchrow("SELECT base FROM booster_module WHERE guild_id = $1", ctx.guild.id)      
    if role is None:
      if check is None: 
        return await ctx.send_warning("Booster Role **base role* hasn't been created!\n") 
      
      await self.bot.db.execute("UPDATE booster_module SET base = $1 WHERE guild_id = $2", None, ctx.guild.id) 
      return await ctx.send_success("The **base** role has been **removed**.")
    
    await self.bot.db.execute("UPDATE booster_module SET base = $1 WHERE guild_id = $2", role.id, ctx.guild.id) 
    return await ctx.send_success(f"{role.mention} has been **set** as the **base role**\n>>> *All booster roles will be created under this role*")
  
  @boosterrole.command(name="create", brief="server booster")
  @br_is_configured()
  async def br_create(self, ctx: Context, *, name: str=None):
    """
    Create a booster role
    """

    if not ctx.author.premium_since: 
      return await ctx.send_warning("You need to **boost** this **server** to use **booster role!**")
    
    che = await self.bot.db.fetchval("SELECT base FROM booster_module WHERE guild_id = $1", ctx.guild.id)

    if not name: 
      name = f"{ctx.author.name}'s role" 

    if await self.bot.db.fetchrow("SELECT * FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id): 
      return await ctx.send_warning(f"You **already** have an **existing** booster role!")
    
    ro = ctx.guild.get_role(che)
    role = await ctx.guild.create_role(name=name)
    await role.edit(position=ro.position if ro is not None else 1)
    await ctx.author.add_roles(role)
    await self.bot.db.execute(
      """
      INSERT INTO booster_roles 
      VALUES ($1,$2,$3)
      """, 
      ctx.guild.id, 
      ctx.author.id, 
      role.id
    )
    await ctx.send_success("Your **booster role** has been **created!**")
  
  @boosterrole.command(name="name", brief="server booster")
  @has_br_role()
  async def br_name(self, ctx: Context, *, name: str):
    """
    Edit your booster role name
    """

    if len(name) > 32: 
      return await ctx.send_warning("Please provide a name **less** than **32 characters**")
    
    role = ctx.guild.get_role(
      await self.bot.db.fetchval("SELECT role_id FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    )
    if not role:
      return await ctx.send_warning(f"Unable to find your **booster role!**\nPlease use `{ctx.clean_prefix}br delete` then `{ctx.clean_prefix}br create`")
    
    await role.edit(
      name=name,
      reason="Edited booster role name"
    )
    await ctx.send_success(f"Your **booster role** name has been updated to: **{name}**")

  @boosterrole.command(name="color", brief="server booster")
  @has_br_role()
  async def br_color(self, ctx: Context, *, color: HexColor):
    """
    Edit the booster role color
    """

    role = ctx.guild.get_role(
      await self.bot.db.fetchval("SELECT role_id FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    )
    if not role:
      return await ctx.send_warning(
        f"Unable to find your **booster role!**\nPlease use `{ctx.clean_prefix}br delete` then `{ctx.clean_prefix}br create`"
      )

    await role.edit(
      color=color.value,
      reason="Edited booster role color"
    )   
    await ctx.send(embed=Embed(
      color=color.value, 
      description=f"{ctx.author.mention}: Your **booster role** color has been updated to: `{color.hex}`"
    ))

  @boosterrole.command(name="icon", brief="server booster")
  @has_br_role()
  @boosted_to(2)
  async def br_icon(self, ctx: Context, *, emoji: Union[PartialEmoji, str]): 
    """
    Edit the booster role icon
    """

    role = ctx.guild.get_role(
      await self.bot.db.fetchval("SELECT role_id FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    )
    if not role:
      return await ctx.send_warning(
        f"Unable to find your **booster role!**\nPlease use `{ctx.clean_prefix}br delete` then `{ctx.clean_prefix}br create`"
      )
    
    await role.edit(
      display_icon=await emoji.read() if isinstance(emoji, PartialEmoji) else emoji,
      reason="Edited the booster role icon"
    )
    return await ctx.send_success(f"Booster Role **icon** changed to: **{emoji.name if isinstance(emoji, PartialEmoji) else emoji}**")

  @boosterrole.command(name="delete", brief="server booster")
  @has_br_role()
  async def br_delete(self, ctx: Context):
    """
    Delete your booster role
    """

    role = ctx.guild.get_role(
      await self.bot.db.fetchval("SELECT role_id FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    )  

    if role: 
      await role.delete(reason="Booster role deleted")

    await self.bot.db.execute("DELETE FROM booster_roles WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
    return await ctx.send_success("Your **booster role** has been **deleted!**")   
  
  @boosterrole.command(name="list")
  async def br_list(self, ctx: Context): 
    """
    Show all booster roles
    """
    
    results = await self.bot.db.fetch("SELECT * FROM booster_roles WHERE guild_id = $1", ctx.guild.id)
    if len(results) == 0: 
      return await ctx.send_error("No **booster roles** found in this server")

    return await ctx.paginate(
      [f"<@&{result['role_id']}> owned by <@!{result['user_id']}>" for result in results],
      f"Booster Roles ({len(results)})",
      {"name": ctx.guild.name, "icon_url": ctx.guild.icon}
    )     
  
async def setup(bot) -> None: 
  return await bot.add_cog(Boosterrole(bot))  
