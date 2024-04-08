import discord
import datetime
import config
import requests
from discord.ext import commands
from io import BytesIO
from PIL import Image

class UtilCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(
        name='ping'
    )
    async def ping(self, ctx: commands.Context):
        e = discord.Embed(
            color=config.Colors.default,
            description=f'it took `{round(self.bot.latency * 1000)}` ms to ping the me.',
            timestamp=datetime.datetime.utcnow()
        )
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        e.set_footer(text=f'requested by {ctx.author.name}')
        async with ctx.typing():
            await ctx.reply(embed=e)

    @commands.command(aliases=["ri"])
    async def roleinfo(self, ctx, role:discord.Role):
        members_with_role = role.members
        embed=discord.Embed(color=config.Colors.default)
        member_names = [member.name for member in members_with_role]
        embed.add_field(name=f"{len(members_with_role)} users have '{role}' role.",value="\n ".join(member_names), inline=False)
        perm_list = ("\n".join([perm[0] for perm in role.permissions if perm[1]]).title().replace("_", " "))
        if "Administrator" in perm_list:
                perm_list = "**Administrator**"
        if not perm_list:
                perm_list = "None"
        embed.add_field(name="perms", value=perm_list, inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def nick(self, ctx, member: discord.Member, *, nickname: str= None):
        if nickname is None:
            nickname = member.global_name
        await member.edit(nick=nickname)
        embed = discord.Embed(color=config.Colors.default, description=f"{member.name}\n<:icons_reply:969824831719759872> changed nick to {nickname}\n<:icons_reply:969824831719759872> action taken by {ctx.message.author}")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["mc"])
    async def membercount(self, ctx):
        embed = discord.Embed(color=config.Colors.default, description=f"{ctx.guild.member_count} niggers are in the server rn.")
        async with ctx.typing():
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        total_text_channels = len(guild.text_channels)
        total_voice_channels = len(guild.voice_channels)
        total_channels = total_text_channels  + total_voice_channels 
        total_roles = len(guild.roles)

        embed=discord.Embed(color=3158326, description=f"**__{guild.name}__**\n**<:icons_reply:969824831719759872> own; {guild.owner.mention}\n<:icons_reply:969824831719759872> contains {total_roles} roles, {total_voice_channels} voice channels and {total_text_channels} text channels\n<:icons_reply:969824831719759872> since {ctx.guild.created_at.strftime('%d %b %Y')}\n**")
        async with ctx.typing():
            await ctx.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member: 
            member = ctx.message.author  
            embed = discord.Embed(color=config.Colors.default, timestamp=datetime.datetime.utcnow(),title=f"Avatar of - {member}")
            embed.set_image(url=member.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
        else:  
            embed = discord.Embed(color=config.Colors.default, timestamp=datetime.datetime.utcnow(),title=f"Avatar of - {member}")
            embed.set_image(url=member.avatar.url)
            async with ctx.typing():
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["whois", "ui"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:  
            member = ctx.message.author  
            roles = [role for role in member.roles]
            embed = discord.Embed(description=f"**{member.name}**\n<:icons_reply:969824831719759872> currently on {str(member.status)}\n<:icons_reply:969824831719759872>userid: `{member.id}`\n\n**Dates**\n<:icons_reply:969824831719759872> **joined**@ {member.joined_at.strftime('%d %b %Y(%a) ')}\n<:icons_reply:969824831719759872>** created**@ {member.created_at.strftime('%d %b %Y(%a)')}\n\n**Links**\n[avatar]({member.display_avatar.url}); ", color=3158326)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=f"{member}", icon_url=f'{member.display_avatar.url}')
            embed.add_field(name=f"Roles[{len(member.roles)}]:", value="".join([role.mention for role in roles]), inline=False)
            await ctx.reply(embed=embed, mention_author=False) 
        else:
            roles = [role for role in member.roles]
            embed = discord.Embed(color=3158326, description=f"**{member.name}**\n<:icons_reply:969824831719759872> currently on {str(member.status)}\n<:icons_reply:969824831719759872>userid: `{member.id}`\n\n**Dates**\n<:icons_reply:969824831719759872> **joined**@ {member.joined_at.strftime('%d %b %Y(%a) ')}\n<:icons_reply:969824831719759872>** created**@ {member.created_at.strftime('%d %b %Y(%a)')}\n\n**Links**\n[avatar]({member.display_avatar.url}); ")
            embed.add_field(name=f"Roles[{len(member.roles)}]:", value="".join([role.mention for role in roles]))
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=f"{member}", icon_url=f'{member.display_avatar.url}')
        
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def pin(self, ctx):
        if ctx.message.reference is not None:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await replied_message.pin()
            embed=discord.Embed(color=3158326, description=f"successfully pinned:\n```{replied_message.content}```")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send('Please reply to a message to pin it.')

    @commands.command()
    async def unpin(self, ctx, *,cntnt):
        if cntnt is None:
            return await ctx.send('Please Enter a valid content to unpin.')
        pinned_messages = await ctx.channel.pins()
        for message in pinned_messages:
            if message.content.startswith(cntnt):
                await message.unpin()
                embed = discord.Embed(color=3158326, description=f"successfully unpinned:\n ```{message.content}```")
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def capture(self, ctx, url):
        if url is None:
            return await ctx.send('Please Enter a valid url to use this')
        response = requests.get(f'https://image.thum.io/get/width/1920/crop/1080/{url}')
        img = Image.open(BytesIO(response.content))
        img.save('screenshot.png')
        await ctx.send(file=discord.File('screenshot.png'))


    @commands.command()
    async def device(self, ctx, user:discord.Member=None):
        if user == None:
            user = ctx.message.author
        off = "offline"
        mob = f"{user.mobile_status}"
        desk = f"{user.desktop_status}"
        web = f"{user.web_status}"

        
        if mob == off and desk == off and web == off: 
            embed = discord.Embed( description="either offline or invisible", color=3158326)
            await ctx.reply(embed=embed)

            
        elif mob != off and desk != off and web != off: 
            embed = discord.Embed(description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on mob, web & desktop", color=3158326)
            await ctx.reply(embed=embed, mention_author=False)

            
        elif desk == off and web == off: 
            embed = discord.Embed(description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on mob.", color=3158326)
            embed.set_thumbnail(url=user.display_avatar.url)
            await ctx.reply(embed=embed, mention_author=False) 

            
        elif mob == off and desk == off:
            embed = discord.Embed( description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on web.", color=3158326) 
            await ctx.reply(embed=embed, mention_author=False)

            
        elif mob == off and web == off: 
            embed = discord.Embed(description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on pc.", color=3158326) 
            await ctx.reply(embed=embed, mention_author=False)

            
        elif desk == off:
            embed = discord.Embed(description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on both mob and web.", color=3158326)
            await ctx.reply(embed=embed, mention_author=False)

            
        elif web == off: 
            embed = discord.Embed(description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on both mob and pc", color=3158326)
            await ctx.reply(embed=embed, mention_author=False)

            
        elif mob == off:    
            embed = discord.Embed(description=f"{user.name}\n<:icons_reply:969824831719759872> using cord on both web and pc.", color=3158326)
            await ctx.reply(embed=embed, mention_author=False)
            
        else:
            await ctx.reply("unable to fetch user.", mention_author=False)


async def setup(bot):
    await bot.add_cog(UtilCmds(bot))