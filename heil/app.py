import discord
import os
import config
from discord.ext import commands

async def get_prefix(bot, message: discord.Message):
    guild = bot.get_guild(config.guild)
    role = guild.get_role(config.role)
    if role in message.author.roles:
        return [",", ""]
    else:
        return "005548544"

bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    allowed_mentions = discord.AllowedMentions(
        everyone=False,
        roles=False
    )
)
bot.owner_ids = config.owner_ids

@bot.event
async def on_connect():
    extentions = ['jishaku']
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):
            extentions.append("cogs." + files[:-3])
        
    for extention in extentions:
        await bot.load_extension(extention)


bot.run(token=config.token, reconnect=True)