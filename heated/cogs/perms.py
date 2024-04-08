import discord
from discord.ext import commands

class perms(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def perms(self, ctx):
        perms = ctx.guild.me.guild_permissions

        # Define emoji IDs
        good = '<:true:1214258277391536158>'
        bad = '<:false:1214258281183453254>'

        permission_strings = [
            f"{good if allowed else bad} {perm}" 
            for perm, allowed in perms
        ]

        embed = discord.Embed(title="", color=0xCCCCCC)
        embed.add_field(name="Permissions", value="\n".join(permission_strings) or "None", inline=False)

        await ctx.send(embed=embed)



    @commands.command()
    @commands.is_owner()
    async def perms(self, ctx):

        perms = ctx.guild.me.guild_permissions

        good = [perm for perm, allowed in perms if allowed]

        embed = discord.Embed(title="", color=0xCCCCCC)
        embed.add_field(name="Perms:", value=", ".join(good) or "None")

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(perms(client))