import discord
from discord.ext import commands
from discord.ext.commands import commabd, Cog, has_permissions

class mod(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @Cog.listener("on_message_delete")
    async def snipelog(message):
        snipe_data[message.channel.id] = {
            'author': message.author,
            'content': message.content,
            'timestamp': message.created_at
        }

    @command()
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx: commands.Context, time_input: str, *, reason: str = "no reason provided"):
        seconds = parse_time(time_input).total_seconds()
        if seconds > 21600:
            embed = discord.Embed(
                description="> Slowmode can't be more than **21600s**.",
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)
            return
    
        if ctx.channel.slowmode_delay == seconds:
            embed = discord.Embed(
                description=f"> The slowmode is already set to **{time_input}** for {ctx.channel.mention}.",
                color=0x2b2d31  
            )
            await ctx.send(embed=embed)
            return
    
        await ctx.channel.edit(slowmode_delay=int(seconds), reason=f"Slowmode: used by {ctx.author}, Reason: {reason}")
    
         
        embed = discord.Embed(
            description=f"> Slowmode has been set to **{time_input}** for {ctx.channel.mention}.",
            color=0x2b2d31  
        )
        await ctx.send(embed=embed)


    @command()
    async def lock(ctx):
        if ctx.author.guild_permissions.manage_channels:
            channel = ctx.channel
            everyone_role = ctx.guild.default_role
            await channel.set_permissions(everyone_role, send_messages=False)

            embed = discord.Embed(  
                description=f'> {channel.mention} has been locked.',
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)

          
      else:
          embed = discord.Embed(
            description="> You or me are missing **manage_channel** perms.",
            color=0x2b2d31  
        )
        await ctx.send(embed=embed)

    @command()
    async def unlock(ctx):
        if ctx.author.guild_permissions.manage_channels:
            channel = ctx.channel
            everyone_role = ctx.guild.default_role
             await channel.set_permissions(everyone_role, send_messages=True)
            embed = discord.Embed(
                description=f'> {channel.mention} has been unlocked.',
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="> You or me are missing **manage_channel** perms.",
                color=0x2b2d31  
            )
            await ctx.send(embed=embed)

    @command()
    async def hide(ctx):
        if ctx.author.guild_permissions.manage_channels:
            channel = ctx.channel
            await channel.set_permissions(ctx.guild.default_role, read_messages=False)
            embed = discord.Embed(
                description=f'> {channel.mention} has been hidden.',
                color=0x2b2d31  
            )
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description="> You or me are missing **manage_channel** perms.",
                color=0x2b2d31  
            )
            await ctx.send(embed=embed)

    @command()
    async def unhide(self, ctx):
        if ctx.author.guild_permissions.manage_channels:
            channel = ctx.channel
            await channel.set_permissions(ctx.guild.default_role, read_messages=True)
            embed = discord.Embed(
                description=f'> {channel.mention} has been made visible.',
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="> You or me are missing **manage_channel** perms.",
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)

    @command(aliases=['bye','fuckoff','fuckyou'])
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member = None):
        try:
            await member.ban()
            embed = discord.Embed(
                description=f'> {member.mention} has been **banned**.',
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                description="> You or I are missing **ban_members** permissions.",
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)

    @command()
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, *, user: str = None):
        try:
            banned_users = await ctx.guild.fetch_bans()
            for ban_entry in banned_users:
                user_info = ban_entry.user
                if str(user_info.id) == str(user) or user_info.name.lower() == user.lower():
                    await ctx.guild.unban(user_info)
                    embed = discord.Embed(
                        description=f'> {user_info.mention} has been **unbanned**.',
                        color=0x2b2d31
                    )
                    await ctx.send(embed=embed)
                    return
            embed = discord.Embed(
                description=f'> "{user}" is **not banned**.',
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                description="> You or I are missing **ban_members** permissions.",
                color=0x2b2d31 
            )
            await ctx.send(embed=embed)

@command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None):
    try:
        await member.kick()
        embed = discord.Embed(
            title='',
            description=f'> {member.mention} has been **kicked**.',
            color=0x2b2d31
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            title='',
            description="> You or me are missing **kick_members** perms.",
            color=0x2b2d31 
        )
        await ctx.send(embed=embed)

