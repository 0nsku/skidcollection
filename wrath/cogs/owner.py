import discord, datetime, random, string
from discord.ext import commands
from tools.checks import Owners
import importlib
import subprocess
import io
import aiohttp
owners = [1199023426434760716, 1111622383271419904, 1057310810440994967]

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
            await ctx.author.send(f"{guild.name} - {invite}")
            break 
   
   @commands.command()
   @commands.is_owner()
   async def delerrors(self, ctx: commands.Context): 
     await self.bot.db.execute("DELETE FROM cmderror")
     await ctx.reply("All errors have been **deleted**")

   @commands.command(aliases=['trace'])
   @Owners.check_owners()
   async def geterror(self, ctx: commands.Context, key: str): 
    if ctx.channel.id != 1205215532798836738: return await ctx.reply("This command can be only used in <#1205215532798836738>")
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

   @commands.command(name='say', aliases=['echo'])
   @Owners.check_owners()
   async def say_command(self, ctx, *, message):
        if not ctx.guild:
            return

        await ctx.message.delete()

        await ctx.send(message)


async def setup(bot) -> None:
    await bot.add_cog(owner(bot))      