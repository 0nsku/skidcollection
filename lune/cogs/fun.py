from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check
import datetime, discord, humanize, os, arrow, uwuipy, humanfriendly, asyncio, aiohttp, random, json, time, dateutil.parser
from discord import Embed, File, TextChannel, Member, User, Role, Message
from deep_translator import GoogleTranslator
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from discord.ext import commands 
from discord.ui import Button, View
import requests
from discord.ext import tasks
from discord.ext.commands import BadArgument, Cog, hybrid_command, hybrid_group, Author, command
from aiohttp import ClientResponse
import typing
import sys
from random import randrange
from typing import List
from tools.checks import Perms
from aiogtts import aiogTTS
from random import choice
from typing import Union
from io import BytesIO
import tracemalloc
tracemalloc.start()

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int, player1: discord.Member, player2: discord.Member):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.player1 = player1
        self.player2 = player2

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if interaction.user != self.player1: return await interaction.response.send_message("This is not your game!", ephemeral=True)
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"It's **{self.player2.mention}**'s turn"
        else:
            if interaction.user != self.player2: return await interaction.response.send_message("This is **not** your **game**", ephemeral=True)
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"It's **{self.player1.mention}'s** turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'**{self.player1.mention}** won!'
            elif winner == view.O:
                content = '**{}** won!'.format(self.player2.mention)
            else:
                content = "You're **tied** up!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, player1, player2))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None
    
    async def on_timeout(self) -> None:
      for item in self.children: item.disabled = True 
      await self.message.edit(view=self.view)   

class fun(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.hybrid_command(description="Define a word on urbandictionary", help="fun", usage="[word]")
    async def urban(self, ctx, *, word):
      embeds = []
      try:
       data = await self.bot.session.json("http://api.urbandictionary.com/v0/define", params={"term": word})
       defs = data["list"]
       for defi in defs: 
        e = discord.Embed(color=self.bot.color, description=defi["definition"], timestamp=dateutil.parser.parse(defi["written_on"]))
        e.set_author(name=word, url=defi["permalink"])
        e.add_field(name="Example", value=defi["example"], inline=False) 
        e.set_footer(text=f"{defs.index(defi)+1}/{len(defs)}")
        embeds.append(e)
       return await ctx.paginator(embeds)
      except Exception as e: await ctx.reply("no definition found for **{}**".format(word))                       

    @hybrid_command(help="fun", description="join vc and make some noise")
    async def esex(self, ctx: commands.Context): 
      if not ctx.author.voice: return await ctx.send_warning("You are **not** in a voice channel")
      if ctx.voice_client: return await ctx.send_warning("The bot is **already** in a voice channel")
      vc = await ctx.author.voice.channel.connect()
      vc.play(discord.FFmpegPCMAudio("./esex.mp3"), after=lambda e: print("done"))
      while vc.is_playing(): 
       await asyncio.sleep(10)
       if not ctx.voice_client: return
       await ctx.send(embed = Embed(description="That was **so good...** I'm finished now..", color=self.bot.color))
       await ctx.voice_client.disconnect(force=True)      

    @hybrid_group(aliases=["ttt"], description="Play TicTacToe", help="fun", usage="[member]")
    async def tictactoe(self, ctx: commands.Context, *, member: discord.Member):
      if member is ctx.author: return await ctx.reply(embed=discord.Embed(color=self.bot.color, description=f"> {ctx.author.mention}: You need **somebody** to play **with**"))
      if member.bot: return await ctx.reply("Robots cant play sorry!")      
      embed = discord.Embed(color=self.bot.color, description=f"**{ctx.author.name}** wants to play **tictactoe**")
      style = discord.ButtonStyle.gray
      yes = discord.ui.Button(label="Accept", style=style)
      no = discord.ui.Button(label="Deny", style=style)
      
      async def yes_callback(interaction: discord.Interaction): 
         if interaction.user != member:
           em = discord.Embed(color=self.bot.color, description=f"> You're **not** the author")
           return await interaction.response.send_message(embed=em, ephemeral=True)
         vi = TicTacToe(ctx.author, member)
         await interaction.message.delete()
         vi.message = await ctx.send(content=f'**{ctx.author.mention}** is starting the game **first**', embed=None, view=vi)  
         
      async def no_callback(interaction: discord.Interaction): 
         if interaction.user != member:
           em = discord.Embed(color=self.bot.color, description=f"> You're **not** the author")
           return await interaction.response.send_message(embed=em, ephemeral=True)
         await interaction.response.edit_message(embed=discord.Embed(color=self.bot.color, description=f"**{interaction.user.name}** doesn't **want to play**"), view=None, content=ctx.author.mention)

         
      yes.callback = yes_callback
      no.callback = no_callback  
      view = discord.ui.View()
      view.add_item(yes)
      view.add_item(no)
      await ctx.send(embed=embed, view=view, content=member.mention) 

    @commands.command(name="dare")
    async def dare(self, ctx: Context):
        dare_file_path = os.path.join("texts", "dares.txt")

        if os.path.exists(dare_file_path):
            with open(dare_file_path, "r", encoding="utf-8") as file:
                dares = file.readlines()

            random_dare = random.choice(dares).strip()

            embed = Embed(description=f"{ctx.author.mention}: {random_dare}", color=self.bot.color)

            await ctx.reply(embed=embed)
        else:
            await ctx.send_warning(f"Couldn't find **dares** file, please **join the** [**__support server__**](https://disccord.gg/lunehq)")

    @commands.command(name="truth")
    async def truth(self, ctx: Context):
        dare_file_path = os.path.join("texts", "truths.txt")

        if os.path.exists(dare_file_path):
            with open(dare_file_path, "r", encoding="utf-8") as file:
                dares = file.readlines()

            random_dare = random.choice(dares).strip()

            embed = Embed(description=f"{ctx.author.mention}: {random_dare}", color=self.bot.color)

            await ctx.reply(embed=embed)
        else:
            await ctx.send_warning(f"Couldn't find **truth** file, please **join the** [**__support server__**](https://disccord.gg/lunehq)")
    
    @commands.command(name="wouldyourather", aliases=["wyr"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def would_you_rather(self, ctx: Context):
        wyr_file_path = os.path.join("texts", "wyr.txt")

        if os.path.exists(wyr_file_path):
            with open(wyr_file_path, "r", encoding="utf-8") as file:
                questions = [line.strip() for line in file.readlines()]

            if len(questions) >= 2:
                emoji_a = "🅰"
                emoji_b = "🅱"

                question_a, question_b = random.sample(questions, 2)
                while question_a == question_b:
                    question_a, question_b = random.sample(questions, 2)

                embed = Embed(title="Would You Rather?", color=self.bot.color)
                embed.description = f"{emoji_a} {question_a}\n\n{emoji_b} {question_b}"
                embed.set_footer(text=f"React with {emoji_a} or {emoji_b} to choose!")

                message = await ctx.reply(embed=embed)

                await message.add_reaction(emoji_a)
                await message.add_reaction(emoji_b)
            else:
                await ctx.send_warning(f"Not enough questions in the 'wyr.txt' file. Please **join the** [**__support server__**](https://disccord.gg/lunehq)")
        else:
            await ctx.send_warning(f"Couldn't find **wouldyourather** file. Please **join the** [**__support server__**](https://disccord.gg/lunehq)")
       


async def setup(bot) -> None:
    await bot.add_cog(fun(bot))        