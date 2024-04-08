import discord
from discord.ext import commands

class nick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nickname'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member = None, *, new_nickname = None):
        if member is None or new_nickname is None:
            embed = discord.Embed(
                title='',
                description=f'> ` ;nick [@user] [nickname]`',
                color=0xCCCCCC
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.edit(nick=new_nickname)
            embed = discord.Embed(
                title='',
                description=f'> <:true:1214258277391536158> Changed nickname for {member.name} to {new_nickname}!',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='',
                description=f"> <:false:1214258281183453254> Put my role above the persons you want to change nickname.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='',
                description=f"An error occurred: {e} Contact [davidosxo](https://discord.com/users/1168186952772747364) or [support](https://discord.gg/heated)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
            
    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> Missing `manage_nicknames` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(nick(client))