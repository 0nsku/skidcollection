import discord
from discord.ext import commands
import sqlite3

class fn(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.connection = sqlite3.connect("fn.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS forced_nicknames (user_id INTEGER PRIMARY KEY, nickname TEXT)")
        self.connection.commit()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild is None:
            return
        forced_nickname = self.get_forced_nickname(after.id)
        if forced_nickname is not None and after.nick != forced_nickname:
            try:
                await after.edit(nick=forced_nickname)
            except discord.Forbidden:
                print(f"Bot doesn't have permission to change nickname for {after.display_name}")

    def get_forced_nickname(self, user_id):
        self.cursor.execute("SELECT nickname FROM forced_nicknames WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    @commands.command(aliases=['fn'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def forcenick(self, ctx, member: discord.Member = None, *, forced_nickname = None):
        if member is None or forced_nickname is None:
            embed = discord.Embed(
                title='',
                description='`;forcenick [@user] [nickname]`',
                color=0xCCCCCC
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title='',
                description='> <:false:1214258281183453254> You cannot force a nickname on yourself.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.edit(nick=forced_nickname)
            self.cursor.execute("INSERT OR REPLACE INTO forced_nicknames VALUES (?, ?)", (member.id, forced_nickname))
            self.connection.commit()
            embed = discord.Embed(
                title='<:true:1214258277391536158> Success',
                description=f"Set force nickname for {member.mention} to `{forced_nickname}`!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='',
                description=f"> <:false:1214258281183453254> Unable to set forced nickname for {member.mention}. Make sure my role is above theirs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='',
                description=f"> <:false:1214258281183453254> An error occurred: {e} Contact [davidosxo](https://discord.com/users/1168186952772747364) or [support](https://discord.gg/heated)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['unfn'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def unforcenick(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title='',
                description='`;unforcenick [@user]`',
                color=0xCCCCCC
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title='',
                description='> <:false:1214258281183453254> You cannot unforce your own nickname.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            self.cursor.execute("DELETE FROM forced_nicknames WHERE user_id=?", (member.id,))
            self.connection.commit()
            await member.edit(nick=None)
            embed = discord.Embed(
                title='<:true:1214258277391536158> Success',
                description=f'> Removed force nickname for {member.mention}!',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='',
                description=f"> <:false:1214258281183453254> Unable to remove forced nickname for {member.mention}. Make sure my role is above theirs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='',
                description=f"> <:false:1214258281183453254> An error occurred: {e} Contact [davidosxo](https://discord.com/users/1168186952772747364) or [support](https://discord.gg/heated)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
            
async def setup(client):
    await client.add_cog(fn(client))