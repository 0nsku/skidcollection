import discord
import asyncio
import random
from discord.ext import commands, tasks

class status(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(seconds=5)
    async def change_status(self):
        total_members = sum(guild.member_count for guild in self.client.guilds)
        total_guilds = len(self.client.guilds)
        shard_count = 3

        status_messages = [
            "{:,} users".format(total_members),
            "{:,} guilds".format(total_guilds),
            ".gg/back",
        ]

        current_status = random.choice(status_messages)

        activity = discord.Activity(name=current_status, type=discord.ActivityType.watching)
        await self.client.change_presence(activity=activity, status=discord.Status.online)

    @change_status.before_loop
    async def before_change_status(self):
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(status(client))