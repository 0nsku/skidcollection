from discord.ext import commands
import config
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} ({self.bot.user.id})")
        await self.bot.change_presence(status= discord.Status.idle, activity = discord.Streaming(name = "rep /slacks", url = "https://www.twitch.tv/Discord"))

    
    @commands.Cog.listener()
    async def on_presence_update(self, before : discord.Member, after: discord.Member):
        if before.activities == after.activities:
            return
        userActivity = None
        guild = self.bot.get_guild(config.VanityRoles.haunt)
        chan = guild.get_channel(config.VanityRoles.logchan)
        role = guild.get_role(config.VanityRoles.hauntrole)
        for activity in after.activities:
            if isinstance(activity, discord.CustomActivity):
                if '/slacks' in str(activity):
                    userActivity = True

        if userActivity is True:
            if before.status == discord.Status.offline:
                return
            if role in after.roles:
                return
            else:
                await after.add_roles(role, reason='repped /slacks in their status.')
                await chan.send(f"{after.mention}",
                    embed = discord.Embed(
                        color=config.Colors.default,
                        description=f'ty for putting **/slacks** in your status; you now have the <@&{config.VanityRoles.hauntrole}> role.',
                        title='𝚒𝚕𝚢 ☆'
                    ).set_thumbnail(
                        url=after.display_avatar.url
                    ).set_footer(
                        text='enjoy your pic perms'
                    )
                )
        else:
            if after.status == discord.Status.offline:
                return
            if not role in after.roles:
                return
            else:
                await after.remove_roles(role, reason='removed the vanity.')
                await chan.send(
                    embed = discord.Embed(
                        color=config.Colors.default,
                        description=f'<:icons_Wrong:969824246241042442> removed role from {after.mention}.\n<:icons_warning:969824136014745630> removed vanity from their status.'
                    )
                )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        chan = self.bot.get_channel(config.Welcome.mainCh)
        chan2 = self.bot.get_channel(config.Welcome.chatCh)
        r1 = discord.utils.get(member.guild.roles, name = 'haunt w')
        r2 = discord.utils.get(member.guild.roles, name="/slacks")
        mainEmbed = discord.Embed(color = config.Colors.default, description = "<:rule:1092317181334786141>** ; **[/slacks](https://discord.com/channels/1077555829697413212/1217436545578172496)")
        mainEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1218053208874684527/1218055331314139166/a_2983e8c0221e797ea375415e9f60ab08.gif?ex=6606456d&is=65f3d06d&hm=a3393208b7c6286d6b5d3db00ac352d42460be33abc1cc5d8066b16145f1b561&")
        await chan.send(f"{member.mention}", embed=mainEmbed)
        cembed = discord.Embed(color = 2895153,description = "⠀        welc **@haunt**\n  ⠀     [rules](https://discord.com/channels/1077555829697413212/1217436545578172496)﹒[msg](https://discord.com/channels/1077555829697413212/1217436561574985769)﹒[rich](https://discord.com/channels/1077555829697413212/1217436559658192966)")
        cembed.set_thumbnail(url=f'{member.display_avatar.url}')
        cembed.set_footer(text=f"{member.guild.member_count}th")
        await chan2.send(f"<@&1092317403196706896> <:bfly:1092317941523025952> {member.name}", embed=cembed)
        await member.add_roles(r1, r2, reason='heil autorole')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(1077555829697413212)
        leac = self.bot.get_channel(1218274690494107668)
        embed = discord.Embed(color=config.Colors.default, description=f"fuck <@{member.id}>\nall my homies hate {member.name} *\n we have **{guild.member_count}** trollers left <:spiderop:1086953104735473714>")
        await leac.send("bye loser",embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot))