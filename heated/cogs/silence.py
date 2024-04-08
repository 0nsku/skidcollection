import discord
from discord.ext import commands
from discord import Embed
import sqlite3

class silence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("silence.db")
        self.cursor = self.conn.cursor()
        self.setup_db()

    def setup_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS silenced_users (
                              guild_id INTEGER,
                              user_id INTEGER,
                              PRIMARY KEY (guild_id, user_id)
                           )''')
        self.conn.commit()

    async def send_custom_embed(self, ctx, title, description, color=discord.Color.blue()):
        embed = Embed(title=title, description=description, color=color)
        await ctx.send(embed=embed)

    async def send_error_embed(self, ctx, error_message, color=discord.Color.red()):
        await self.send_custom_embed(ctx, "<:false:1214258281183453254> Fail", error_message, color=color)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def silence(self, ctx, member: discord.Member = None):
        if member is None:
                embed = discord.Embed(
                title='Silence',
                color=0xCCCCCC,
                description="Auto deletes messages from users when they're silenced."
            )
                embed.add_field(
                    name='<:cmds:1214258288326090773> Command Usage:',
                    value=f'```\n{ctx.prefix}silence [@user]\n```',
                    inline=False
                )
                embed.add_field(
                    name='<:info:1214258260836749462> Example:',
                    value=f'```\n{ctx.prefix}silence @rip.rive \n```',
                    inline=True
                )
                embed.add_field(
                    name='<:wait:1214258202754154617> Permissions:',
                    value=f'```\nManage Messages\n```',
                    inline=True
            )
                await ctx.send(embed=embed)
                return
            

        if ctx.author.id == member.id:
            await self.send_error_embed(ctx, f"> {ctx.author.mention} you cannot silence yourself.")
            return
            
        if ctx.author.top_role <= member.top_role:
            await self.send_error_embed(ctx, f"> {ctx.author.mention} You cannot silence someone with a higher role.")
            return
            
            guild_id = ctx.guild.id
            user_id = member.id
            
            self.cursor.execute('SELECT * FROM silenced_users WHERE guild_id=? AND user_id=?', (guild_id, user_id))
        if not self.cursor.fetchone():
            guild_name = ctx.guild.name
            await self.send_custom_embed(ctx, "<:true:1214258277391536158> Success", f"> {member.mention} has been silenced by {ctx.author.mention}.", color=discord.Color.green())
            self.cursor.execute('INSERT INTO silenced_users (guild_id, user_id) VALUES (?, ?)', (guild_id, user_id))
            self.conn.commit()
        else:
            await self.send_error_embed(ctx, f"> {member.mention} is already silenced.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unsilence(self, ctx, member: discord.Member = None):
        if member is None:
                embed = discord.Embed(
                title='Unsilence',
                color=0xCCCCCC,
                description="Removes silence."
            )
                embed.add_field(
                    name='<:cmds:1214258288326090773> Command Usage:',
                    value=f'```\n{ctx.prefix}unsilence [@user]\n```',
                    inline=False
                )
                embed.add_field(
                    name='<:info:1214258260836749462> Example:',
                    value=f'```\n{ctx.prefix}unsilence @rip.rive \n```',
                    inline=True
                )
                embed.add_field(
                    name='<:wait:1214258202754154617> Permissions:',
                    value=f'```\nManage Messages\n```',
                    inline=True
            )
                await ctx.send(embed=embed)
                return

        if ctx.author.id == member.id:
            await self.send_error_embed(ctx, f"> {ctx.member.mention} you cannot unsilence yourself.")
            return

        if ctx.author.top_role <= member.top_role:
            await self.send_error_embed(ctx, f"> {ctx.author.mention} you cannot unsilence someone with a higher role.")
            return

        guild_id = ctx.guild.id
        user_id = member.id

        self.cursor.execute('SELECT * FROM silenced_users WHERE guild_id=? AND user_id=?', (guild_id, user_id))
        if self.cursor.fetchone():
            guild_name = ctx.guild.name
            await self.send_custom_embed(ctx, "<:true:1214258277391536158> Success", f"> {member.mention} has been unsilenced by {ctx.author.mention}.", color=discord.Color.green())
            self.cursor.execute('DELETE FROM silenced_users WHERE guild_id=? AND user_id=?', (guild_id, user_id))
            self.conn.commit()
        else:
            await self.send_error_embed(ctx, f"> {member.mention} is not silenced.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        user_id = message.author.id

        self.cursor.execute('SELECT * FROM silenced_users WHERE guild_id=? AND user_id=?', (guild_id, user_id))
        if self.cursor.fetchone():
            await message.delete()

async def setup(client):
    await client.add_cog(silence(client))