import discord
from discord.ext import commands

class dm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dm(self, ctx, user: discord.User = None, *, message=None):
        if user is None or message is None:
            embed = discord.Embed(
                title='Dm',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Send a dm to an user.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}dm [@user] (dm)\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}dm @rip.rive hi\n```',
                inline=True
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="<:true:1214258277391536158> Success",
                description=f"> Sent message to: {user.display_name}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

            try:
                embed = discord.Embed(
                    title="",
                    description=f"{message}",
                    color=0xCCCCCC
                )
                sender_pfp = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
                embed.set_author(name=ctx.author.name, icon_url=sender_pfp)
                await user.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="<:false:1214258281183453254> Fail",
                    description="> Could'nt send the message.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            
async def setup(client):
    await client.add_cog(dm(client))