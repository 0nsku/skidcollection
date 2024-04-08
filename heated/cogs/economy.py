import discord
from discord.ext import commands
import sqlite3

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client



async def setup(client):
    await client.add_cog(economy(client))