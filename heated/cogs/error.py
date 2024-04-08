import discord
from discord.ext import commands

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            command_name = ctx.command.name 
            cooldown_time = error.retry_after
            embed = discord.Embed(
                title='<:false:1214258281183453254> Fail',
                description=f" > **{command_name}** is on cooldown, please try again in `{cooldown_time:.2f}s`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            missing_perms = format(error.missing_permissions).replace('[', '').replace("'", '').replace(']', '').replace('_', ' ')

            embed = discord.Embed(title='<:false:1214258281183453254> Fail', description=f'> Missing ``{missing_perms}`` permission(s)', color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(error(client))