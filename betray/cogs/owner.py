import discord
from discord.ext.commands import command, Cog, is_owner

 class owner(Cog):
    def __init__(self, bot)
        self.bot = bot
    @command()
    @is_owner
    async def restart(self, ctx):
        global is_restarting
            await ctx.send(embed=embed)
            return
        if not is_restarting:
            is_restarting = True
            embed = discord.Embed(description=f'> Restarting...', color=0x2b2d31)
            await ctx.send(embed=embed)
            await self.bot.close()
            os.system("home/container/main.py")

    @command()
    @is_owner
    async def leavesrv(self, ctx, server_id: int = None):
        if ctx.author.id not in owner_ids:
            embed = discord.Embed(description=f"nuh uh buddy, you aint an owner.", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        if server_id:
            guild = self.bot.get_guild(server_id)
            if guild:
                await guild.leave()
                embed = discord.Embed(description="Leaving server.", color=0x2b2d31)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Couldn't find a server with that ID.")
        else:
            embed = discord.Embed(description="Leaving server.", color=0x2b2d31)
            await ctx.send(embed=embed)
            await ctx.guild.leave()

    @command()
    async def dm(self, ctx, member: discord.Member, *, message):
        try:
            await member.send(message)
            embed = discord.Embed(description=f"Sent DM to {member.mention}.", color=0x2b2d31)
             await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description=f"Failed - {e}.", color=0x2b2d31)
            await ctx.send(embed=embed)

    @command()
    async def statemb(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Restarting . . .", color=0x2b2d31)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        reply_embed = discord.Embed(description="> **Restarted** <#1211776141577297940> for an update.", color=0x2b2d31)
        await message.reply(embed=reply_embed)

    @command()
    async def createtemplate(self, ctx): 
        template = await ctx.guild.create_template(name="betray server template", description="this is a template")
        embed = discord.Embed(title="", description=f"server template - [template]({template.url})", color=0x2b2d31)
        await ctx.send(embed=embed)

    @command()
    @is_owner()
    async def allservers(self, ctx):
        if ctx.guild is not None:
            guilds = ctx.bot.guilds
            for guild in guilds:
                try:
                    invite = await guild.text_channels[0].create_invite(max_age=86400)
                    await ctx.send(f"**Server: {guild.name}**\n{invite}")
                except discord.Forbidden:
                    await ctx.send(f"**Server: {guild.name}**\nUnable to create invite link due to insufficient permissions.\n")

    @command()
    async def payment(self, ctx):
        title = "betray premium"
        embed = discord.Embed(
            title=title,
            description=(
                "<:eth:1219384518159634484> - `0x1f4d31b8278bFE254b462651d1072C61A328BA87`\n"
                "<:LTC:1219387927390322889> - `LaE9C7KdiKVKvqpWBAVQMvYntxMM7c9G9t`\n"
                "<:btc:1219384504959893564> - `bc1qtr8ydg6q2edcxasgvjxltdkpp3w8wn4lzcs528`\n"
                "<:paypal:1219384530088230962> - **[paypal](https://paypal.com)**\n\n"
                "**$5 for lifetime premium whitelist**\n"
                "**> Premium benefits, you will get all premium cmds in https://bertay.vip/cmds**\n"
                "> **Open a [ticket](https://discord.com/channels/1190116499344605346/1219385862954025051) in [our support server](https://discord.gg/betray) and send proof of purchase.**"
            ),
            color=0x2b2d31
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(owner)