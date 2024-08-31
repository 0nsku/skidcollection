import discord
from discord.ext.commands import command, Cog
from discord.ext import commands
import datetime, requests, psutil
from typing import Union
from discord import Member, User
class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Invite", style=discord.ButtonStyle.link, url="https://discord.com/api/oauth2/authorize?client_id=1211780078858534983&permissions=8&scope=bot"))
        self.add_item(discord.ui.Button(label="Commands", style=discord.ButtonStyle.link, url="https://betray.vip/cmds"))
        
class HelpDropdown(discord.ui.Select):
    def __init__(self, bot, cogs):
        options = [
            discord.SelectOption(label=cog_name, description=f"{cog_name} commands")
            for cog_name in cogs
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        cog_name = self.values[0]
        cog = self.bot.get_cog(cog_name)
        if cog:
            commands_list = '\n'.join([command.name for command in cog.get_commands()])
            await interaction.response.send_message(f"Commands in {cog_name}:\n```\n{commands_list}\n```", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid category selected!", ephemeral=True)

class HelpView(discord.ui.View):
    def __init__(self, bot, cogs):
        super().__init__()
        self.add_item(HelpDropdown(bot, cogs))
        
class info(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        

    @commands.command(name='help')
    async def help_command(self, ctx):
        cogs = [cog for cog in self.bot.cogs.keys()]
        view = HelpView(self.bot, cogs)
        await ctx.send("Select a category:", view=view)

    @command(aliases=["up"])
    async def uptime(self, ctx):
        current_time = datetime.datetime.utcnow()
        uptime_delta = current_time - self.bot.launch_time
        uptime_seconds = uptime_delta.total_seconds()
        embed = discord.Embed(
            description=f"> **Betray's** uptime - <t:{int(self.bot.launch_time.timestamp())}:R>",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

    @command(aliases=["cred"])
    async def credit(self, ctx):
        embed = discord.Embed(
            description='> **own by and made by** - [`@yau`](https://betray.vip/yau)\n> **big thanks to [`@yurrion`](https://guns.lol/miah) for helping recode and make the bot**',
            color=0x2b2d31 
        )
        await ctx.send(embed=embed)

    @command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  
        embed = discord.Embed(
            description=f'> Bot ping: **{latency}ms**',
            color=0x2b2d31 
        )
        message = await ctx.send(embed=embed)
        button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="check status",
            url="https://betray.betteruptime.com/"
        )
        view = discord.ui.View()
        view.add_item(button)
        await message.edit(view=view)

    
    @command(aliases=["bi"])
    async def botinfo(self, ctx):
        total_users = sum(len(guild.members) for guild in self.bot.guilds)
        total_servers = len(self.bot.guilds)
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        command_count = len(self.bot.commands)
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(title="Betray", color=0x2b2d31)
        embed.add_field(name="Commands", value=f"**[{command_count}](https://betray.vip/cmds)**", inline=False)
        embed.add_field(name="Owner", value="[`@yau`](https://betray.vip/yau)", inline=False)
        embed.add_field(name="Users", value=f"{total_users}", inline=True)
        embed.add_field(name="Servers", value=f"{total_servers}", inline=True)
        embed.add_field(name="System", value=f"CPU usage - **{cpu_usage}%**\nMemory usage - **{memory_usage}%**\nBot ping - **{latency}ms**", inline=True)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed, view=MyView())


    @command(aliases=["uc"])
    async def usercount(self, ctx):
        members_count = sum(guild.member_count for guild in self.bot.guilds)
        embed = discord.Embed(
            description=f"> Managing ***{members_count}*** users.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

    @command(aliases=["sc"])
    async def servercount(self, ctx):
        servers_count = len(bot.guilds)
        embed = discord.Embed(
            description=f"> Managing ***{servers_count}*** servers.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

    @command(aliases=['av'])
    async def avatar(self, ctx, user: discord.User = None):
        if not user:
            user = ctx.author
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=user.avatar.url)
        avatar_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Avatar", url=user.avatar.url)
        view = discord.ui.View()
        view.add_item(avatar_button)
        await ctx.send(embed=embed, view=view)


    @command()
    async def banner(self, ctx: commands.Context, *, user: Union[Member, User] = None):
        if user is None:
            user = ctx.author
        else:
            if isinstance(user, str):
                try:
                    user = await MemberConverter().convert(ctx, user)
                except commands.MemberNotFound:
                    try:
                        user = await UserConverter().convert(ctx, user)
                    except commands.UserNotFound:
                        return await ctx.send(embed=discord.Embed(description="Invalid user."))
        info = await self.bot.fetch_user(user.id)
        if not info.banner:
            embed = discord.Embed(description=f'> {user.mention} has **no banner set**', color=0x2b2d31)
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x2b2d31, title=f"", url=info.banner.url)
            embed.set_image(url=info.banner.url)
            banner_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Banner", url=info.banner.url)
            view = discord.ui.View()
            view.add_item(banner_button)
            await ctx.send(embed=embed, view=view)

    @command(aliases=['srvicon'])
    async def servericon(self, ctx):
        server = ctx.guild
        if server.icon:
            embed = discord.Embed(color=0x2b2d31)
            embed.set_image(url=server.icon.url)
            icon_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Icon", url=server.icon.url)
            view = discord.ui.View()
            view.add_item(icon_button)
            await ctx.send(embed=embed, view=view)
        else:
            embed = discord.Embed(description=f'> This server does **not have** an icon yet.', color=0x2b2d31)
            await ctx.send(embed=embed)

    @command(aliases=['ui'])
    async def userinfo(self, ctx, user: discord.User = None):
        user = user or ctx.author
        embed = discord.Embed(title=f'User Info - {user.name}', color=0x2b2d31)
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name='Info', value=f'`{user.id}`', inline=False)
        embed.add_field(name='Account Created', value=f'<t:{int(user.created_at.timestamp())}:F>', inline=False)

        if isinstance(user, discord.Member):
            embed.add_field(name='Joined Server', value=f'<t:{int(user.joined_at.timestamp())}:F>', inline=False)
            roles = [role.mention for role in user.roles[1:]]
            embed.add_field(name='Roles', value=', '.join(roles) if roles else 'None', inline=False)
        else:
            guild = ctx.guild
            member = guild.get_member(user.id)
            if member:
                embed.add_field(name='Joined Server', value=f'<t:{int(member.joined_at.timestamp())}:F>', inline=False)
                roles = [role.mention for role in member.roles[1:]]
                embed.add_field(name='Roles', value=', '.join(roles) if roles else 'None', inline=False)
        
        info = await self.bot.fetch_user(user.id)
        banner_url = info.banner.url if info.banner else None
        
        view = discord.ui.View()
        profile_button = discord.ui.Button(style=discord.ButtonStyle.link, label="User Profile", url=f"https://discord.com/users/{user.id}")
        view.add_item(profile_button)

        if user.avatar:
            avatar_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Avatar", url=user.avatar.url)
            view.add_item(avatar_button)
        
        if banner_url:
            banner_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Banner", url=banner_url)
            view.add_item(banner_button)

        await ctx.send(embed=embed, view=view)

    @command(aliases=['si'])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        created_at = f'<t:{int(guild.created_at.timestamp())}:R>'
        verification_level = guild.verification_level
        verification_levels = {
            0: "None",
            1: "Low",
            2: "Medium",
            3: "High",
            4: "Very High"
        }
        verification = verification_levels.get(verification_level, "None")
        vanity_url = guild.vanity_url if guild.vanity_url else "None"
        if guild.vanity_url:
            invite_info = f"Vanity - {vanity_url}"
        else:
            invite = await ctx.channel.create_invite()
            invite_info = f"Invite - {invite.url}"
        boosts = guild.premium_subscription_count
        boost_level = guild.premium_tier
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        members = guild.member_count
        bots = sum(member.bot for member in guild.members)
        roles = len(guild.roles)
        max_emojis = guild.emoji_limit
        emojis = len(guild.emojis)
        max_stickers = guild.sticker_limit
        stickers = len(guild.stickers)
        embed = discord.Embed(
            title=f'{guild.name}',
            color=discord.Color(0x2b2d31)
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        embed.add_field(name="", value=f'Created {created_at}', inline=False)
        embed.add_field(name="info", value=f"```verification - {verification}\n{invite_info}\nboosts - {boosts}{' (level ' + str(boost_level) + ')' if boosts > 0 else ''}```", inline=False)
        embed.add_field(name="channels", value=f"```total - {text_channels + voice_channels}\ntext - {text_channels}\nvoice - {voice_channels}\ncategories - {categories}```", inline=False)
        embed.add_field(name="numbers", value=f"```roles - {roles}\nemojis - {emojis}\nstickers - {stickers}\nmembers - {members}\nbots - {bots}```", inline=False)
        embed.set_footer(text=f"ID - {guild.id}")
        buttons = []
        if guild.vanity_url:
            buttons.append(discord.ui.Button(style=discord.ButtonStyle.link, label="Server Invite", url=guild.vanity_url))
        else:
            buttons.append(discord.ui.Button(style=discord.ButtonStyle.link, label="Server Invite", url=invite.url))
        if guild.banner:
            buttons.append(discord.ui.Button(style=discord.ButtonStyle.link, label="Banner", url=guild.banner.url))
        if guild.icon:
            buttons.append(discord.ui.Button(style=discord.ButtonStyle.link, label="Icon", url=guild.icon.url))
        view = discord.ui.View()
        for button in buttons:
            view.add_item(button)
    
        await ctx.send(embed=embed, view=view)

    @command(aliases=['jp'])
    async def joinposition(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        try:
            join_position = sorted(ctx.guild.members, key=lambda m: m.joined_at).index(user) + 1
            embed = discord.Embed(description=f'> {user.mention} was the **{join_position}th** to join the server.', color=0x2b2d31)
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(description=f'> {user.mention} could not be found.', color=0x2b2d31)
            await ctx.send(embed=embed)
        except AttributeError:
            embed = discord.Embed(description=f'> user could not be found.', color=0x2b2d31)
            await ctx.send(embed=embed)
        
    @command()
    async def botcount(self, ctx):
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        embed = discord.Embed(description=f'> **{bot_count}** bots in the server.', color=0x2b2d31)
        await ctx.send(embed=embed)

    @command(aliases=['mc'])
    async def membercount(self, ctx):
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        total_members = len(ctx.guild.members)
        embed = discord.Embed(description=f'> **Members** - ***{total_members}***\n> **Bots** - ***{bot_count}***', color=0x2b2d31)
        await ctx.send(embed=embed)
    
    @command()
    async def iicon(self, ctx, invite_code: str = None):
        invite_link = f"https://discord.com/invite/{invite_code}"
    
        try:
            invite = await self.bot.fetch_invite(invite_code)
            guild = invite.guild
        
            if guild.icon:
                server_icon_url = guild.icon.url
                await ctx.send(server_icon_url)
            else:
                embed = discord.Embed(description='> Server has not got an icon', color=0x2b2d31)
                await ctx.send(embed=embed)
        except discord.errors.NotFound:
            embed = discord.Embed(description='> **Invalid** invite', color=0x2b2d31)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @command()
    async def isplash(self, ctx, invite_code: str = None):
        invite_link = f"https://discord.com/invite/{invite_code}"
    
        try:
            invite = await self.bot.fetch_invite(invite_code)
            guild = invite.guild
        
            if guild.splash:
                server_splash_url = guild.splash.url
                await ctx.send(server_splash_url)
            else:
                embed = discord.Embed(description='> server has not got a splash', color=0x2b2d31)
                await ctx.send(embed=embed)
        except discord.errors.NotFound:
            embed = discord.Embed(description='> **invalid** invite', color=0x2b2d31)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @command()
    async def createinvite(self, ctx, server_id: int = None):
        invite = await server.text_channels[0].create_invite()
        embed = discord.Embed(
            title="",
            description=f"Server invite for **{server.name}**\n**[Invite]({invite.url})**",
            color=0x2b2d31
        )
        invite_button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="Invite",
            url=invite.url
        )
        view = discord.ui.View()
        view.add_item(invite_button)
        await ctx.send(embed=embed, view=view)
    
@command()
async def ibanner(ctx, invite_code: str = None):
    invite_link = f"https://discord.com/invite/{invite_code}"
    
    try:
        invite = await command.fetch_invite(invite_code)
        guild = invite.guild
        
        if guild.banner:
            server_banner_url = guild.banner.url
            await ctx.send(server_banner_url)
        else:
            embed = discord.Embed(description='> server has not got a banner', color=0x2b2d31)
            await ctx.send(embed=embed)
    except discord.errors.NotFound:
        embed = discord.Embed(description='> **invalid** invite', color=0x2b2d31)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error: {e}")
    
    @command()
    async def support(self, ctx):
        embed = discord.Embed(
            description='> Join our **support** server **[here](https://discord.gg/betray)**',
            color=0x2b2d31
        )
        message = await ctx.send(embed=embed)
        button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="join support",
            url="https://discord.gg/betray"
        )
        view = discord.ui.View()
        view.add_item(button)
        await message.edit(view=view)

    @command(aliases=["cc"])
    async def commandcount(self, ctx):
        command_count = len(bot.commands)
        embed = discord.Embed(
            description=f"> ***[{command_count}](https://betray.vip/cmds)*** cmds loaded.",
            color=0x2b2d31
        )
        message = await ctx.send(embed=embed)
        button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="cmds",
            url="https://betray.vip/cmds"
        )
        view = discord.ui.View()
        view.add_item(button)
        await message.edit(view=view)
        
    @command()
    async def botcount(self, ctx):
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        embed = discord.Embed(description=f'> **{bot_count}** bots in the server.', color=0x2b2d31)
        await ctx.send(embed=embed)
        
    @command(aliases=["cc"])
    async def commandcount(self, ctx):
        command_count = len(bot.commands)
        embed = discord.Embed(
            description=f"> ***[{command_count}](https://betray.vip/cmds)*** cmds loaded.",
            color=0x2b2d31
        )
        message = await ctx.send(embed=embed)
        button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="cmds",
            url="https://betray.vip/cmds"
        )
        view = discord.ui.View()
        view.add_item(button)
        await message.edit(view=view)
        
    @command(aliases=["inv"])
    async def invite(self, ctx):
        embed = discord.Embed(
            description='> Invite our bot **[here](https://discord.com/oauth2/authorize?client_id=1211780078858534983&permissions=8&scope=bot)**',
            color=0x2b2d31 
        )
        message = await ctx.send(embed=embed)
        button = discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="invite",
            url="https://discord.com/oauth2/authorize?client_id=1211780078858534983&permissions=8&scope=bot"
        )
        view = discord.ui.View()
        view.add_item(button)
        await message.edit(view=view)
    
    @command()
    async def purchasetos(self, ctx):
        title = "purchase tos"
        embed = discord.Embed(
            title=title,
            description=(
                "**Last updated - <t:1710795848:d>**\n"
                "*when you buy a premium whitelist you agree to our purchase tos*\n\n"
                "**<:whitedot:1213604287947472997> only pay with friends and family on paypal or you just get a refund and not get a whitlist**\n"
                "**<:whitedot:1213604287947472997> only the user who purchased the whitelist can claim the whitelist**\n"
                "**<:whitedot:1213604287947472997> if you do not provide proof of purchase or evidence you bought the whitelist you will not be able to claim the whitelist**\n"
                "**<:whitedot:1213604287947472997> if you pay under the amount needed for the whitelist you will not be able to claim your whitelist**\n"
                "**<:whitedot:1213604287947472997> no refunds after 24h after purchase**\n"
                "**<:whitedot:1213604287947472997> charge back on paypal = blacklist from betray**\n"
                "**<:whitedot:1213604287947472997> we have the right to change the terms of service at any point**\n"
            ),
            color=0x2b2d31
        )
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(info(bot))