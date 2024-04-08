import discord
from discord.ext import commands, tasks
import aiohttp

class guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def guild(self, ctx):
        embed = discord.Embed(
            title='Guild',
            color=0xCCCCCC,
            description="Change stuff in the guild."
        )
        embed.add_field(
            name='<:cmds:1214258288326090773> Command Usage:',
            value=f'```\n{ctx.prefix}guild rename [name] - Rename the server\n{ctx.prefix}guild icon [url] - Change the guild icon\n```',
            inline=False
        )
        embed.add_field(
            name='<:info:1214258260836749462> Example:',
            value=f'```\n{ctx.prefix}guild rename home\n```',
            inline=True
        )
        embed.add_field(
            name='<:wait:1214258202754154617> Permissions:',
            value=f'```\nManage Guild\n```',
            inline=True
        )
        await ctx.send(embed=embed)

    @guild.command()
    @commands.has_permissions(manage_guild=True)
    async def icon(self, ctx, icon_url=None):
        try:
            async with ctx.typing(), aiohttp.ClientSession() as session:
                async with session.get(icon_url) as resp:
                    if resp.status != 200:
                        embed = discord.Embed(
                            title='',
                            description=f'> <:false:1214258281183453254> Unable to fetch the image (Status code: {resp.status}) contact davidosxo',
                            color=discord.Color.red()
                        )
                        return await ctx.send(embed=embed)

                    await ctx.guild.edit(icon=await resp.read())
                    embed = discord.Embed(
                        title='',
                        description="> <:true:1214258277391536158> Changed the guild's icon.",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='',
                description=f'> <:false:1214258281183453254> An error occurred: {e} contact davidosxo',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @guild.command()
    @commands.has_permissions(manage_guild=True)
    async def rename(self, ctx, *, new_name: commands.clean_content=None):
        if new_name is not None:
            try:
                await ctx.guild.edit(name=new_name)

                embed = discord.Embed(
                    title='',
                    description=f'> <:true:1214258277391536158> Renamed the **Server Name** to: `{new_name}`.',
                    color=discord.Color.green()
                )
            except discord.Forbidden:
                embed = discord.Embed(
                    title='',
                    description="> <:false:1214258281183453254> I'm missing permission(s). Make sure I have the `Manage Server` permission.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            
async def setup(client):
    await client.add_cog(guild(client))