import discord, asyncio
from discord.ext import commands
from typing import Union
from io import BytesIO
from tools.checks import Perms as utils

class Emoji(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
      self.bot = bot

   @commands.command(description="Delete an emoji", help="emoji", usage="[emoji]", brief="manage emojis", aliases=["delemoji"])
   @utils.get_perms("manage_guild")
   async def deleteemoji(self, ctx: commands.Context, emoji: discord.Emoji): 
    await emoji.delete()
    await ctx.send_success("Deleted the emoji")  

   @commands.command(description="Add an emoji", help="emoji", usage="[emoji] <name>", brief="manage emojis", aliases=['steal'])
   @utils.get_perms("manage_guild")
   async def addemoji(self, ctx: commands.Context, emoji: Union[discord.Emoji, discord.PartialEmoji], *, name: str=None):
    if not name: name = emoji.name 
    try:
     emoji = await ctx.guild.create_custom_emoji(image=await emoji.read(), name=name)
     await ctx.send_success(f"Added emoji `{name}` | {emoji}".capitalize())
    except discord.HTTPException as e: return await ctx.send_error(ctx, f"**Unable** to **add** that **emoji**\n> {e}")

   @commands.command(description="Add multiple emojis", help="emoji", usage="[emojis]", aliases=["am"], brief="manage emojis")
   @utils.get_perms("manage_guild")
   async def addmultiple(self, ctx: commands.Context, *emoji: Union[discord.Emoji, discord.PartialEmoji]): 
    if len(emoji) == 0: return await ctx.send_warning("Please give me **emojis** to **add**")       
    emojis = []
    await ctx.channel.typing()
    for emo in emoji:
       try:
         emoj = await ctx.guild.create_custom_emoji(image=await emo.read(), name=emo.name)
         emojis.append(f"{emoj}")
         await asyncio.sleep(.5)
       except discord.HTTPException as e: return await ctx.send_error(ctx, f"**Unable** to **add** that **emoji**\n> {e}")

    embed = discord.Embed(color=self.bot.color, title=f"Added {len(emoji)} emojis") 
    embed.description = "".join(map(str, emojis))    
    return await ctx.reply(embed=embed)
   
   @commands.group(invoke_without_command=True, help="emoji", description="Manage the servers stickers")
   async def sticker(self, ctx: commands.Context): 
    return await ctx.create_pages()

   @sticker.command(name="steal", help="emoji", description="Add a sticker", aliases=['add'], usage="[attach sticker]", brief="manage emojis")
   @utils.get_perms("manage_guild")
   async def sticker_steal(self, ctx: commands.Context): 
    return await ctx.invoke(self.bot.get_command('stealsticker'))  
   
   @sticker.command(name="enlarge", aliases=['e', 'jumbo'], help="emoji", description="Show enlarged sticker", usage="[attach sticker]")
   async def sticker_enlarge(self, ctx: commands.Context): 
    if ctx.message.stickers: stick = ctx.message.stickers[0]
    else: 
     messages = [m async for m in ctx.channel.history(limit=20) if m.stickers]  
     if len(messages) == 0: return await ctx.send_warning("No **sticker** found")
     stick = messages[0].stickers[0]
    return await ctx.reply(file=await stick.to_file(filename=f"{stick.name}.png"))

   @sticker.command(name="delete", help="emoji", description="Delete a sticker", usage="[attach sticker]", brief="manage emojis")
   @utils.get_perms("manage_guild")
   async def sticker_delete(self, ctx: commands.Context): 
    if ctx.message.stickers: 
     sticker = ctx.message.stickers[0]
     sticker = await sticker.fetch() 
     if sticker.guild.id != ctx.guild.id: return await ctx.send_warning("That **sticker** is **not** from **this server**")
     await sticker.delete(reason=f"sticker deleted by {ctx.author}") 
     return await ctx.send_success("Deleted the sticker")
    async for message in ctx.channel.history(limit=10): 
      if message.stickers: 
        sticker = message.stickers[0]
        s = await sticker.fetch()
        if s.guild_id == ctx.guild.id: 
         embed = discord.Embed(color=self.bot.color, description=f"Are you sure you want to delete `{s.name}`?").set_image(url=s.url)
         button1 = discord.ui.Button(emoji="<:tick:1208542339132432385>")
         button2 = discord.ui.Button(emoji="<:cross:1208542342504517702>")
         async def button1_callback(interaction: discord.Interaction): 
          if ctx.author.id != interaction.user.id: return await self.bot.ext.send_warning(interaction, "You're **not** the author")
          await s.delete()
          return await interaction.response.edit_message(embed=discord.Embed(color=self.bot.color, description=f"{self.bot.yes} {interaction.user.mention}: Deleted sticker"), view=None)   
         
         async def button2_callback(interaction: discord.Interaction): 
           if ctx.author.id != interaction.user.id: return await self.bot.ext.send_warning(interaction, "You're **not** the author")
           return await interaction.response.edit_message(embed=discord.Embed(color=self.bot.color, description=f"{interaction.user.mention}"))
         
         button1.callback = button1_callback
         button2.callback = button2_callback 
         view = discord.ui.View()
         view.add_item(button1)
         view.add_item(button2)
         return await ctx.reply(embed=embed, view=view)
         
   @commands.command(description="Add a sticker to the server", help="emoji", usage="[attach sticker]", brief="manage emojis", aliases=["stickersteal", "addsticker", "stickeradd"])
   @utils.get_perms("manage_guild")
   async def stealsticker(self, ctx: commands.Context):
     if ctx.message.stickers:
      try:
       url = ctx.message.stickers[0].url
       name = ctx.message.stickers[0].name
       img_data = await self.bot.session.read(url)
       tobytess = BytesIO(img_data)
       file = discord.File(fp=tobytess)
       sticker = await ctx.guild.create_sticker(name=name, description=name, emoji="skull", file=file, reason=f"sticker created by {ctx.author}")
       format = str(sticker.format) 
       form = format.replace("StickerFormatType.", "")
       embed = discord.Embed(color=self.bot.color, title="Sticker Added")
       embed.set_image(url=url)
       return await ctx.reply(embed=embed)
      except Exception as error: return await ctx.send_error(ctx, f"**Unable** to **add** that **emoji**")
     elif not ctx.message.stickers:
      async for message in ctx.channel.history(limit=10):
       if message.stickers:
        e = discord.Embed(color=self.bot.color, title=message.stickers[0].name).set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
        e.set_image(url=message.stickers[0].url)
        e.set_footer(text="Please use the buttons below")
        button1 = discord.ui.Button(label="", style=discord.ButtonStyle.gray, emoji="<:tick:1208542339132432385>")
        button2 = discord.ui.Button(label="", style=discord.ButtonStyle.gray, emoji="<:cross:1208542342504517702>")
        
        async def button1_callback(interaction: discord.Interaction): 
          if interaction.user != ctx.author: return await self.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True)
          try:
           url = message.stickers[0].url
           name = message.stickers[0].name
           img_data = await self.bot.session.read(url)
           tobytess = BytesIO(img_data)
           file = discord.File(fp=tobytess)
           sticker = await ctx.guild.create_sticker(name=name, description=name, emoji="skull", file=file, reason=f"sticker created by {ctx.author}")
           format = str(sticker.format) 
           form = format.replace("StickerFormatType.", "")
           embed = discord.Embed(color=self.bot.color, title="Sticker Added")
           embed.set_image(url=url)
           return await interaction.response.edit_message(embed=embed, view=None)
          except:
           embed = discord.Embed(color=self.bot.color, description=f"{self.bot.no} {ctx.author.mention}: **Unable** to **add** this **sticker**")
           return await interaction.response.edit_message(embed=embed, view=None)

        button1.callback = button1_callback 

        async def button2_callback(interaction: discord.Interaction): 
          if interaction.user != ctx.author: return await self.bot.ext.send_warning(interaction, "You're **not** the author", ephemeral=True)            
          return await interaction.response.edit_message(embed=discord.Embed(color=self.bot.color, description=f"{interaction.user.mention}: **Cancelled**"), view=None)

        button2.callback = button2_callback 

        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)
        return await ctx.reply(embed=e, view=view)      
       
     return await ctx.send_error(ctx, "No **sticker** found")

   @commands.command(description="Shows all server emojis", help="emoji", aliases=["emojis"])
   async def emojilist(self, ctx: commands.Context):
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for emoji in ctx.guild.emojis:
              mes = f"{mes}`{k}` {emoji} - ({emoji.name})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=self.bot.color, title=f"Emojis in {ctx.guild.name} [{len(ctx.guild.emojis)}]", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            number.append(discord.Embed(color=self.bot.color, title=f"Emojis in {ctx.guild.name} [{len(ctx.guild.emojis)}]", description=messages[i]))
            await ctx.paginator(number)       

   @commands.command(aliases=["downloademoji", "e", 'jumbo'], description="Enlarge Emoji", help="emoji", usage="[emoji]")
   async def enlarge(self, ctx: commands.Context, emoj: Union[discord.PartialEmoji, str]): 
    if isinstance(emoj, discord.PartialEmoji): return await ctx.reply(file=await emoj.to_file(filename=f"{emoj.name}{'.gif' if emoj.animated else '.png'}"))
    elif isinstance(emoj, str): return await ctx.reply(file=discord.File(fp=await self.bot.getbyte(f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{ord(emoj):x}.png"), filename="emoji.png"))
  
async def setup(bot) -> None:
    await bot.add_cog(Emoji(bot))   
