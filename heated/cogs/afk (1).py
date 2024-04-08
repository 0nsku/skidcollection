import discord
from discord.ext import commands
import sqlite3

class afk(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.connection = sqlite3.connect('afk.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS afk_users (
                user_id INTEGER PRIMARY KEY,
                message TEXT
            )
        ''')
        self.connection.commit()

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def afk(self, ctx, *, message: str = f"I'm currently AFK."):
        self.cursor.execute('''
            INSERT OR REPLACE INTO afk_users (user_id, message) VALUES (?, ?)
        ''', (ctx.author.id, message))
        self.connection.commit()

        afk_embed = discord.Embed(
            description=f"> :zzz:{ctx.author.mention} is now AFK, with the status: **{message}**",
            color=discord.Color.blue()
        )

        await ctx.send(embed=afk_embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.client.user.id and not message.content.startswith(self.client.command_prefix(self.client, message)):
            for user in message.mentions:
                self.cursor.execute('SELECT message FROM afk_users WHERE user_id = ?', (user.id,))
                result = self.cursor.fetchone()
                if result:
                    mentioned_afk_embed = discord.Embed(
                        description=f"> {user.mention} is currently AFK, with the status: **{result[0]}**",
                        color=discord.Color.blue()
                    )
                    await message.channel.send(embed=mentioned_afk_embed)

            self.cursor.execute('SELECT message FROM afk_users WHERE user_id = ?', (message.author.id,))
            result = self.cursor.fetchone()
            if result:
                remove_afk_embed = discord.Embed(
                    description=f"> :wave:{message.author.mention} is no longer AFK. Welcome back!",
                    color=0xCCCCCC
                )

                await message.channel.send(embed=remove_afk_embed)
                self.cursor.execute('DELETE FROM afk_users WHERE user_id = ?', (message.author.id,))
                self.connection.commit()

async def setup(client):
    await client.add_cog(afk(client))