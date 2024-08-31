import discord
import sys
import psutil
import humanize
import string
import random
import os
import asyncio
import re
import requests
import aiohttp
import json
import psutil
from discord import Member, User, Embed
from discord.ext.commands import MemberConverter, UserConverter, is_owner
from discord.ui import view, select
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Union, Optional
from googletrans import Translator
from colorama import Fore, Style
from gtts import gTTS
import glob

intents = discord.Intents.all()

class BetrayBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=",",
            strip_after_prefix=True,
            help_command=None,
            chunk_guilds_on_startup=False,
            case_insensitive=True,
            intents=intents,
            allowed_mentions=discord.AllowedMentions(
                everyone=False,
                users=True,
                roles=False,
                replied_user=True
            )
        )

        self.owner_ids = [1163174089083592786, 1079189478981243072]
        self.start_time = datetime.now(timezone.utc)
        self.launch_time = datetime.utcnow()
        self.bot_pfp = 'betray (2).gif'
        self.main_guild_id = 1190116499344605346
        self.snipe_data = {}
        self.user_deletion_count = defaultdict(int)

    async def on_connect(self):
        await self.wait_until_ready()
        await self.turnon()
        print("Connected!")

    async def turnon(self) -> None:
        try:
            await self.load_extension('jishaku')
        except Exception as e:
            print(f"Failed to load Jishaku extension: {e}")
        cog_files = glob.glob('cogs/*.py')
        for cog_file in cog_files:
            try:
                cog_name = os.path.splitext(os.path.basename(cog_file))[0]
                await self.load_extension(f"cogs.{cog_name}")
                print(f"Cog loaded: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog: {e} ({cog_name})")

    def generate_key(self):
        prefix = "b#"
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        return prefix + suffix

    async def has_premium(user_id):
        with open('premiumusers.txt', 'r') as file:
            return str(user_id) in file.read().splitlines()

    @staticmethod
    def parse_time(time_string):
        time_string = time_string.lower()
        match = re.match(r'(\d+)(s|m|h)', time_string)
        if not match:
            return None
        amount, unit = match.groups()
        amount = int(amount)
        if unit == 's':
            return amount
        elif unit == 'm':
            return amount * 60
        elif unit == 'h':
            return amount * 3600

bot = BetrayBot()


async def identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                '$os': sys.platform,
                '$browser': 'Discord iOS',
                '$device': 'Discord iOS',
                '$referrer': '',
                '$referring_domain': ''
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }

    if self.shard_id is not None and self.shard_count is not None:
        payload['d']['shard'] = [self.shard_id, self.shard_count]

    state = self._connection
    if state._activity is not None or state._status is not None:
        payload['d']['presence'] = {
            'status': state._status,
            'game': state._activity,
            'since': 0,
            'afk': False
        }

    if state._intents is not None:
        payload['d']['intents'] = state._intents.value

    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(payload)
discord.gateway.DiscordWebSocket.identify = identify

@bot.event
async def on_ready():
    start_time = datetime.now(timezone.utc)
    with open(bot.bot_pfp, 'rb') as file:
        gif_image = file.read()
    try:
        await bot.user.edit(avatar=gif_image)
        print('Bot profile picture set')
    except discord.HTTPException as e:
        print(f'Failed to set bot profile picture: {e}')
    print(f"{Fore.MAGENTA}┌┐ ┌─┐┌┬┐┬─┐┌─┐┬ ┬")
    print(f"{Fore.MAGENTA}├┴┐├┤  │ ├┬┘├─┤└┬┘")
    print(f"{Fore.MAGENTA}└─┘└─┘ ┴ ┴└─┴ ┴ ┴")
    print(f"{Fore.MAGENTA}V2 / recode")
    print(f'{Fore.WHITE}Betray is online.{Style.RESET_ALL}')
    print(f'{Fore.WHITE}Dev: {Fore.MAGENTA}yau{Style.RESET_ALL}')
    members_count = sum(guild.member_count for guild in bot.guilds)
    print(f'{Fore.WHITE}servers - {len(bot.guilds)}')
    print(f'{Fore.WHITE}member count - {members_count}')
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    await rotate_status(bot)

    
@tasks.loop(seconds=20.0)
async def rotate_status(bot):
    statuses = [
        {'type': discord.ActivityType.competing, 'name': f"{len(bot.guilds)} guilds"},
        {'type': discord.ActivityType.listening, 'name': f"{sum(guild.member_count for guild in bot.guilds)} users"},
        {'type': discord.ActivityType.competing, 'name': "betray better >-<"},
        {'type': discord.ActivityType.listening, 'name': f"{round(bot.latency * 1000)}ms"}
    ]
        
    try:
        current_status = statuses[rotate_status.current_loop % len(statuses)]
        await bot.change_presence(activity=discord.Activity(type=current_status['type'], name=current_status['name']))
    except (IndexError, ZeroDivisionError):
        print("Failed to update status due to an unexpected error.")

@bot.event
async def on_command_completion(ctx):
    print(f"{Fore.WHITE}{ctx.author}〡,{ctx.command}")



@bot.command()
async def genpremkeys(ctx, amount: int):
    if ctx.author.id not in owner_ids:
        return await ctx.send("nope, nice try.")
    keys = [generate_key() for _ in range(amount)]
    with open('premmiumkeys.txt', 'a') as file:
        for key in keys:
            file.write(key + '\n')
    embed = discord.Embed(description=f'> Made **{amount}** keys.', color=0x2b2d31)
    await ctx.send(embed=embed)

@bot.command()
async def redeem(ctx, key):
    with open('premmiumkeys.txt', 'r') as file:
        keys = file.read().splitlines()
    if key in keys:
        keys.remove(key)
        with open('premmiumkeys.txt', 'w') as file:
            file.write('\n'.join(keys))
        with open('premiumusers.txt', 'a') as file:
            file.write(str(ctx.author.id) + '\n')
        embed = discord.Embed(description="> Thank you for buying premium\n> You have redeemed a `lifetime` key for betray", color=0x2b2d31)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="> Your key is invaild", color=0x2b2d31)
        await ctx.send(embed=embed)

def has_premium(user_id):
    with open('premiumusers.txt', 'r') as file:
        return str(user_id) in file.read().splitlines()
    
@bot.event
async def on_message(message):
    if (message.guild.id, message.author.id) in bot.user_deletion_count and bot.user_deletion_count[(message.guild.id, message.author.id)] > 0:
        await message.delete()
        bot.user_deletion_count[(message.guild.id, message.author.id)] -= 1
    await bot.process_commands(message)
   

bot.run('[Redacted just so discord wont revoke it]')
