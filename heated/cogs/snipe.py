import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.deleted_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_messages.setdefault(message.channel.id, []).append(message)

    @commands.command(aliases=['s'])
    async def snipe(self, ctx, index: int = 1):
        channel_id = ctx.channel.id
        sniped_messages = self.deleted_messages.get(channel_id, [])

        if sniped_messages:
            if 1 <= index <= len(sniped_messages):
                deleted_message = sniped_messages[-index]

                deleting_user = ctx.guild.get_member(int(deleted_message.author.id))

                message_user = ctx.guild.get_member(int(deleted_message.author.id))

                user_pfp = message_user.avatar.url if message_user.avatar else message_user.default_avatar.url

                embed = discord.Embed(
                    title=f'',
                    description=deleted_message.content,
                    color=0xCCCCCC
                )
                embed.set_author(name=message_user.display_name, icon_url=user_pfp)
                embed.set_footer(text=f'Page {index} of {len(sniped_messages)}')

                await ctx.send(embed=embed)
            else:
                await ctx.send('Invalid snipe index. Please specify a valid index.')
        else:
            await ctx.send('No deleted messages to snipe.')

async def setup(client):
    await client.add_cog(Utility(client))