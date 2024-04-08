import discord, datetime, asyncio, random 
from discord.ext import commands 
from discord.ui import Button, View
from tools.checks import Perms 

class MarryView(discord.ui.View): 
   def __init__(self, ctx: commands.Context, member: discord.Member): 
    super().__init__() 
    self.ctx = ctx 
    self.member = member
    self.status = False 

   @discord.ui.button(label="Yes")
   async def yes(self, interaction: discord.Interaction, button: discord.ui.Button): 
    if interaction.user == self.ctx.author: return await interaction.client.ext.send_warning(interaction, "you can't accept your own marriage".capitalize(), ephemeral=True)
    elif interaction.user != self.member: return await self.ctx.bot.ext.send_warning(interaction, "you're **not** the author".capitalize(), ephemeral=True)
    else:   
      await interaction.client.db.execute("INSERT INTO marry VALUES ($1, $2, $3)", self.ctx.author.id, self.member.id, datetime.datetime.now().timestamp())                   
      embe = discord.Embed(color=interaction.client.color, description=f"**{self.ctx.author}** is now married with **{self.member}**")
      await interaction.response.edit_message(content=None, embed=embe, view=None)
      self.status = True              

   @discord.ui.button(label="No")
   async def no(self, interaction: discord.Interaction, button: discord.ui.Button): 
     if interaction.user == self.ctx.author: return await self.ctx.bot.ext.send_warning(interaction, "you can't reject your own marriage".capitalize(), ephemeral=True)
     elif interaction.user != self.member: return await self.ctx.bot.ext.send_warning(interaction, "you're **not** the author".capitalize(), ephemeral=True)
     else:                         
        embe = discord.Embed(color=interaction.client.color, description=f"Sorry **{self.ctx.author}**, maybe **{self.member}** isnt your piece of cake")
        await interaction.response.edit_message(content=None, embed=embe, view=None)
        self.status = True 
   
   async def on_timeout(self):
     if self.status == False:
      embed = discord.Embed(color=0xd3d3d3, description=f"**{self.member}** didn't reply in time 😥")  
      try: await self.message.edit(content=None, embed=embed, view=None)  
      except: pass 

