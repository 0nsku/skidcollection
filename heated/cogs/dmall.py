import discord
from discord.ext import commands

class dmall(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='dmtest')
    @commands.is_owner()
    async def dm_test(self, ctx):

        message_embed = discord.Embed(
            title="Hi! <a:B_mymelodykiss:1204320256202379265>",
            description="<:rp:1197985417908191452> Are you looking for a new and untested discord bot?",
            color=0xCCCCCC
        )
        message_embed.add_field(name='If not', value='You can just ignore this message.', inline=True)
        message_embed.add_field(name='If yes', value='I\'m the perfect bot for that! \n join discord.gg/heated and ping the owner that you\'re trying to find bugs! \n I\'ll give you something in return! *If I\'m gonna be able to* \n and I\'m also looking for devs! ', inline=True)
        message_embed.add_field(name='If you don\'t wanna hunt bugs', value='then at least please add the bot and use it if you\'re comfortable. \n That\'s all bye! <a:p_:1201616794922786957>', inline=True)

        try:
            await ctx.author.send(embed=message_embed)
            await ctx.send("Message sent to you!")
        except discord.Forbidden:
            await ctx.send("Unable to send a direct message. Please check your privacy settings.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name='dmall')
    @commands.is_owner()
    async def dm_all(self, ctx):
        message_embed = discord.Embed(
            title="Hi! <a:B_mymelodykiss:1204320256202379265>",
            description="<:rp:1197985417908191452> Are you looking for a new and untested discord bot?",
            color=0xCCCCCC
        )
        message_embed.add_field(name='If not', value='You can just ignore this message.', inline=True)
        message_embed.add_field(name='If yes', value='I\'m the perfect bot for that! \n join discord.gg/heated and ping the owner that you\'re trying to find bugs! \n I\'ll give you something in return! *If I\'m gonna be able to* \n and I\'m also looking for devs! ', inline=True)
        message_embed.add_field(name='If you don\'t wanna hunt bugs', value='then at least please add the bot and use it if you\'re comfortable. \n That\'s all bye! <a:p_:1201616794922786957>', inline=True)
        
        for guild in self.client.guilds:
            for member in guild.members:
                try:
                    await member.send(embed=message_embed)
                    print(f"DM sent to {member.display_name} in {guild.name}")
                except discord.Forbidden:
                    print(f"Unable to send DM to {member.display_name} in {guild.name}")
                except Exception as e:
                    print(f"An error occurred: {e}")

        await ctx.send("done")
        print("Broadcast DMs sent to all members in all guilds I'm done")



async def setup(client):
    await client.add_cog(dmall(client))