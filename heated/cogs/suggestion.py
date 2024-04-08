import discord
from discord.ext import commands

class suggestion(commands.Cog):
    def __init__(self, client):
        self.client = client
            
            
    @commands.command(aliases=['suggestion'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion=None):
        suggestion_channel_id = 1216840905286357114
        suggestion_channel = self.client.get_channel(suggestion_channel_id)

        if suggestion is None:
            embed = discord.Embed(
                title='Suggestion',
                color=0xCCCCCC,
                description='<:rp:1197985417908191452> Suggestion a feature or anything that would be useful!'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}suggestion [suggestion]\n```',
                inline=False
            )
            embed.add_field(
                name='<:info:1214258260836749462> Example:',
                value=f'```\n{ctx.prefix}suggestion add an alias for kick\n```',
                inline=True
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\nsuggest\n```',
                inline=True
            )
            await ctx.send(embed=embed)
            return

        if suggestion_channel:
            formatted_suggestion = f"> {suggestion}"

            embed = discord.Embed(title='Suggestion', description=formatted_suggestion, color=0xCCCCCC)
            embed.set_footer(text=f"Suggestion sent by: {ctx.author.name}")

            suggestion_message = await suggestion_channel.send(embed=embed)

            await suggestion_message.add_reaction('<:true:1214258277391536158>')
            await suggestion_message.add_reaction('<:false:1214258281183453254>')

            success_embed = discord.Embed(title='<:true:1214258277391536158> Success', description='> Your suggestion has been submitted! Thanks for your input.', color=0x00ff00)
            await ctx.send(embed=success_embed)
        else:
            error_embed = discord.Embed(title='', description=f'> <:false:1214258281183453254> No channel found. Contact [davidosxo](https://discord.com/users/921148808551870484) or [support](https://discord.gg/heated)', color=0xff0000)
            await ctx.send(embed=error_embed)

async def setup(client):
    await client.add_cog(suggestion(client))