import discord
from discord.ext.commands import Cog
from discord.ext import commands
from gtts import gTTS
import io, requests, random
from discord import FFmpegPCMAudio
import os

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        cat_url = data[0]['url']
        embed = discord.Embed(title="", color=0x2b2d31)
        embed.set_image(url=cat_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        dog_url = data['message']
        embed = discord.Embed(title="", color=0x2b2d31)
        embed.set_image(url=dog_url)
        await ctx.send(embed=embed)
    
    @commands.group(invoke_without_command=True)
    async def tts(self, ctx):
        await ctx.send("Invalid usage of tts command. Usage: !tts <text>")

    @tts.command(name='channel', aliases=['ch'])
    async def tts_channel(self, ctx, *, message: str):
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.send("You are not in a voice channel.")
    
        user_channel = ctx.author.voice.channel
        voice_state = ctx.guild.voice_client

        if voice_state and voice_state.channel:
            if voice_state.channel.guild == user_channel.guild and voice_state.channel != user_channel:
                await voice_state.disconnect()
    
        if voice_state and voice_state.channel == user_channel:
            return await ctx.send("Bot is already in your voice channel.")

        await user_channel.connect()
    
        tts_data = await self.tts_bytes(message)
        tts_audio_filename = "tts_audio.mp3"
        with open(tts_audio_filename, 'wb') as f:
            f.write(tts_data.getvalue())
    
        tts_audio_source = discord.FFmpegPCMAudio(tts_audio_filename)
        ctx.voice_client.play(tts_audio_source, after=lambda e: print(f"Finished playing TTS audio: {e}"))
    
        os.remove(tts_audio_filename)

    async def tts_bytes(self, message):
        tts = gTTS(text=message, lang='en')
        tts_data = io.BytesIO()
        tts.write_to_fp(tts_data)
        tts_data.seek(0)
        return tts_data

    @commands.command()
    async def eightball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        response = random.choice(responses)
        embed = discord.Embed(description=f"{ctx.author.mention} {response}", color=0x2b2d31)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['wyr'])
    async def wouldyourather(self, ctx):
        questions = [
    "Would you rather have the ability to fly or be invisible?",
    "Would you rather never use the internet again or never watch TV again?",
    "Would you rather have a rewind button for your life or a pause button?",
    "Would you rather have a pet dragon or be a dragon?",
    "Would you rather have unlimited pizza or unlimited tacos?",
    "Would you rather always be 10 minutes late or always be 20 minutes early?",
    "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
    "Would you rather live in a world where it is always daytime or always nighttime?",
    "Would you rather have the ability to talk to animals or speak all foreign languages?",
    "Would you rather be able to teleport anywhere or be able to read minds?",
    "Would you rather have to sing everything you say or dance every time you move?",
    "Would you rather have a rewind button for your life or a fast forward button?",
    "Would you rather have everything you eat be too salty or not salty enough no matter how much salt you add?",
    "Would you rather have fingers for toes or toes for fingers?",
    "Would you rather always have to say everything on your mind or never speak again?",
    "Would you rather have a personal theme song that plays every time you enter a room or have a voice-activated spotlight follow you around?",
    "Would you rather have to eat a bowl of spiders or a bowl of worms?",
    "Would you rather be able to talk to animals but they can never understand you or be able to speak every language except your own?",
    "Would you rather have a flying car or a personal robot?",
    "Would you rather sneeze cheese or have your tears be made of hot sauce?",
    "Would you rather have a nose that glows red like Rudolph's whenever you're embarrassed or be followed by circus music everywhere you go?",
    "Would you rather have a unicorn horn or a squirrel tail?",
    "Would you rather have to communicate only through interpretive dance or never be able to communicate at all?",
    "Would you rather have hair that changes color with your emotions or tattoos that appear all over your body depicting what you did yesterday?",
    "Would you rather have to eat a bowl of bugs or a bowl of toenail clippings?",
    "Would you rather have to wear wet socks for the rest of your life or only be able to wash your hair once a year?",
    "Would you rather have a clown only you can see that follows you everywhere and just stands silently in a corner watching you without doing or saying anything or have a real-life stalker who dresses like the Easter Bunny and leaves you notes made of human teeth?",
    "Would you rather have to wear your clothes inside out every day or have all your clothes be two sizes too small?",
    "Would you rather be constantly followed by a ghost for the rest of your life or never be able to wear shoes again?",
    "Would you rather have to eat a spoonful of wasabi once a day or never be able to eat sweets again?",
    "Would you rather have to live in a house made of ice cream or a house made of candy?",
    "Would you rather have to wear a cape wherever you go for the rest of your life or have to wear an eyepatch?",
    "Would you rather have to fight a bear with only your hands or fight a swarm of bees with only a newspaper?",
    "Would you rather have to wear someone else's dirty underwear or use their toothbrush?",
    "Would you rather be able to talk to land animals, animals that fly, or animals that live under the water?",
    "Would you rather be able to control fire or water?",
    "Would you rather have a third eye or a third arm?",
    "Would you rather have to eat a tablespoon of salt or a tablespoon of cinnamon?",
    "Would you rather have to wear clown shoes every day or a clown wig?",
    "Would you rather be able to control the size of objects or their weight?",
    "Would you rather have to hop everywhere or crawl everywhere?",
    "Would you rather have a permanent smile or a permanent frown?",
    "Would you rather be able to fly but only three feet off the ground or be able to run faster than a car?",
    "Would you rather have to always wear a full suit of armor or a tutu?",
    "Would you rather be able to breathe underwater or talk to animals?",
    "Would you rather be able to turn invisible or be able to teleport?",
        ]
        question1, question2 = random.sample(questions, 2) 
        embed = discord.Embed(title="Would You Rather", color=0x2b2d31)
        embed.add_field(name="Option 1", value=f"**```{question1}```**", inline=False)
        embed.add_field(name="Option 2", value=f"**```{question2}```**", inline=False)
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:one_white:1220463576418877480>')
        await message.add_reaction('<:two_white:1220463609545621514>')

    @commands.command()
    async def roast(self, ctx, member: discord.Member):
        roasts = [
    "You're not pretty enough to be this dumb, {}.",
    "If I wanted to kill myself, I'd climb to your ego and jump to your IQ, {}.",
    "I'd agree with you, but then we'd both be wrong, {}.",
    "If brains were dynamite, you wouldn't have enough to blow your nose, {}.",
    "I'm not saying you're stupid, I'm just saying you have bad luck when thinking, {}.",
    "Your family tree must be a cactus because everyone on it is a prick, {}.",
    "It's a shame you can't Photoshop your personality, {}.",
    "If you were any more inbred, you'd be a sandwich, {}.",
    "I'd tell you to go to hell, but I work there and don't want to see you every day, {}.",
    "If ignorance is bliss, you must be the happiest person alive, {}.",
    "It's not a bald spot, it's a solar panel for a sex machine, {}.",
    "I don't know what makes you so stupid, but it really works, {}.",
    "You're not stupid; you just have bad luck thinking, {}.",
    "You have the right to remain silent because whatever you say will probably be stupid anyway, {}.",
    "Is your ass jealous of the amount of crap that comes out of your mouth, {}?",
    "I'd roast you, but my mom told me not to burn trash, {}.",
    "I'm not insulting you; I'm describing you, {}.",
    "You must have been born on a highway because that's where most accidents happen, {}.",
    "Your face is fine, but you'll have to put a bag over that personality, {}.",
    "You're the reason the average sperm count is declining, {}.",
    "I'm not saying I hate you, but I would unplug your life support to charge my phone, {}.",
    "Do you still love nature, despite what it did to you, {}?",
    "I'd like to see things from your perspective, but I can't seem to get my head that far up my ass, {}.",
    "You're not the dumbest person in the world, but you'd better hope they don't die, {}.",
    "You're the reason they invented double doors, {}!",
    "I hope your day is as pleasant as you are, {}.",
    "If I wanted a bitch, I'd have bought a dog, {}.",
    "You're not as bad as people say; you're worse, {}.",
    "It's not your fault you were born like that, but you could at least try to improve, {}.",
    "Your birth certificate is an apology letter from the condom factory, {}.",
    "I'd slap you, but I don't want to make your face look any better, {}.",
    "I'd call you a tool, but even they serve a purpose, {}.",
    "You're not the sharpest tool in the shed. Heck, you're not even a tool, {}.",
    "You're the human equivalent of a participation trophy, {}.",
    "I'd say you're dumb as a rock, but at least a rock has some uses, {}.",
    "I'd challenge you to a battle of wits, but I see you're unarmed, {}.",
    "I'd insult you, but I don't want to give you any more brain damage, {}.",
    "If I threw you into a river, you'd come out with a fish in your mouth and claim you were just swimming, {}.",
        ]
        roast_message = random.choice(roasts).format(member.mention)
        embed = discord.Embed(description=f'**{roast_message}**', color=0x2b2d31)
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What did one ocean say to the other ocean? Nothing, they just waved.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "I'm on a whiskey diet. I've lost three days already!",
    "I told my computer I needed a break and now it won't stop sending me vacation ads.",
    "What did the grape say when it got stepped on? Nothing, it just let out a little wine.",
    "Why don't some couples go to the gym? Because some relationships don't work out.",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "Why did the chicken join a band? Because it had the drumsticks!",
    "I'm trying to organize a hide and seek competition, but it's really hard to find good players.",
    "I'd tell you a joke about the construction industry, but I'm still working on it.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the bicycle fall over? Because it was two-tired!",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call a snowman with a six-pack? An abdominal snowman!",
    "Why don't skeletons fight each other? They don’t have the guts.",
    "Why did the coffee file a police report? It got mugged.",
    "What did one hat say to the other? You stay here, I'll go on ahead.",
    "What did the janitor say when he jumped out of the closet? Supplies!",
    "Why couldn't the leopard play hide and seek? Because he was always spotted!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What did one plate say to the other plate? Dinner's on me!",
    "What's orange and sounds like a parrot? A carrot!",
    "Why did the math book look sad? Because it had too many problems.",
    "I'm reading a book on the history of glue. I just can't seem to put it down!",
    "I used to be a baker, but I couldn't make enough dough.",
    "I'm writing a book on anti-gravity. It's going to be hard to put down!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What's brown and sticky? A stick!",
        ]
        embed = discord.Embed(description=random.choice(jokes), color=0x2b2d31)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(fun(bot))