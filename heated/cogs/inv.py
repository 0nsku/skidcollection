import discord
from discord.ext import commands
from discord.ui import view

class inv(commands.Cog):
    def __init__(self, client):
        self.client = client

    class Link(discord.ui.View):
        def __init__(self):
            super().__init__()

            self.add_item(discord.ui.Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1215779345793286194&permissions=8&scope=applications.commands%20bot", emoji="<:link:1214258293304852570>"))
            self.add_item(discord.ui.Button(label="Support", url="https://www.discord.gg/whoa", emoji="<:staff2:1217190802229301248>"))
            
    @commands.command(aliases=['invite', 'links'])
    async def inv(self, ctx: commands.Context):
        view = self.Link()
        embed = discord.Embed(
            title="<:heated:1215001858100428851> Links",
            description=f"> Invite heated for the **best** user experience",
            color=0xCCCCCC
        )

        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(inv(client))