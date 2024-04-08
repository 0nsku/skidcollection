import discord
from discord.ext import commands
from discord.ui import view, select
from utils import functions

class help2(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['help2'])
    async def h2(self, ctx):
        
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url

        embed = discord.Embed(
            title="<:home:1188615407175737365> Help | Home",
            description=f"",
            color=0xCCCCCC
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="<:channel:1045750417457422397> **Need help?**", value="<:rp:1197985417908191452> to navigate click down on the bar.", inline=False)
        embed.add_field(name=f"<:channel:1045750417457422397> **Useful links**", value="<:rp:1197985417908191452> [Support](https://discord.gg/heated)・[Bot](https://discord.com/api/oauth2/authorize?client_id=1168544159599186041&permissions=8&scope=bot+applications.commands)・[Website](https://graveyardbot.xyz)", inline=False)

        await ctx.send("Moved to: https://graveyardbot.xyz/commands/ cus of dropdowns issues.", embed=embed)
        
        
class DropdownSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Select a category",
            options=[
                discord.SelectOption(label="home", emoji="<:home:1188615407175737365>", description="home page"),
                discord.SelectOption(label="moderation", emoji="<:moderation:1188604075231682671>", description="ban, kick, silence"),
                discord.SelectOption(label="utility", emoji="<:Utility:1172264083534381166>", description="snipe, afk"),
                discord.SelectOption(label="config", emoji="<:config:1188605506672152697>", description="soon."),
                discord.SelectOption(label="info", emoji="<:info:1188604389301166120>", description="avatar, banner, inv"),
                discord.SelectOption(label="fun", emoji="<:fun:1173279154762940578>", description="coinflip, 8ball, ppsize"),
                discord.SelectOption(label="interactions", emoji="<:fun:1173279154762940578>", description="soon."),
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        await handle_interaction(selected_option, interaction)

async def handle_interaction(selected_option, interaction):
    if selected_option == "home":
        embed = discord.Embed(title="<:home:1188615407175737365> Help | Home", 
                              description="", 
                              color=0x000000)
        embed.add_field(name="<:channel:1045750417457422397> **Need help?**", 
                        value="<:rp:1197985417908191452> to navigate click down on the bar.", inline=False)
        embed.add_field(name=f"<:channel:1045750417457422397> **Useful links**", 
                        value="<:rp:1197985417908191452> [Support](https://discord.gg/stealing)・[Bot](https://discord.com/api/oauth2/authorize?client_id=1168544159599186041&permissions=8&scope=bot+applications.commands)・[Website](https://graveyardbot.xyz)", inline=False)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "utility":
        embed = discord.Embed(title="<:Utility:1172264083534381166> Help | Utility:", 
                              description=f"> `$snipe` show a deleted message. \n > `$afk` show an afk status.", 
                              color=0x000000)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "moderation":
        embed = discord.Embed(title="<:moderation:1188604075231682671> Help | Moderation:", 
                              description=f"> `;ban` ban an user. \n > `;unban` unban an user. \n > `;kick` kick an user. \n > `;silence` silence an user. \n > `;unsilence` unsilence an user. \n > `;role` add/remove roles. \n > `;say` talk through the bot. \n > `;clear | purge` delete message's from the channel. \n > `;nuke` recreate the channel. \n > `;strip` remove all roles from an user. \n > `;lock` lock a channel. \n > `;unlock` unlock a channel. \n > `;guildicon` change the servers icon. \n > `;rename` rename the server.\n > `;slowmode` chnage the slowmode of the channel. \n > `;nick` change someone's nickname. \n > `;forcenick | fn` changes someones nickname auto back. \n > `;unfornick | unfn` stops changing someone's nickname.", 
                              color=0x000000)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "info":
        embed = discord.Embed(title="<:info:1188604389301166120> Help | Information:", 
                              description="> `;ping` shows latency. \n > `;credits` shows credits. \n > `;botinfo | bot` show info about bot. \n > `;membercount | mc` show members. \n > `;servericon` show the server's icon. \n > `;serverbanner | sb` show the server's banner. \n > `;server | serverinfo | si` show the server's info. \n > `;avatar` show someone's avatar \n > `;banner | b` show someone's banner.", 
                              color=0x000000)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "config":
        embed = discord.Embed(title="<:config:1188605506672152697> Help | Config:", 
                              description="", 
                              color=0x000000)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "interactions":
        embed = discord.Embed(title="<:fun:1173279154762940578> Help | Interactions:", 
                              description="", 
                              color=0x000000)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "fun":
        embed = discord.Embed(title="<:fun:1173279154762940578> Help | Fun:", 
                              description="> `;coinflip` flip a coin. \n > `;8ball | eight_ball | ask` ask a question. \n > `;ppsize | pp` get the size of your pp.", 
                              color=0x000000)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    else:
        await interaction.response.send_message("if you broke you cg contact me :sob: davidosxo")

def get_dropdown_view():
    view = discord.ui.View()
    view.add_item(DropdownSelect())
    return view

    @commands.Cog.listener()
    async def on_select_option(interaction):
        await interaction.defer_edit()
        await interaction.message.view.callback(interaction)

async def setup(client):
    await client.add_cog(help2(client))
   