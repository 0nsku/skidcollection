import discord
from discord.ext import commands

class slowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sl"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, duration: str=None):
        try:
            if duration is not None:
                duration = int(duration)
                await ctx.channel.edit(slowmode_delay=duration)
                
                embed = discord.Embed(
                    title='<:true:1214258277391536158> Success',
                    description=f"> Set slowmode to `{duration}` seconds!",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title='Slowmode',
                    color=0xCCCCCC,
                    description='<:rp:1197985417908191452> Change the slowmode of the chnanel.'
            )
                embed.add_field(
                    name='<:cmds:1214258288326090773> Command Usage:',
                    value=f'```\n{ctx.prefix}slowmode [number]\n```',
                    inline=False
            )
                embed.add_field(
                    name='<:info:1214258260836749462> Example:',
                    value=f'```\n{ctx.prefix}slowmode 5\n```',
                    inline=True
            )
                embed.add_field(
                    name='<:misc:1215001481338556496> Aliases:',
                    value=f'```\nsl\n```',
                    inline=True
            )
                embed.add_field(
                    name='<:wait:1214258202754154617> Permissions:',
                    value=f'```\nManage Channels\n```',
                    inline=True
            )
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(
                title='<:false:1214258281183453254> Fail',
                description='> Invalid duration format.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(slowmode(client))