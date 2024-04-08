import discord
from discord.ext import commands
import random

class ball(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ask', '8ball'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def eight_ball(self, ctx, *, question=None):
        if not question:
            embed = discord.Embed(
                title='8Ball',
                color=0xCCCCCC,
                description='Ask a question.'
            )
            embed.add_field(
                name='<:cmds:1214258288326090773> Command Usage:',
                value=f'```\n{ctx.prefix}8ball [question]\n```',
                inline=False
            )
            embed.add_field(
                name='<:misc:1215001481338556496> Aliases:',
                value=f'```\nask, eight_ball\n```',
                inline=False
            )
            await ctx.send(embed=embed)
            return

        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes – definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Don’t count on it.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]

        response = random.choice(responses)

        embed = discord.Embed(title='', color=0xCCCCCC)
        embed.add_field(name='Question', value=question, inline=False)
        embed.add_field(name='Answer', value=response, inline=False)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(ball(client))