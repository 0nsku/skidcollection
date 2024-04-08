import discord
from discord.ext import commands
import aiohttp

class pfp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def pfp(self, ctx, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        print(f"Failed to fetch image. Status code: {resp.status}")
                        return await ctx.send('Fetch image failed.')

                    data = await resp.read()

                    await self.client.user.edit(avatar=data)
                    await ctx.send('Changed pfp')
        except Exception as e:
            print(f'An error occurred: {e}')
            await ctx.send(f'An error occurred: {e}')

async def setup(client):
    await client.add_cog(pfp(client))
