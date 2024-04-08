import discord
from discord.ext import commands

class credits(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def credits(self, ctx):
        embed = discord.Embed(title='<:heated:1215001858100428851> Credits', description='', color=0xCCCCCC)
        embed.add_field(name='', 
                        value=f'<:rp2:1197985457527603322> <:owner:1214258306051215410> Founder: [`davidosxo`](https://vsc.lol/davidosxo) \n <:rp2:1197985457527603322> <:staff:1214258253983252520> Developers: [`yau`](https://discord.gg/betray) [`1deals`](https://discord.com/users/958607606241447936)\n <:rp:1197985417908191452> <:staff2:1217190802229301248> Staff: [`Solix`](https://guns.lol/solixblox)  [`ripbing`](https://loser.rip)  [`Zendyx_`](https://guns.lol/zendyx)', inline=False)
        await ctx.send(embed=embed)
    
    
async def setup(client):
    await client.add_cog(credits(client))