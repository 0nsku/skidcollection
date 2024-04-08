import discord
from discord.ext import commands
from discord.ui import view

class g2(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        
    class Link(discord.ui.View):
        def __init__(self):
            super().__init__()

            self.add_item(discord.ui.Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1215779345793286194&permissions=8&scope=applications.commands%20bot"))
            self.add_item(discord.ui.Button(label="Support", url="https://www.discord.gg/heated"))
            self.add_item(discord.ui.Button(label="Owner", url="https://discord.com/users/921148808551870484"))
            
    
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            if member.id == guild.owner_id:
                embed = discord.Embed(
                    title=f"<:heated:1215001858100428851> Thank you for inviting Heated!",
                    description="<:rp:1197985417908191452> Here is some useful information:",
                    color=0xCCCCCC
                )
                avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
                view = self.Link()
                
                embed.set_thumbnail(url=avatar_url)

                embed.add_field(name=f"<:knowledge:1214258123804770385> **Information**", value="<:rp2:1197985457527603322> Default prefix = `;` \n <:rp:1197985417908191452> Prefix change = `;prefix [prefix]`", inline=True)

                await member.send(embed=embed, view=view)
                break
        
        
async def setup(client):
    await client.add_cog(g2(client))