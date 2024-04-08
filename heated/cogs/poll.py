import discord
from discord.ext import commands

class poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, question=None):
        if question is None:
            embed = discord.Embed(
                title='Poll',
                color=0xCCCCCC,
                description='Make a poll.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}poll [question]\n```',
                inline=False
            )
            await ctx.send(embed=embed)
        else:
            user_pfp = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
            embed = discord.Embed(title="Poll:", description=question, color=0xCCCCCC)
            embed.set_author(name=ctx.author.name, icon_url=user_pfp)
            message = await ctx.send(embed=embed)
            
            await message.add_reaction('<:yes:1214258212145205330>')
            await message.add_reaction('<:no:1214258209934675978>')

            await ctx.message.delete()
            
            
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:false:1214258281183453254> Fail',
                description='> Missing `manage_messages` permission(s)',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
async def setup(client):
    await client.add_cog(poll(client))