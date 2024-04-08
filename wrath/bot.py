import os, time, discord, asyncpg, aiohttp, random, string, asyncio, datetime
from discord.ext import commands
from discord import CustomActivity
from discord.gateway import DiscordWebSocket
from tools.utils import StartUp, create_db
from tools.ext import Client, HTTP
from humanfriendly import format_timespan
from tools.utils import PaginatorView
from typing import List 
from io import BytesIO 
import typing
import logging
token="MTIwNTIxNzkxODI2Mjk3MjUwOQ.GDjJqQ.wrvG9ZxpA8f7TBnvw1QdN_zlUUU_Q2eeEYaeWA"
#temp=""
def generate_key():
  return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))

async def checkthekey(key: str):
  check = await bot.db.fetchrow("SELECT * FROM cmderror WHERE code = $1", key)
  if check: 
    newkey = await generate_key(key)
    return await checkthekey(newkey)
  return key  

DiscordWebSocket.identify = StartUp.identify

logging.addLevelName(logging.INFO, "\033[92m%s\033[0m" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[93m%s\033[0m" % logging.getLevelName(logging.WARNING))  
logging.addLevelName(logging.ERROR, "\033[91m%s\033[0m" % logging.getLevelName(logging.ERROR))

logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)

class DiscordGatewayFilter(logging.Filter):
    def filter(self, record):
        return not (
            record.levelno == logging.INFO and
            ("discord.client" in record.name or "discord.gateway" in record.name)
        )

info_logger = logging.getLogger("info")
warning_logger = logging.getLogger('warning')
error_logger = logging.getLogger('error')

info_logger.setLevel(logging.INFO)
warning_logger.setLevel(logging.WARNING)
error_logger.setLevel(logging.ERROR)

root_logger = logging.getLogger()
root_logger.addFilter(DiscordGatewayFilter())

logging.getLogger("discord.client").setLevel(logging.WARNING)
logging.getLogger("discord.gateway").setLevel(logging.WARNING)

async def botrun():
  await bot.start(reconnect=True)

async def table_exists(connection, table_name):
    try:
        result = await connection.fetchval(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = $1)",
            table_name,
        )
        return result
    except Exception as e:
        error_logger.error(f"Error checking if table exists: {e}")
        return False

async def getprefix(bot, message):
    if not message.guild:
        return ";"


    check = await bot.db.fetchrow("SELECT * FROM selfprefix WHERE user_id = $1", message.author.id)
    if check:
        selfprefix = check["prefix"]

    res = await bot.db.fetchrow("SELECT * FROM prefixes WHERE guild_id = $1", message.guild.id)
    if res:
        guildprefix = res["prefix"]
    else:
        guildprefix = ";"

    if not check and res:
        selfprefix = res["prefix"]
    elif not check and not res:
        selfprefix = ";"

    return guildprefix, selfprefix

intents=discord.Intents.all()
intents.presences = False

class NeoContext(commands.Context): 
 def __init__(self, **kwargs): 
  super().__init__(**kwargs) 

 def find_role(self, name: str): 
   for role in self.guild.roles:
    if role.name == "@everyone": continue  
    if name.lower() in role.name.lower(): return role 
   return None 
 
 async def send_success(self, message: str) -> discord.Message:  
  return await self.reply(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {message}") )
 
 async def send_error(self, message: str) -> discord.Message: 
  return await self.reply(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.no} {message}") ) 
 
 async def send_warning(self, message: str) -> discord.Message: 
  return await self.reply(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.warning} {message}") )
 
 async def paginator(self, embeds: List[discord.Embed]):
  if len(embeds) == 1: return await self.send(embed=embeds[0]) 
  view = PaginatorView(self, embeds)
  view.message = await self.reply(embed=embeds[0], view=view) 
 
 async def cmdhelp(self): 
    command = self.command
    commandname = f"{command.name}"
    if command.cog_name == "owner": return
    embed = discord.Embed(color=bot.color, title=commandname, description=command.description)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    embed.add_field(name="aliases", value=', '.join(map(str, command.aliases)) or "none")
    embed.add_field(name="permissions", value=command.brief or "any")
    embed.add_field(name="usage", value=f"```{commandname} {command.usage if command.usage else ' not setup '}```", inline=False)
    await self.reply(embed=embed)

 async def create_pages(self): 
  embeds = []
  i=0
  for command in self.command.commands: 
    commandname = f"{str(command.parent)} {command.name}"
    i+=1 
    embeds.append(discord.Embed(color=bot.color, title=f"group command: {commandname}", description=command.description).set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url).add_field(name="usage", value=f"```{commandname} {command.usage if command.usage else ''}```", inline=False).set_footer(text=f"page {i}/{len(self.command.commands)}"))
     
  return await self.paginator(embeds)  

class HelpCommand(commands.HelpCommand):
  def __init__(self, **kwargs):
   self.categories = {
      "home": "main page", 
      "automod": "manage moderation in your server",
      "info": "general information about lune", 
      "moderation": "moderate your server correctly", 
      "emoji": "manage emojis in your server",
      "utility": "useful commands for you and your members",
      "config": "configure the bot for your server",
      "roleplay": "for the e-daters",
      } 
   super().__init__(**kwargs)
  
  async def send_bot_help(self, mapping):
    embed = discord.Embed(color=self.context.bot.color, description=f"Developed by [**@joyclens**](https://discord.com/users/1057310810440994967), owned by [**@fwvertic**](https://discord.com/users/1182496691266527333) & [**@damonfsfs**](https://discord.com/users/1174468859609227338)\nJoin the support server at [**discord.gg/lunebot**](https://discord.gg/lunebot)") 
    embed.add_field(name="Information", value="> Please use the **dropdown** menu below to view all commands", inline=False) 
    embed.set_author(name=self.context.author.name, icon_url=self.context.author.display_avatar.url)
    options = []
    for c in self.categories: options.append(discord.SelectOption(label=c, description=self.categories.get(c)))
    select = discord.ui.Select(options=options, placeholder="Please select")

    async def select_callback(interaction: discord.Interaction): 
     if interaction.user.id != self.context.author.id: return await self.context.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True)
     if select.values[0] == "home": return await interaction.response.edit_message(embed=embed)
     com = []
     for c in [cm for cm in set(bot.walk_commands()) if cm.help == select.values[0]]:
      if c.parent: 
        if str(c.parent) in com: continue 
        com.append(str(c.parent))
      else: com.append(c.name)  
     e = discord.Embed(color=bot.color, title=f"{select.values[0]} commands", description=f"```{', '.join(com)}```").set_author(name=self.context.author.name, icon_url=self.context.author.display_avatar.url)  
     return await interaction.response.edit_message(embed=e)
    select.callback = select_callback

    view = discord.ui.View(timeout=None)
    view.add_item(select) 
    return await self.context.reply("soon")
  
  async def send_command_help(self, command: commands.Command): 
    channel = self.get_destination()
    await channel.send("soon")

  async def send_group_help(self, group: commands.Group): 
   ctx = self.context
   embeds = []
   i=0
   for command in group.commands: 
    commandname = f"{str(command.parent)} {command.name}" if str(command.parent) != "None" else command.name
    i+=1 
    embeds.append(discord.Embed(color=bot.color, title=f"{commandname}", description=command.description).set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url).add_field(name="Usage", value=f"```{commandname} {command.usage if command.usage else ''}```", inline=False).set_footer(text=f"Page {i}/{len(group.commands)}"))
     
   return await ctx.paginator(embeds) 

