import discord, random
import aiohttp
import os
import datetime
from discord.ext import commands
from discord.ui import View, Button
import json
from datetime import datetime, timedelta
import psutil
from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = [ 
            "Kill that urge to be chosen . CHOOSE URSELF . ",
            "I miss me imma come back lol .",
            "Everyday is an opportunity to fix some shit u messed up . Mess ups are a moment, quitting is forever . Be kind to urself ",
            "Talking less being more .",
            "Anger depletes the body.",
            "Sometimes u gotta not give a fuck, trust God n just do you.",
            "Ur fear looking stupid is holding u back.",
            "Aboslutely no more going w the flow. Create my own flow or bust.",
            "I jus be shakin ass through the pain . ",
            "God bless even the bitches that dont fuck w me 🙏♥",
            "One thing about me .. imma do what I want . For certain. at all times .",
            "W all due respect . Sometimes no respct is due",
            "Sometimes asking questions is disrespectful to ur own intuition. You know wtf goin on. Now act accordingly.",
            "SMOKE A BLUNT, EXFOLIATE, REPLACE HIM, REPEAT.",
            "Quiet is good.",
            "Wanting to fit in and be liked is an **INFECTIONOUS** DISEASE ... natural tho, like chickenpox.",
            "Focus . Focus . Focus . Focus . Focus . Focus focus focus focus focus . Fuck it all . Just focus .",
            "Stop letting ppl try u on .",
            "Very important to surround urself w ppl that see u fully.",
            "Some people gon hate chu for no reason. N u gon shine regardless ..",
            "Stay soft, life is hard.",
            "Imma be misunderstood til I die, might aswell have a good time",
            "Calm down n stay the course.",
            "Good day in my mind, safe to take a step out, get some air now, let your edge out.",
            "All the while, I'll await my armored fate with a smile.",
            "Gotta get right, tryna free my mind before the end of the world.",
            "You a wild one, and I'm wadin' in you like it's cool water.",
            "Why is it so hard to accept the party is over?",
            "Bring the gin, got the juice, bring the sin, got that too.",
            "Somebody get the tacos, somebody spark a blunt, let's start the Narcos off at episode one.",
            "You like 9 to 5, I'm the weekend.",
            "Gettin' all in your love, fallin' all over love.",
            "I gotta say I'm in the mood for a little bit more of that.",
            "How you ain't say you was movin' forward? Honesty hurts when you're gettin' older.",
            "20 something, all alone still, not a thing in my name.",
            "Stuck in them 20 somethings, stuck in them 20 somethings.",
            "And if it's an illusion, I don't wanna wake up. I'm gonna hang on to it.",
            "Promise I won't cry over spilled milk.",
            "Acting like we wasn't more than a summer fling, I said farewell, you took it well.",
            "Why you bother me when you know you don't want me?",
            "I'm never going back, never going back, you can't make me.",
            "I've paid enough of petty dues, I've heard enough of sh*tty news.",
            "Can't beat ‘em, just join the party.",
            "All that I've got, pieces and pages.",
            "Got a shift ay 10 a.m., got a dip at 10 p.m., gotta get that cash.",
            "It made me feel good for temporary love, you was a temporary lover.",
            "I could be your supermodel if you believe, if you see it in me.",
            "But I need you, I need you, I need you.",
            "Why I can't stay alone just by myself? Wish I was comfortable just with myself.",
            "Maybe I should kill my inhibition, maybe I'll perfect in a new dimension.",
            "Down for the ride, down for the ride, you could take me anywhere.",
            "Need you for the old me, need you for my sanity, need you to remind me where I come from.",
            "Love me even if it rain, love me even if it pain you.",
            "I make bad decisions frequently. They're fun.",
            "It starts with trusting yourself, even if people are telling you you're too young to trust yourself.",
            "I don't have any control over what actually happens except for that I have full control over my will for myself, my intention, and why I'm there. That's all that matters.",
            "I want to excel at something, to follow through, to not be afraid.",
            "Don't get discouraged with your skin when it doesn't do what you want it to do... Give it some time. That's the only way to get to know yourself.",
            "I learned everything the hard way - like, literally, everything. I know that God does that to people that he has lessons for. I just wish that I had learned less extreme lessons.",
            "I wasn't popular in high school; I had no friends.",
            "I got a lot of crap for being named SZA but not being affiliated with Wu-Tang, and being a girl.",
            "In one way, I want to heal people.",
            "I worry so much. Like, 'Damn, how can I be excellent?' But it's a journey.",
            "You can take care of your body, and it will low-key show you respect in turn.",
            "I feel good being a black woman; I've always felt good.",
            "Control is not real, and I'm really understanding that every day. It's about the acceptance of relinquishing control that makes it powerful for you.",
            

        ]

    # sza quotes
    @commands.command(name="szaquote")
    async def szaquote(self, ctx):
        random_quote = random.choice(self.quotes)

        color = discord.Color(random.randint(0xAAAAAA, 0xEEEEEE))

        embed = discord.Embed(description=f"> {random_quote}", color=self.bot.color)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Misc(bot))   