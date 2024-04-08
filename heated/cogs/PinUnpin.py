import discord
from discord.ext import commands



class PinUnpin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, message_id: int):
        try:
            message = await ctx.channel.fetch_message(message_id)
            await message.pin()
            embed = discord.Embed(title = "<:true:1214258277391536158> Success", description= f"> Message has been pinned.", color = discord.Color.green())
            await ctx.send(embed = embed)
        except discord.NotFound:
            embed = discord.Embed(title = "<:false:1214258281183453254> Fail", description= f"> Message not found.", color = discord.Color.red())
            await ctx.send(embed = embed)
        except discord.Forbidden:
            embed = discord.Embed(title = "<:false:1214258281183453254> Fail", description= f"> I don't have the correct permissions to unpin this message.", color = discord.Color.red())
            await ctx.send(embed = embed)
        except discord.HTTPException:
            embed = discord.Embed(title = "<:false:1214258281183453254> Fail", description= f"> Failed to unpin the message.", color = discord.Color.red())
            await ctx.send(embed = embed)

    @commands.command(name="unpin")
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, message_id: int):
        try:
            message = await ctx.channel.fetch_message(message_id)
            await message.unpin()
            embed = discord.Embed(title = "<:true:1214258277391536158> Success", description= f"> Message has been unpinned.", color = discord.Color.green())
            await ctx.reply(embed = embed)
        except discord.NotFound:
            embed = discord.Embed(title = "<:false:1214258281183453254> Fail", description= f"> Message not found.", color = discord.Color.red())
            await ctx.reply(embed = embed)
        except discord.Forbidden:
            embed = discord.Embed(title = "<:false:1214258281183453254> Fail", description= f"> I don't have the correct permissions to unpin this message.", color = discord.Color.red())
            await ctx.reply(embed = embed)
        except discord.HTTPException:
            embed = discord.Embed(title = "<:false:1214258281183453254> Fail", description= f"> Failed to unpin the message.", color = discord.Color.red())
            await ctx.reply(embed = embed)
            
    @pin.error
    async def cmdname_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="> :false: Missing `perms` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @unpin.error
    async def cmdname_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="> :false: Missing `perms` permission(s).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)         

async def setup(client):
    await client.add_cog(PinUnpin(client))
