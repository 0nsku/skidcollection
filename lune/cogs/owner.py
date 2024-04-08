import discord, datetime, random, string
from discord.ext import commands
from tools.checks import Owners
import importlib
import subprocess
import io
import aiohttp
from bot import info_logger
owners = [1057310810440994967, 1111622383271419904]

class owner(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
       self.bot = bot           

   @commands.command(aliases=["guilds"])
   @Owners.check_owners()
   async def servers(self, ctx: commands.Context): 
            def key(s): 
              return s.member_count 
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            lis = [g for g in self.bot.guilds]
            lis.sort(reverse=True, key=key)
            for guild in lis:
              mes = f"{mes}`{k}` {guild.name} ({guild.id}) - ({guild.member_count})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=self.bot.color, title=f"Servers ({len(self.bot.guilds)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            number.append(discord.Embed(color=self.bot.color, title=f"Servers ({len(self.bot.guilds)})", description=messages[i]))
            await ctx.paginator(number)  

   @commands.command()
   @Owners.check_owners()
   async def portal(self, ctx, id: int):
      await ctx.message.delete()      
      guild = self.bot.get_guild(id)
      for c in guild.text_channels:
        if c.permissions_for(guild.me).create_instant_invite: 
            invite = await c.create_invite()
            await ctx.author.send(f"{guild.name} Invite: {invite}")
            break 
   
   @commands.command()
   @commands.is_owner()
   async def delerrors(self, ctx: commands.Context): 
     await self.bot.db.execute("DELETE FROM cmderror")
     await ctx.reply("All errors have been **deleted**")

   @commands.command(aliases=['trace'])
   @Owners.check_owners()
   async def geterror(self, ctx: commands.Context, key: str): 
    if ctx.channel.id != 1188211136022200361: return await ctx.reply("This command can be only used in <#1188211136022200361>")
    check = await self.bot.db.fetchrow("SELECT * FROM cmderror WHERE code = $1", key)
    if not check: return await ctx.send_error(f"No error associated with the key `{key}`")  
    embed = discord.Embed(color=self.bot.color, title=f"Error {key}", description=f"```{check['error']}```")
    await ctx.reply(embed=embed) 

   @commands.command()
   @commands.is_owner()
   async def leaveguild(self, ctx, guild: int):
        guild = self.bot.get_guild(int(guild))
        await guild.leave()
        await ctx.send_success(f"`{guild.name}` has been **left**")

   @commands.command()
   @Owners.check_owners()
   async def export(self, ctx: commands.Context):
    parts = list()

    output_header = "Support @ https://discord.gg/lunehq\nDefault Prefix: ; | () = Required, <> = Optional\n\n"
    parts.append(output_header)

    for cog in sorted([self.bot.get_cog(cog) for cog in self.bot.cogs if self.bot.get_cog(cog).get_commands() and self.bot.get_cog(cog).qualified_name not in ('Jishaku', 'Developer')], key=lambda c: c.qualified_name[:2]):
        parts.append(f"\n### {cog.qualified_name.replace('_', ' ')} ###")
        for cmd in cog.get_commands():
            parts.append(f"{cmd.qualified_name}" + (f"[{'|'.join(cmd.aliases)}]" if cmd.aliases else "") + f": {cmd.description}")
            if hasattr(cmd, 'commands'):
                for c in cmd.walk_commands():
                    parts.append(f"  - {c.qualified_name}" + (f"[{'|'.join(c.aliases)}]" if c.aliases else "") + f": {c.description}")

    with open('commands.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(parts))

    await ctx.send(file=discord.File('commands.txt'))


   @commands.command(name="sql")
   @Owners.check_owners()
   async def execute_sql(self, ctx, table_name: str, *values):
        """
        Execute a SQL command to insert values into a specified table.

        Example usage:
        ;sql hardban 123456789012345678 987654321098765432 111111111111111111
        """
        try:
            values = [int(value) for value in values]

            query = f"INSERT INTO {table_name} VALUES ({', '.join(map(str, values))})"
            
            await self.bot.db.execute(query)

            await ctx.send(f"Successfully inserted values into `{table_name}` table.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

   @commands.command(name='devhardban')
   @Owners.check_owners()
   async def dev_hardban(self, ctx, user_id):
    guild_id = ctx.guild.id
    author_id = ctx.bot.user.id

    await self.bot.db.execute("INSERT INTO developerhardban (guild_id, banned, author) VALUES ($1, $2, $3)", guild_id, int(user_id), author_id)
    
    await ctx.send_success(f"User with ID **{user_id}** has been **added** to the developer hardban list.")

   @commands.command(name='devhardunban')
   @Owners.check_owners()
   async def dev_hardunban(self, ctx, user_id):
    guild_id = ctx.guild.id

    await self.bot.db.execute("DELETE FROM developerhardban WHERE guild_id = $1 AND banned = $2", guild_id, int(user_id))

    await ctx.send_success(f"User with ID **{user_id}** has been **removed** from the developer hardban list.")

   @commands.command(name='devhardbanlist')
   @Owners.check_owners()
   async def dev_hardban_list(self, ctx):
    guild_id = ctx.guild.id

    hardbans = await self.bot.db.fetch("SELECT * FROM developerhardban WHERE guild_id = $1", guild_id)

    embed = discord.Embed(title="Developer Hardbanned Users", color=self.bot.color, description="")

    for index, hardban in enumerate(hardbans, start=1):
        user_id = hardban["banned"]

        user = self.bot.get_user(user_id)
        
        embed.description += f"{index}. {user.name if user else 'Unknown User'} ({user_id})\n"

    await ctx.send(embed=embed)

   @commands.command(name='say', aliases=['echo'])
   @Owners.check_owners()
   async def say_command(self, ctx, *, message):
        if not ctx.guild:
            return

        await ctx.message.delete()

        await ctx.send(message)

   @commands.command(name='joysnap')
   async def joysnap(self, ctx):

        await ctx.send("add joy on snap [@joyclenlols](https://snapchat.com/add/joyclenlols)")

   @commands.group(invoke_without_command=True)
   @Owners.check_owners()
   async def premium(self, ctx: commands.Context):
    await ctx.create_pages()

   @premium.command()
   @Owners.check_owners()
   async def add(self, ctx: commands.Context, *, member: discord.User): 
       result = await self.bot.db.fetchrow("SELECT * FROM donor WHERE user_id = {}".format(member.id))
       if result is not None: return await ctx.reply(f"{member} is already a **premium** subscriber")
       ts = int(datetime.datetime.now().timestamp()) 
       await self.bot.db.execute("INSERT INTO donor VALUES ($1,$2)", member.id, ts)
       return await ctx.send_success(f"{member.mention} is now a **premium** subscriber")

   @premium.command()
   @Owners.check_owners()
   async def remove(self, ctx: commands.Context, *, member: discord.User):    
       result = await self.bot.db.fetchrow("SELECT * FROM donor WHERE user_id = {}".format(member.id)) 
       if result is None: return await ctx.reply(f"{member} isn't a **premium** subscriber")
       await self.bot.db.execute("DELETE FROM donor WHERE user_id = {}".format(member.id))
       return await ctx.send_success(f"{member.mention} is not a **premium** subscriber anymore")


async def setup(bot) -> None:
    await bot.add_cog(owner(bot)) 
