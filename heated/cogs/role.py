import discord
from discord.ext import commands

class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, aliases=["r"])
    async def role(self, ctx):
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
        embed = discord.Embed(
            title='Role',
            color=0xCCCCCC,
            description='<:rp:1197985417908191452> Manage roles.'
            )
        embed.add_field(
            name='<:cmds:1214258288326090773> Command Usage:',
            value=f'```\n{ctx.prefix}role create [name] - create a role \n{ctx.prefix}role add [@user] [@role] - add a user a role\n{ctx.prefix}role remove [@user] [@role] - remove a user a role\n{ctx.prefix}role delete [@role] - delete a role\n{ctx.prefix}role rename [role] [name] - rename a role \n```',
            inline=False
            )
        embed.add_field(
            name='<:info:1214258260836749462> Example:',
            value=f'```\n{ctx.prefix}role create admin \n```',
            inline=True
            )
        embed.add_field(
            name='<:misc:1215001481338556496> Aliases:',
            value=f'```\nr\n```',
            inline=True
            )
        embed.add_field(
            name='<:wait:1214258202754154617> Permissions:',
            value=f'```\nManage Roles\n```',
            inline=True
            )
        await ctx.send(embed=embed)
        embed.set_thumbnail(url=avatar_url)

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def create(self, ctx, *, role_name):
        new_role = await ctx.guild.create_role(name=role_name)
        embed = discord.Embed(
            title="",
            description=f"> <:true:1214258277391536158> Created the role: {new_role.name}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def add(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)
        embed = discord.Embed(
            title="",
            description=f"> <:true:1214258277391536158> Added the {role.mention} role to {member.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def remove(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.remove_roles(role)
        embed = discord.Embed(
            title="",
            description=f"> <:true:1214258277391536158> Removed {role.mention} role from {member.mention}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def delete(self, ctx, *, role: discord.Role):
        await role.delete()
        embed = discord.Embed(
            title="",
            description=f"> <:true:1214258277391536158> Deleted the {role.name} role.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @role.command()
    @commands.has_permissions(manage_roles=True)
    async def rename(self, ctx, role: discord.Role, *, new_name):
        await role.edit(name=new_name)
        embed = discord.Embed(
            title="",
            description=f"> <:true:1214258277391536158> Renamed {role.mention} to {new_name}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(role(client))