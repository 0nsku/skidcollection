import discord
from discord.ext import commands
import config

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='purge',
        aliases=['clear']
    )
    async def purge(self, ctx: commands.Context, len: int = 1):
        amount = len + 1
        await ctx.channel.purge(limit=amount)
        await ctx.send(
            embed=discord.Embed(
                color=config.Colors.default,
                description=f'✅ {ctx.author.mention} : Sucessfully removed {len} messages.'
            ),
            delete_after=5
        )

    @commands.command(
        name='lock'
    )
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx: commands.Context, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'locked by {ctx.author.name}')
        await ctx.reply(
            embed = discord.Embed(
                color=config.Colors.default,
                description=f'✅ {ctx.author.mention} : Sucessfully locked {ctx.channel.mention}'
            )
        )


    @commands.command(
        name='lockall',
        aliases=['lockdown']
    )
    @commands.has_permissions(manage_channels=True)
    async def lockall(self, ctx: commands.Context):
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            for channels in list(ctx.guild.text_channels):
                overwrite = channels.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                await channels.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'lockall command executed by : {ctx.author.name}')
                await ctx.send(
                    embed = discord.Embed(
                        color=config.Colors.default,
                        description=f'✅ {ctx.author.mention} : The whole server is locked.'
                    )
                )
        else:
            await ctx.reply('❌ Command Execution failed due to role hierchy', delete_after=5)

    @commands.command(
        name='unlock'
    )
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'unlocked by {ctx.author.name}')
        await ctx.reply(
            embed = discord.Embed(
                color=config.Colors.default,
                description=f'✅ {ctx.author.mention} : Sucessfully unlocked {ctx.channel.mention}'
            )
        )

    @commands.command(
        name='unlockall',
        aliases=['unlockdown']
    )
    @commands.has_permissions(manage_channels=True)
    async def unlockall(self, ctx: commands.Context):
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            for channels in list(ctx.guild.text_channels):
                overwrite = channels.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = True
                await channels.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'unlockall command executed by : {ctx.author.name}')
                await ctx.send(
                    embed = discord.Embed(
                        color=config.Colors.default,
                        description=f'✅ {ctx.author.mention} : The whole server is unlocked.'
                    )
                )
        else:
            await ctx.reply('❌ Command Execution failed due to role hierchy', delete_after=5)


    @commands.command(
        name='hide'
    )
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx: commands.Context, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'hidden by {ctx.author.name}')
        await ctx.reply(
            embed = discord.Embed(
                color=config.Colors.default,
                description=f'✅ {ctx.author.mention} : Sucessfully hid {ctx.channel.mention}'
            )
        )

    @commands.command(
        name='unhide'
    )
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx: commands.Context, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'unhidden by {ctx.author.name}')
        await ctx.reply(
            embed = discord.Embed(
                color=config.Colors.default,
                description=f'✅ {ctx.author.mention} : Sucessfully unhid {ctx.channel.mention}'
            )
        )

    @commands.command(
        name='hideall',
        aliases=['shutdown']
    )
    @commands.has_permissions(manage_channels=True)
    async def hideall(self, ctx: commands.Context):
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            for channels in list(ctx.guild.text_channels):
                overwrite = channels.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channels.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f'hideall command executed by : {ctx.author.name}')
                await ctx.send(
                    embed = discord.Embed(
                        color=config.Colors.default,
                        description=f'✅ {ctx.author.mention} : The whole server is shutted down.'
                    )
                )
        else:
            await ctx.reply('❌ Command Execution failed due to role hierchy', delete_after=5)


    @commands.command(
        name='role'
    )
    async def role(self, ctx: commands.Context, member: discord.Member = None, role: discord.Role = None):
        if member is None:
            return await ctx.send(
                embed=discord.Embed(
                    color=config.Colors.default,
                    description=f'❌ {ctx.author.mention} : You need to mention a valid member to give roles.'
                )
            )
        if role is None:
            return await ctx.send(
                embed=discord.Embed(
                    color=config.Colors.default,
                    description=f'❌ {ctx.author.mention} : You need to mention a role to give the member.'
                )
            )
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(
                    embed=discord.Embed(
                    color=config.Colors.default,
                    description=f'✅  | Changed roles for {member.name} -{role.name}'
                    )
                )
            if ctx.author.top_role.position >= role.position:
                await member.add_roles(role)
                await ctx.send(
                    embed=discord.Embed(
                    color=config.Colors.default,
                    description=f'✅  | Changed roles for {member.name} +{role.name}'
                    )
                )
            else:
                await ctx.reply(" You must have roles above that role to use this command!", mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(color=3158326, description="Get a higher role nigga."), mention_author=False)

    @commands.command()
    async def ban(self, ctx,member : discord.Member,*,reason= "No reason provided"):
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            if ctx.author.top_role >= member.top_role or ctx.author == ctx.guild.owner:
                if not member:
                    await ctx.reply("Provide a user for unbanning!")
                else:
                    try:
                        await member.ban(reason=reason)
                        koki = discord.Embed(color=3158326,description=f"executed {member.mention}")
                        await ctx.reply(embed=koki, mention_author=False)
                    except Exception as e:
                        embed=discord.Embed(title="Error", description=f'{e}')
                        await ctx.reply(embed=embed)
            else:
                await ctx.reply("get an higher role to ban that man bud.")
        else:
            await ctx.reply(embed=discord.Embed(color=3158326, description="Get a higher role nigga."), mention_author=False)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx,member : discord.Member,*,reason= "No reason provided by moderator."):
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            if ctx.author.top_role >= member.top_role or ctx.author == ctx.guild.owner:
                if not member:
                    embed = discord.Embed(color=3158326, description=f"{ctx.author.mention} provide a user to kick") 
                    await ctx.reply(embed=embed, mention_author=False)
                else:   
                    try:
                        await member.kick(reason=reason)
                        embed=discord.Embed(color=3158326, description=f"{member.name}\n<:icons_reply:969824831719759872> kicked that member\n<:icons_reply:969824831719759872> for reason: {reason}\n<:icons_reply:969824831719759872> action taken by {ctx.author.mention}")
                        await ctx.reply(embed=embed, mention_author=False)
                    except Exception as e:
                        embed=discord.Embed(color=3158326, title="Error", description=f'{e}')
                        await ctx.reply(embed=embed, mention_author=False)
            else:
                await ctx.reply(embed=discord.Embed(color=3158326, description="Get a higher role nigga."))
        else:
            await ctx.reply(embed=discord.Embed(color=3158326, description="Get a higher role nigga."))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,*,member=None):
        if ctx.author.top_role >= ctx.guild.me.top_role or ctx.author == ctx.guild.owner:
            if ctx.author.top_role >= member.top_role or ctx.author == ctx.guild.owner:
                if not member:
                    embed = discord.Embed(color=3158326, description=f"{ctx.author.mention} provide a user to unban.")
                    await ctx.reply(" Provide a user for unbanning!", mention_author=False)
                else: 
                    try:
                        banned_users = await ctx.guild.bans()
                        member_name, member_disc = member.split('#')
                        for banned_entry in banned_users:
                            user = banned_entry.user
                            if(user.name, user.discriminator)==(member_name, member_disc):
                                embed=discord.Embed(title=f"{self.user.name}", description="<:icons_like:969823693284990980> Unbanned that user!") 
                                embed.add_field(name="**User:**", value=f"`{member_name}`", inline=False)
                                embed.add_field(name="**Moderator:**", value=f"{ctx.author.mention}", inline=False)
                                await ctx.guild.unban(user)
                                await ctx.reply(embed=embed, mention_author=False)
                                return
                    except Exception as e:
                        embed=discord.Embed(title="Error", description=f'{e}')
                        await ctx.reply(embed=embed, mention_author=False)
            else:
                await ctx.reply(" Your role is not enough higher to kick that user!", mention_author=False)
        else:
            await ctx.reply(embed=discord.Embed(color=3158326, description="Get a higher role nigga."), mention_author=False)


async def setup(bot):
    await bot.add_cog(Moderation(bot))