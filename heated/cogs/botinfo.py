import discord
from discord.ext import commands
import psutil
import sqlite3
import platform

class botinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_ping_emoji(self, latency):
        if latency < 50:
            return "<:good:1214258219619192882>"
        elif latency < 100:
            return "<:okay:1214258223901581402>"
        else:
            return "<:bad:1214258227189911623>"

    @commands.command(aliases=['bot'])
    async def botinfo(self, ctx):
        
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
        members = sum(guild.member_count for guild in self.client.guilds)
        guilds = len(self.client.guilds)
        latency = round(self.client.latency * 1000)
        emoji = self.get_ping_emoji(latency)
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        commands_count = len(self.client.commands)
        
        embed = discord.Embed(title=f'<:heated:1215001858100428851> heated', color=0xCCCCCC)
        embed.add_field(name='<:minus:1203037065705562153> Stats:', value=f'<:users:1214258272735858728> **Users**: `{members:,}` \n <:home:1214258263999119420> **Servers**: `{guilds:,}` \n <:cmds:1214258288326090773> **Commands**: `{commands_count}`', inline=True)
        embed.add_field(name='<:minus:1203037065705562153> Usage:', value=f'{emoji} **Ping**: `{latency}ms` \n <:cloud:1215007207297519666> **Cpu**: `{cpu}%` \n <:save:1214258156192923698> **Ram**: `{ram}%`', inline=True)
        
        
        embed.set_thumbnail(url=avatar_url)
        await ctx.send(embed=embed)
    
    
async def setup(client):
    await client.add_cog(botinfo(client))