import discord
from discord.ext import commands
from discord.ui import Button, View
import datetime
from datetime import datetime

class server(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def server(self, ctx):
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
        embed = discord.Embed(
            title='Server',
            color=0xCCCCCC,
            description='<:rp:1197985417908191452> Get server ralated stuff.'
        )
        embed.add_field(
            name='<:cmds:1214258288326090773> Command Usage:',
            value=f'```\n{ctx.prefix}server icon - shows the server icon\n{ctx.prefix}server banner - shows the server banner \n{ctx.prefix}server info - shows info about the server \n```',
            inline=False
        )
        await ctx.send(embed=embed)
        embed.set_thumbnail(url=avatar_url)

    @server.command()
    async def info(self, ctx):
        guild = ctx.guild
        member_count = guild.member_count
        text_channels = len(guild.text_channels)
        all_members = guild.member_count
        members = sum(not member.bot for member in guild.members)
        bots = sum(member.bot for member in guild.members)
        voice_channels = len(guild.voice_channels)
        roles = len(guild.roles)
        boost_level = guild.premium_tier
        emoji_count = len(guild.emojis)
        icon = ctx.guild.icon.url
        categories = len(ctx.guild.categories)
        created_at = guild.created_at.strftime("%B %d, %Y")
        
        banner_url = None
        if guild.banner:
            banner_url = guild.banner.url

        if guild.vanity_url_code:
            vanity_emoji = "<:true:1214258277391536158>"
            vanity_info = f"{guild.vanity_url_code}"
        else:
            vanity_emoji = "<:false:1214258281183453254>"
            vanity_info = "None"
        
        embed = discord.Embed(title=f"{guild.name}'s Information", color=0xCCCCCC)
        embed.set_thumbnail(url=icon)
        if banner_url:
            embed.set_image(url=banner_url)
        embed.add_field(name="<:minus:1203037065705562153> <:info:1214258260836749462> Server", value=f"<:rp2:1197985457527603322> Created: `{created_at}`\n<:rp2:1197985457527603322> Server id: `{guild.id}`\n<:rp:1197985417908191452> Owner: `{guild.owner}`", inline=True)
        embed.add_field(name="<:minus:1203037065705562153> <:config:1214258256588054548> Misc", value=f"<:rp2:1197985457527603322> Roles: `{roles}`\n<:rp2:1197985457527603322> Emojis: `{emoji_count}`\n<:rp:1197985417908191452> Soon", inline=True)
        embed.add_field(name="<:minus:1203037065705562153> <:folder:1214258245015707750> Channels", value=f"<:rp2:1197985457527603322> Voice: `{voice_channels}`\n<:rp2:1197985457527603322> Text: `{text_channels}`\n<:rp:1197985417908191452> Categories: `{categories}`", inline=True)
        embed.add_field(name="<:minus:1203037065705562153> <:boost:1214258310111567923> Boost", value=f"<:rp2:1197985457527603322> Boost level: `{boost_level}`\n<:rp:1197985417908191452> Vanity: `{vanity_info}`", inline=True)
        embed.add_field(name="<:minus:1203037065705562153> <:users:1214258272735858728> Members", value=f"<:rp2:1197985457527603322> All: `{all_members}`\n<:rp2:1197985457527603322> Humans: `{members}`\n<:rp:1197985417908191452> Bots: `{bots}`", inline=True)

        await ctx.send(embed=embed)

    @server.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def icon(self, ctx):
        try:
            if ctx.guild:
                if ctx.guild.icon:
                    icon = ctx.guild.icon.url

                    embed = discord.Embed(title=f"{ctx.guild.name}'s Icon", color=0xCCCCCC)
                    embed.set_image(url=icon)

                    icon = Button(style=5, label="Server Icon", url=icon)

                    view = View()
                    view.add_item(icon)

                    await ctx.send(embed=embed, view=view)
                else:
                    embed = discord.Embed(title=f"> <:false:1177620773339414641> {ctx.guild.name} doesn't have an icon or it's not accessible.", color=discord.Color.red())
                    await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @server.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def banner(self, ctx):
        guild = ctx.guild
        name = guild.name

        embed = discord.Embed(title=f"{name}'s Banner", color=0xCCCCCC)

        if guild.banner:
            banner_url = guild.banner.url
            embed.set_image(url=banner_url)

            banner = Button(style=5, label="Server Banner", url=banner_url)

            view = View()
            view.add_item(banner)
        else:
            embed.add_field(name=f"> <:false:1214258281183453254> {name} doesn't have a banner or it's not accessible.", value="", inline=False)

        await ctx.send(embed=embed, view=view)

async def setup(client):
    await client.add_cog(server(client))