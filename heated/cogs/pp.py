import discord
from discord.ext import commands
import random

class pp(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['pp'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ppsize(self, ctx):
        sizes = [
            "8D",
            "8=D",
            "8==D",
            "8===D",
            "8====D",
            "8=====D",
            "8======D",
            "8=======D",
            "8========D",
            "8=========D",
            "8==========D"
        ]

        random_size = random.choice(sizes)

        embed = discord.Embed(
            title="",
            description=random_size,
            color=0xCCCCCC
        )

        await ctx.send(f"{ctx.author.mention}", embed=embed)
        
        
        
async def setup(client):
    await client.add_cog(pp(client))