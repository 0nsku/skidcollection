import discord
from discord.ext import commands
from discord.ui import view, select

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['help'])
    async def h(self, ctx):
        
        view = get_dropdown_view()
        
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url

        embed = discord.Embed(
            title="<:home:1214258263999119420> Help | Home",
            description=f"<:rp:1197985417908191452> Welcome to ***` #HEATED `***",
            color=0xCCCCCC
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="<:search:1214258137637326858> **Need help?**", value="<:rp2:1197985457527603322> Navigate by using Menu. \n <:rp:1197985417908191452> More info: ;help [command]", inline=True)
        embed.add_field(name=f"<:g_nun:1186052591239561248>", value="・", inline=True)
        embed.add_field(name=f"<:knowledge:1214258123804770385> **Info**", value="<:rp2:1197985457527603322> Bot is in development. \n <:rp:1197985417908191452> Latest version: 0.08", inline=True)
        embed.add_field(name=f"<:link:1214258293304852570>  **Useful links**", value="<:rp2:1197985457527603322> [Support](https://discord.gg/whoa) \n <:rp:1197985417908191452> [Bot](https://discord.com/api/oauth2/authorize?client_id=1215779345793286194&permissions=8&scope=applications.commands%20bot)", inline=True)
        embed.add_field(name=f"<:g_nun:1186052591239561248>", value="・", inline=True)
        embed.add_field(name=f"<:iforgot:1214258131627155547> **Keys**", value="<:rp2:1197985457527603322> [] = Needed \n <:rp:1197985417908191452> () = Optional", inline=True)

        await ctx.send(embed=embed, view=view)
        
        
class DropdownSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Menu",
            options=[
                discord.SelectOption(label="moderation", emoji="<:staff:1214258253983252520>", description=""),
                discord.SelectOption(label="utility", emoji="<:utility:1214258167119224862>", description=""),
                discord.SelectOption(label="config", emoji="<:config:1214258256588054548> ", description=""),
                discord.SelectOption(label="info", emoji="<:info:1214258260836749462>", description=""),
                discord.SelectOption(label="fun", emoji="<:fun:1214258162304028732>", description=""),
                discord.SelectOption(label="interactions", emoji="<:spark:1214258182252142625>", description=""),
                discord.SelectOption(label="economy", emoji="<:money:1214258215747985478>", description=""),
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        await handle_interaction(selected_option, interaction)

async def handle_interaction(selected_option, interaction):
    if selected_option == "utility":
        embed = discord.Embed(title="<:utility:1214258167119224862> Help | utility:", 
                              description=f"```snipe, afk```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "moderation":
        embed = discord.Embed(title="<:staff:1214258253983252520> Help | Moderation:", 
                              description=f"```ban & unban, kick, silence & unsilence, role, say, purge, nuke, strip, lock & unlock, guild, slowmode, nick, forcenick & unfornick, pin & unpin, poll```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "info":
        embed = discord.Embed(title="<:info:1214258260836749462> Help | Information:", 
                              description="```ping, credits, botinfo, membercount, server, avatar, banner```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "config":
        embed = discord.Embed(title="<:config:1214258256588054548> Help | Config:", 
                              description="```prefix```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "interactions":
        embed = discord.Embed(title="<:spark:1214258182252142625> Help | Interactions:", 
                              description="```Soon```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "fun":
        embed = discord.Embed(title="<:fun:1214258162304028732> Help | Fun:", 
                              description="```8ball, ppsize, dm```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    elif selected_option == "economy":
        embed = discord.Embed(title="<:money:1214258215747985478> Help | economy:", 
                              description="```Soon```", 
                              color=0xCCCCCC)
        await interaction.response.edit_message(content="", embed=embed, view=get_dropdown_view())
    else:
        await interaction.response.send_message("if you broke bot or bot help broken, contact me [Solix](https://discord.com/users/546548675086778398) or my dev [davidosxo](https://discord.com/users/1168186952772747364)")

def get_dropdown_view():
    view = discord.ui.View()
    view.add_item(DropdownSelect())
    return view

    @commands.Cog.listener()
    async def on_select_option(interaction):
        await interaction.defer_edit()
        await interaction.message.view.callback(interaction)

async def setup(client):
    await client.add_cog(help(client))