class roleplay(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot 
        self.joint_emoji = "🍃"
        self.smoke = "🌬️" 
        self.joint_color = 0x57D657
        self.book = "📖" 

    @commands.hybrid_command(description="kiss an user", usage="[member]", help="roleplay")
    async def kiss(self, ctx: commands.Context, *, member: discord.Member):
     lol = await self.bot.session.json("http://api.nekos.fun:8080/api/kiss")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** kissed **{member.name}** 😘")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="cuddle an user", usage="[member]", help="roleplay")
    async def cuddle(self, ctx, *, member: discord.Member):
     lol = await self.bot.session.json("http://api.nekos.fun:8080/api/cuddle")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** cuddled **{member.name}** 🥰")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="hug an user", usage="[member]", help="roleplay")
    async def hug(self, ctx: commands.Context, *, member: discord.Member): 
     lol = await self.bot.session.json(f"http://api.nekos.fun:8080/api/{ctx.command.name}")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** hugged **{member.name}** 🥰")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="pat an user", usage="[member]", help="roleplay")
    async def pat(self, ctx, *, member: discord.Member):
     lol = await self.bot.session.json(f"http://api.nekos.fun:8080/api/{ctx.command.name}")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** pats **{member.name}** 🥰")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="slap an user", usage="[member]", help="roleplay")
    async def slap(self, ctx, *, member: discord.Member): 
     lol = await self.bot.session.json(f"http://api.nekos.fun:8080/api/{ctx.command.name}")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** slaps **{member.name}** 😯")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="start laughing", help="roleplay")
    async def laugh(self, ctx): 
     lol = await self.bot.session.json(f"http://api.nekos.fun:8080/api/{ctx.command.name}")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** laughs 🤣")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="start crying", help="roleplay")
    async def cry(self, ctx):
     lol = await self.bot.session.json(f"http://api.nekos.fun:8080/api/{ctx.command.name}")
     embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** cries 😭")
     embed.set_image(url=lol["image"])
     return await ctx.reply(embed=embed)

    @commands.hybrid_command(description="marry an user", help="roleplay", usage="[user]")
    async def marry(self, ctx: commands.Context, *, member: discord.Member):
     if member == ctx.author: return await ctx.send_error("You can't **marry** yourself")
     elif member.bot: return await ctx.send_error("bots cant consent".capitalize())  
     else: 
        meri = await self.bot.db.fetchrow("SELECT * FROM marry WHERE author = $1", member.id)
        if meri is not None: return await ctx.send_warning(f"**{member}** is already married")
        elif meri is None:
           mer = await self.bot.db.fetchrow("SELECT * FROM marry WHERE soulmate = $1", member.id)
           if mer is not None: return await ctx.send_warning(f"**{member}** is already married")
                    
        check = await self.bot.db.fetchrow("SELECT * FROM marry WHERE author = $1", ctx.author.id) 
        if check is not None: return await ctx.send_warning("You are already **married**")
        elif check is None:
           check2 = await self.bot.db.fetchrow("SELECT * FROM marry WHERE soulmate = $1", ctx.author.id) 
           if check2 is not None: await ctx.send_warning("You are already **married**")
           else:
             embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.mention}** wants to marry you, do you accept?")
             view = MarryView(ctx, member)
             view.message = await ctx.reply(content=member.mention, embed=embed, view=view)
    
    @commands.hybrid_command(description="check an user's marriage", usage="<member>", help="roleplay")
    async def marriage(self, ctx: commands.Context, *, member: discord.User=None):
      if member is None: member = ctx.author
      check = await self.bot.db.fetchrow("SELECT * FROM marry WHERE author = $1", member.id)       
      if check is None:
           check2 = await self.bot.db.fetchrow("SELECT * FROM marry WHERE soulmate = $1", member.id)
           if check2 is None: return await ctx.send_error(f"{'**You** are' if member == ctx.author else f'**{member.name}** is'} not **married**")
           elif check2 is not None:
            embed = discord.Embed(color=self.bot.color, description=f"> {f'**{member}** is' if member != ctx.author else '**You** are'} currently married to **{await self.bot.fetch_user(int(check2[0]))}** since **{self.bot.ext.relative_time(datetime.datetime.fromtimestamp(int(check2['time'])))}**")
            return await ctx.reply(embed=embed)  
      elif check is not None:
         embed = discord.Embed(color=self.bot.color, description=f"> {f'**{member}** is' if member != ctx.author else '**You** are'} currently married to **{await self.bot.fetch_user(int(check[1]))}** since **{self.bot.ext.relative_time(datetime.datetime.fromtimestamp(int(check['time'])))}**")
         return await ctx.reply(embed=embed)   

    @commands.hybrid_command(description="divorce with an user", help="roleplay")
    async def divorce(self, ctx: commands.Context):       
        check = await self.bot.db.fetchrow("SELECT * FROM marry WHERE author = $1", ctx.author.id)
        if check is None:
           check2 = await self.bot.db.fetchrow("SELECT * FROM marry WHERE soulmate = $1", ctx.author.id)
           if check2 is None: return await ctx.send_error("You're **not** married")

        button1 = Button(label="Yes", style=discord.ButtonStyle.grey)
        button2 = Button(label="No", style=discord.ButtonStyle.grey)
        embed = discord.Embed(color=self.bot.color, description=f"> **{ctx.author.mention}** are you sure you want to divorce?")
        async def button1_callback(interaction):
         if interaction.user != ctx.author: return await self.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True) 
         if check is None:
            if check2 is not None: await self.bot.db.execute("DELETE FROM marry WHERE soulmate = $1", ctx.author.id)
         elif check is not None: await self.bot.db.execute("DELETE FROM marry WHERE author = $1", ctx.author.id)                    
         embe = discord.Embed(color=self.bot.color, description=f"> **{ctx.author.mention}** divorced with their partner")
         await interaction.response.edit_message(content=None, embed=embe, view=None)       
        button1.callback = button1_callback  

        async def button2_callback(interaction):
          if interaction.user != ctx.author: return await self.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True)                       
          embe = discord.Embed(color=self.bot.color, description=f"> **{ctx.author.mention}** you changed your mind")
          await interaction.response.edit_message(content=None, embed=embe, view=None)
        button2.callback = button2_callback  

        marry = View()
        marry.add_item(button1)
        marry.add_item(button2)
        await ctx.reply(embed=embed, view=marry)      
    
async def setup(bot) -> None:
    await bot.add_cog(roleplay(bot))        
