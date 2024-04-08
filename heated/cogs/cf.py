import discord
from discord.ext import commands
import random
import asyncio

class cf(commands.Cog):
    def __init__(self, client):
        self.client = client
        
async def setup(client):
    await client.add_cog(cf(client))