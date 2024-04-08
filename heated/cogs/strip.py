import discord
from discord.ext import commands

class strip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def strip(self, ctx, member: discord.Member = None):
        if member is not None:
            if ctx.author.top_role <= member.top_role:
                embed = discord.Embed(
                    title='<:false:1214258281183453254> Fail',
                    description="> You can't strip a user with the same or higher role.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                await member.edit(roles=[])

                embed = discord.Embed(
                    title='<:true:1214258277391536158> Success',
                    description=f'> Stripped {member.mention} of all roles.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Strip',
                color=0xCCCCCC,
                description="Remove all roles from a user."
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}strip [@user]\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}strip @rip.rive\n```',
                inline=True
            )
            embed.add_field(
                name='<:wait:1214258202754154617> Permissions:',
                value=f'```\nAdministrator\n```',
                inline=True
            )
            await ctx.send(embed=embed)
            
            
    @strip.error
    async def strip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="",
                description="> <:false:1214258281183453254> Missing `manage_roles` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(strip(client))