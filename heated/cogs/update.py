import discord
from discord.ext import commands
from discord.ui import view, select

class update(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        embed = discord.Embed(
            title='Update',
            description='<:rp:1197985417908191452> *version:* **0.0.9**',
            color=0xCCCCCC
        )
        embed.add_field(name="", value='__`=`__ Snipe \n __`+`__ Dm \n Many more!', inline=False)

        embed_message = await ctx.send(embed=embed)

        await embed_message.add_reaction('<:g_w:1209959559054106714>')
        await embed_message.add_reaction('<:r_L:1209959658236682250>')



async def setup(client):
    await client.add_cog(update(client))