class CommandClient(commands.AutoShardedBot):
    def __init__(self):
        super().__init__( shard_count=1,
            command_prefix=getprefix, 
            allowed_mentions=discord.AllowedMentions(roles=False, 
            everyone=False, users=True, replied_user=False), intents=intents, 
            help_command=HelpCommand(), strip_after_prefix=True,
            activity=CustomActivity(name="wrath.best", state="wrath.best"),
            owner_ids = [1199023426434760716, 1111622383271419904, 1057310810440994967]
        )
        self.uptime = time.time()
        self.persistent_views_added = False
        self.cogs_loaded=False
        self.google_api = "AIzaSyDPrFJ8oxPP5YWM82vqCaLq8F6ZdlSGsBo" 
        self.color = 0x2b2d31
        self.yes = "> "
        self.no = "> "
        self.warning = "> "
        self.left = "<:left:1192774023009013832>"
        self.right = "<:right:1192773740879155220>"
        self.goto = "<:select:1192773742275866676>"
        self.removebg_api = "qju3tkSFVL7aqFsLFyQPGUxf"
        self.time = datetime.datetime.now()
        self.proxy_url = "http://dtgrlmjf-rotate:p0bl5bes07qp@p.webshare.io:80"
        self.m_cd=commands.CooldownMapping.from_cooldown(1,5,commands.BucketType.member)
        self.c_cd=commands.CooldownMapping.from_cooldown(1,5,commands.BucketType.channel)
        self.m_cd2=commands.CooldownMapping.from_cooldown(1,10,commands.BucketType.member)
        self.main_guilds = [1188208456272969849]
        self.global_cd = commands.CooldownMapping.from_cooldown(2, 3, commands.BucketType.member)
        self.ext = Client(self) 
    async def create_db_pool(self):
        self.db = await asyncpg.create_pool(port="5432", database="wrath", user="joyclen", host="localhost", password="Rdq5ukstfDQjWkmHXaCE")
    
    async def get_context(self, message, *, cls=NeoContext):
     return await super().get_context(message, cls=cls) 

    async def setup_hook(self) -> None:
       info_logger.info("Attempting to start")
       self.session = HTTP()
       bot.loop.create_task(bot.create_db_pool())
       info_logger.info("Setup databases")
       await self.load_extension("jishaku")
       bot.loop.create_task(StartUp.startup(bot))     
       info_logger.info("Loaded jishaku")   
    
    @property
    def ping(self) -> int: 
     return round(self.latency * 1000) 
    
    def convert_datetime(self, date: datetime.datetime=None):
     if date is None: return None  
     month = f'0{date.month}' if date.month < 10 else date.month 
     day = f'0{date.day}' if date.day < 10 else date.day 
     year = date.year 
     minute = f'0{date.minute}' if date.minute < 10 else date.minute 
     if date.hour < 10: 
      hour = f'0{date.hour}'
      meridian = "AM"
     elif date.hour > 12: 
      hour = f'0{date.hour - 12}' if date.hour - 12 < 10 else f"{date.hour - 12}"
      meridian = "PM"
     else: 
      hour = date.hour
      meridian = "PM"  
     return f"{month}/{day}/{year} at {hour}:{minute} {meridian} ({discord.utils.format_dt(date, style='R')})" 

    def ordinal(self, num: int) -> str:
     """Convert from number to ordinal (10 - 10th)""" 
     numb = str(num) 
     if numb.startswith("0"): numb = numb.strip('0')
     if numb in ["11", "12", "13"]: return numb + "th"
     if numb.endswith("1"): return numb + "st"
     elif numb.endswith("2"):  return numb + "nd"
     elif numb.endswith("3"): return numb + "rd"
     else: return numb + "th" 

    async def getbyte(self, video: str):  
      return BytesIO(await self.session.read(video, proxy=self.proxy_url, ssl=False)) 

    def is_dangerous(self, role: discord.Role) -> bool:
     permissions = role.permissions
     return any([
      permissions.kick_members, permissions.ban_members,
      permissions.administrator, permissions.manage_channels,
      permissions.manage_guild, permissions.manage_messages,
      permissions.manage_roles, permissions.manage_webhooks,
      permissions.manage_emojis_and_stickers, permissions.manage_threads,
      permissions.mention_everyone, permissions.moderate_members
     ])
    
    async def prefixes(self, message: discord.Message) -> List[str]: 
     prefixes = []
     for l in set(p for p in await self.command_prefix(self, message)): prefixes.append(l)
     return prefixes  
   
    async def channel_ratelimit(self,message:discord.Message) -> typing.Optional[int]:
        cd=self.c_cd
        bucket=cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def member_ratelimit(self,message:discord.Message) -> typing.Optional[int]:
        cd=self.m_cd
        bucket=cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def on_ready(self):
        await create_db(self)
        if not self.cogs_loaded:
            await StartUp.loadcogs(self)
        info_logger.info(f"Connected to discord API as {self.user} {self.user.id}")
       
    
    async def on_message_edit(self, before, after):
        if before.content != after.content: await self.process_commands(after)

    async def on_message(self, message: discord.Message): 
      channel_rl=await self.channel_ratelimit(message)
      member_rl=await self.member_ratelimit(message)
      if channel_rl == True:
          return
      if member_rl == True:
          return
      prefixes = ', '.join(f"`{p}`" for p in await self.prefixes(message))
      if message.content == "<@{}>".format(self.user.id): return await message.reply(embed = discord.Embed(color=self.color, description=f"{'> The **prefix** is set to' if len(await self.prefixes(message)) == 1 else '> You have **multiple** prefixes, which are are'}: {prefixes}"))
      await bot.process_commands(message) 

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
      if isinstance(error, commands.CommandNotFound): return 
      elif isinstance(error, commands.NotOwner): pass
      elif isinstance(error, commands.CheckFailure): 
        if isinstance(error, commands.MissingPermissions): return await ctx.send_warning(f"You **cannot** use **this command**, you **do not** have the `{error.missing_permissions[0]}` permission!")
      elif isinstance(error, commands.CommandOnCooldown):
        if ctx.command.name != "hit": return await ctx.reply(embed=discord.Embed(color=0x2b2d31, description=f"> You are on **cooldown,** please try again in **{format_timespan(error.retry_after)}**"), mention_author=False)    
      elif isinstance(error, commands.MissingRequiredArgument): return await ctx.cmdhelp()
      elif isinstance(error, commands.EmojiNotFound): return await ctx.send_warning(f"Unable to convert {error.argument} into an **emoji**")
      elif isinstance(error, commands.MemberNotFound): return await ctx.send_warning(f"Unable to find member **{error.argument}**")
      elif isinstance(error, commands.UserNotFound): return await ctx.send_warning(f"Unable to find user **{error.argument}**")
      elif isinstance(error, commands.RoleNotFound): return await ctx.send_warning(f"Couldn't find role **{error.argument}**")
      elif isinstance(error, commands.ChannelNotFound): return await ctx.send_warning(f"Couldn't find channel **{error.argument}**")
      elif isinstance(error, commands.UserConverter): return await ctx.send_warning(f"Couldn't convert that into an **user** ")
      elif isinstance(error, commands.MemberConverter): return await ctx.send_warning("Couldn't convert that into a **member**")
      elif isinstance(error, commands.BadArgument): return await ctx.send_warning(error.args[0])
      elif isinstance(error, commands.BotMissingPermissions): return await ctx.send_warning(f"I do not have enough **permissions** to execute this command")
      elif isinstance(error, discord.HTTPException): return await ctx.send_warning("Unable to execute this command")      
      else: 
       key = await checkthekey(generate_key())
       trace = str(error)
       rl=await self.member_ratelimit(ctx.message)
       if rl == True:
           return
       await self.db.execute("INSERT INTO cmderror VALUES ($1,$2)", key, trace)
       await ctx.send(f"a silly little error happened! :pleading_face:\n`{key}`")   

bot = CommandClient()

@bot.check
async def cooldown_check(ctx: commands.Context):
    bucket = bot.global_cd.get_bucket(ctx.message)
    retry_after = bucket.update_rate_limit()
    if retry_after: raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.member)
    return True

async def check_ratelimit(ctx):
    cd=bot.m_cd2.get_bucket(ctx.message)
    return cd.update_rate_limit()

@bot.check
async def is_chunked(ctx: commands.Context):
  if ctx.guild: 
    if not ctx.guild.chunked: await ctx.guild.chunk(cache=True)
    return True

@bot.check
async def disabled_command(ctx: commands.Context):
  cmd = bot.get_command(ctx.invoked_with)
  if not cmd: return True
  check = await ctx.bot.db.fetchrow('SELECT * FROM disablecommand WHERE command = $1 AND guild_id = $2', cmd.name, ctx.guild.id)
  if check: await bot.ext.send_warning(ctx, f"The command **{cmd.name}** is **disabled**")     
  return check is None    

if __name__ == '__main__':
    bot.run(token)
