import discord
from discord.ext import commands
from discord.ui import View, Button

class vanity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def vanity(self, ctx):
        embed = discord.Embed(title="", description="> `vanity use/check`", color=0xCCCCCC)
        await ctx.send(embed=embed)

    @vanity.command()
    async def use(self, ctx):
        vanity_use = ctx.guild.vanity_url_code
        embed = discord.Embed(title="", color=0xCCCCCC)
        if vanity_use:
            embed.add_field(name=f"", value=f"This server uses the vanity `{vanity_use}`")
        else:
            embed.description = "This guild does not have a vanity."
        await ctx.send(embed=embed)

    @vanity.command()
    async def check(self, ctx, vanity: str):
        embed = discord.Embed(color=0xCCCCCC)

        try:
            invite = await self.client.fetch_invite(f"https://discord.gg/{vanity}")
            embed.description = f"The vanity `{vanity}` is currently in use."

            button = discord.ui.Button(label="Invite", url=invite.url, emoji="<:link:1214258293304852570>")
            view = discord.ui.View()
            view.add_item(button)

        except discord.errors.NotFound:
            embed.description = f"The vanity `{vanity}` is available."
            embed.color = discord.Color.green()

        await ctx.send(embed=embed, view=view if 'view' in locals() else None)


async def setup(client):
    await client.add_cog(vanity(client))