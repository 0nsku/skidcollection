import discord
from discord.ext import commands

class logs2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        command_prefix = await self.client.get_prefix(message)

        if message.content.startswith(command_prefix):
            author = f'{message.author.name}'
            authorav = message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
            guild = message.guild.name
            serverav = message.guild.icon.url if message.guild.icon else None

            log_embed = discord.Embed(
                color=0xCCCCCC,
                title='Command:',
                description=message.content,
            )
            log_embed.set_author(name=author, icon_url=authorav)
            log_embed.set_footer(text=guild, icon_url=serverav)

            log_channel = self.client.get_channel(1215297525368496209)
            if log_channel:
                await log_channel.send(embed=log_embed)
            else:
                print(f'no channel id dumbass')


async def setup(client):
    await client.add_cog(logs2(client))