@bot.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    if amount <= 0:
        embed = discord.Embed(
            title='',
            description='Provide a **valid number** of messages to clear.',
            color=0x2b2d31
        )
        message = await ctx.send(embed=embed)
        return
    try:
        cleared = await ctx.channel.purge(limit=amount + 1) 
        cleared_amount = len(cleared) - 1 
        embed = discord.Embed(
            title='',
            description=f'> Cleared **{cleared_amount}** messages by {ctx.author.mention}.',
            color=0x2b2d31
        )
        message = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await message.delete()
    except discord.Forbidden:
        embed = discord.Embed(
            color=0x2b2d31,
            description="You or I are missing **manage_messages** permissions."
        )
        message = await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    try:
        new_channel = await ctx.channel.clone()
        user = ctx.author
        await ctx.channel.delete()
        await new_channel.send(f'first')
    except discord.Forbidden:
        embed = discord.Embed(
            title='',
            description='> You or me are missing **manage_channels** perms.',
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, user: discord.Member, *, role_input: Union[discord.Role, str]):
    if isinstance(role_input, str):
        role = discord.utils.get(ctx.guild.roles, name=role_input)
    else:
        role = role_input

    if role is None:
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"> Role name **{role_input}** not found."
        )
        await ctx.send(embed=embed)
        return
    try:
        await user.add_roles(role)
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"> **Added** {role.mention} to {user.mention}"
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            color=0x2b2d31,
            description="> You or I are missing **manage_roles** permissions."
        )
        await ctx.send(embed=embed)

@bot.command(aliases=['derole'])
@commands.has_permissions(manage_roles=True)
async def unrole(ctx, user: discord.Member, *, role_input: Union[discord.Role, str]):
    if isinstance(role_input, str):
        role = discord.utils.get(ctx.guild.roles, name=role_input)
    else:
        role = role_input
    if role is None:
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"> Role name **{role_input}** not found."
        )
        await ctx.send(embed=embed)
        return
    if role not in user.roles:
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"> {user.mention} does **not** have the role {role.mention}."
        )
        await ctx.send(embed=embed)
        return
    try:
        await user.remove_roles(role)
        embed = discord.Embed(
            color=0x2b2d31,
            description=f"> **Removed** {role.mention} from {user.mention}"
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(
            color=0x2b2d31,
            description="> You or I are missing **manage_roles** permissions."
        )
        await ctx.send(embed=embed)

@bot.command()
async def snipe(ctx):
    channel_id = ctx.channel.id
    if channel_id in snipe_data:
        snipe_info = snipe_data[channel_id]
        user_mention = bot.get_user(snipe_info["author"])
        if user_mention:
            user_mention_text = user_mention.mention
        else:
            user_mention_text = f"{snipe_info['author']}"
        embed = discord.Embed(
            title='Sniped Message',
            description=f'**User - {user_mention_text}**\n**message** ```{snipe_info["content"]}```',
            color=0x2b2d31,
            timestamp=snipe_info['timestamp']
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='',
            description='> **No deleted messages** to snipe in **this** channel.',
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_emojis=True)
async def stealemoji(ctx, emoji: Union[discord.Emoji, discord.PartialEmoji], *, name: str=None):
    embed = discord.Embed(color=0x2b2d31) 
    try:
        if not name:
            name = emoji.name 
        if isinstance(emoji, discord.Emoji):
            image_url = emoji.url
        elif isinstance(emoji, discord.PartialEmoji):
            image_url = emoji.url
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image = await resp.read()
        created_emoji = await ctx.guild.create_custom_emoji(image=image, name=name)
        embed.description = f"**Stolen** the emoji {created_emoji}"
    except discord.HTTPException as e:
        embed.description = f"Unable to add the emoji: {e}"
    except commands.MissingPermissions:
        embed.description = "> You or I are missing **manage_emojis** permissions."
    await ctx.send(embed=embed)
    
@bot.command()
async def nsfwenable(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels:
            try:
                await ctx.channel.edit(nsfw=True)
                embed = discord.Embed(
                    description=">  **NSFW** has been enabled in this channel.",
                    color=0x2b2d31
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description="I **don't have permission** to edit channel settings.",
                    color=0x2b2d31
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="**You don't have permission** to use this command.",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
    else:
                    embed = discord.Embed(
                description="**You don't have permission** to use this command.",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description="This command can **only** be used in text channels.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)
        
        
@bot.command()
async def nsfwdisable(ctx):
    if isinstance(ctx.channel, discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels:
            try:
                await ctx.channel.edit(nsfw=False)
                embed = discord.Embed(
                    description=">  **NSFW** has been disabled in this channel.",
                    color=0x2b2d31
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description="**I don't have permission** to edit channel settings.",
                    color=0x2b2d31
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="**You don't have permission** to use this command.",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description="This command can **only** be used in text channels.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)
