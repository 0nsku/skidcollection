import discord
from discord.ext.commands import command, Cog
from discord.ext import commands
import requests, os, aiohttp
import datetime
from datetime import datetime, timezone


class misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    def read_lastfm_data():
        lastfm_data = {}
        with open("lastfm.txt", "r") as file:
            for line in file:
                user_id, lastfm_user = line.strip().split(",")
                lastfm_data[int(user_id)] = lastfm_user
        return lastfm_data

def write_lastfm_data(self, lastfm_data):
    with open("lastfm.txt", "w") as file:
        for user_id, lastfm_user in lastfm_data.items():
            file.write(f"{user_id},{lastfm_user}\n")

    @command(aliases=['ss'])
    async def screenshot(self, ctx, url: str = None):
        if not url:
            await ctx.send("Please provide a URL.")
            return

        key = '9be0f4'
        endpoint = 'https://api.screenshotmachine.com'
        params = {
            'key': key,
            'url': url,
            'dimension': '1024xfull',
            'format': 'png',
            'cacheLimit': '0',
            'timeout': '200'
        }
        screenshot_filename = 'betray.png'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params) as response:
                    if response.status != 200:
                        await ctx.send(embed=discord.Embed(title="", description=f"Failed to take a screenshot: {response.status}", color=0x2b2d31))
                        return

                    data = await response.read()
                    with open(screenshot_filename, 'wb') as f:
                        f.write(data)
  
                    file = discord.File(screenshot_filename)
                    embed = discord.Embed(title="", description=f"Screenshot of {url}", color=0x2b2d31)
                    embed.set_image(url=f"attachment://{screenshot_filename}")
                    await ctx.send(embed=embed, file=file)
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="", description=f"An error occurred: {e}", color=0x2b2d31))
        finally:
            if os.path.exists(screenshot_filename):
                os.remove(screenshot_filename)

    @command(aliases=['check'])
    async def vanitycheck(ctx: commands.Context, *, vanity: str = None):
        invite = f'https://discord.com/api/v9/invites/{vanity}'
        response = requests.get(invite)
        if response.status_code == 404:
            embed = discord.Embed(
                title="Vanity Check",
                description=f"> **{vanity}** is not taken",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
        elif response.status_code == 200:
            embed = discord.Embed(
                title="Vanity Check",
                description=f"> **{vanity}** is taken",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Vanity Check",
                description=f"> I could not fetch the availability for **{vanity}**",
                color=0x2b2d31       
            )
            await ctx.send(embed=embed)
        
    @command()
    async def translate(ctx, *, message: str = None): 
        try:
            translator = Translator()
            translated_message = translator.translate(message, dest='en')
            embed = discord.Embed(
                title="Translation",
                description=f"> Translated - {translated_message.text}",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")
        
    @command()
    async def calc(ctx, *, expression: str = None):
        try:
            result = eval(expression)
            embed = discord.Embed(
                title="",
                color=0x2b2d31,
                description=f"> *Answer -** {result}"
        )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                color=0x2b2d31,
                description=f"> **Error:** thats not a calcaulation"
            )
            await ctx.send(embed=embed)
        
    @command(aliases=['eth'])
    async def getethbal(ctx, ethaddress: str = None):
        if len(ethaddress) != 42:
            embed = discord.Embed(description="> The provided ETH address isn't valid", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        response = requests.get(f'https://api.blockcypher.com/v1/eth/main/addrs/{ethaddress}/balance')

        if response.status_code != 200:
            if response.status_code == 400:
                embed = discord.Embed(description="> Invalid ETH Address", color=0x2b2d31)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"> Failed to retrieve balance. Error {response.status_code}. Please try again later", color=0x2b2d31)
                await ctx.send(embed=embed)
            return

        data = response.json()
        balance = int(data['balance']) / 10 ** 18
        total_received = int(data['total_received']) / 10 ** 18
        unconfirmed_balance = int(data['unconfirmed_balance']) / 10 ** 18

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')

        if cg_response.status_code != 200:
            embed = discord.Embed(description=f"> Failed to retrieve the current price of ETH. Error {cg_response.status_code}. Please try again later", color=0x2b2d31)       
        await ctx.send(embed=embed)
        return

        usd_price = cg_response.json()['ethereum']['usd']
        usd_balance = balance * usd_price
        usd_total_received = total_received * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price

        embed = discord.Embed(title="", description=f"ETH Address: `{ethaddress}`", color=0x2b2d31)
        embed.add_field(name="Current ETH", value=f"${usd_balance:.2f} USD")
        embed.add_field(name="Total ETH Received", value=f"${usd_total_received:.2f} USD")
        embed.add_field(name="Unconfirmed ETH", value=f"${usd_unconfirmed_balance:.2f} USD")
    
        wallet_button = discord.ui.Button(style=discord.ButtonStyle.link, label="View Wallet", url=f"https://etherscan.io/address/{ethaddress}")

        view = discord.ui.View()
        view.add_item(wallet_button)

        await ctx.send(embed=embed, view=view)


    @command(aliases=['btc'])
    async def getbtcbal(self, ctx, btcaddress: str = None):
        if len(btcaddress) not in [34, 43, 42]:
            embed = discord.Embed(description="> The provided BTC address isn't valid", color=0x2b2d31)
            await ctx.send(embed=embed)
            return
        
        response = requests.get(f'https://api.blockcypher.com/v1/btc/main/addrs/{btcaddress}/balance')

        if response.status_code != 200:
            if response.status_code == 400:
                embed = discord.Embed(description="> Invalid BTC Address", color=0x2b2d31)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"> Failed to retrieve balance. Error {response.status_code}. Please try again later", color=0x2b2d31)
                await ctx.send(embed=embed)
            return

        data = response.json()
        balance = data['balance'] / 10 ** 8
        total_received = data['total_received'] / 10 ** 8
        unconfirmed_balance = data['unconfirmed_balance'] / 10 ** 8

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')

        if cg_response.status_code != 200:
            embed = discord.Embed(description=f"> Failed to retrieve the current price of BTC. Error {cg_response.status_code}. Please try again later", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        usd_price = cg_response.json()['bitcoin']['usd']
        usd_balance = balance * usd_price
        usd_total_received = total_received * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price

        embed = discord.Embed(title="", description=f"BTC Address: `{btcaddress}`", color=0x2b2d31)
        embed.add_field(name="Current BTC", value=f"${usd_balance:.2f} USD")
        embed.add_field(name="Total BTC Received", value=f"${usd_total_received:.2f} USD")
        embed.add_field(name="Unconfirmed BTC", value=f"${usd_unconfirmed_balance:.2f} USD")
    
        wallet_button = discord.ui.Button(style=discord.ButtonStyle.link, label="View Wallet", url=f"https://www.blockchain.com/btc/address/{btcaddress}")

        view = discord.ui.View()
        view.add_item(wallet_button)

        await ctx.send(embed=embed, view=view)

    @command(aliases=['ltc'])
    async def getltcbal(self, ctx, ltcaddress: str = None):
        if len(ltcaddress) not in [34, 43]:
            embed = discord.Embed(description="> The provided LTC address isn't valid", color=0x2b2d31)
            await ctx.send(embed=embed)
            return            

        response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

        if response.status_code != 200:
            if response.status_code == 400:
                embed = discord.Embed(description="> Invalid LTC address", color=0x2b2d31)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"> Failed to retrieve balance. Error {response.status_code}. Please try again later", color=0x2b2d31)
                await ctx.send(embed=embed)
            return

        data = response.json()
        balance = data['balance'] / 10 ** 8
        total_balance = data['total_received'] / 10 ** 8
        unconfirmed_balance = data['unconfirmed_balance'] / 10 ** 8

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

        if cg_response.status_code != 200:
            embed = discord.Embed(description=f"> Failed to retrieve the current price of LTC. Error {cg_response.status_code}. Please try again later", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        usd_price = cg_response.json()['litecoin']['usd']
        usd_balance = balance * usd_price
        usd_total_balance = total_balance * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price

        embed = discord.Embed(title="", description=f"LTC Address: `{ltcaddress}`", color=0x2b2d31)
        embed.add_field(name="Current LTC", value=f"${usd_balance:.2f} USD")
        embed.add_field(name="Total LTC Received", value=f"${usd_total_balance:.2f} USD")
        embed.add_field(name="Unconfirmed LTC", value=f"${usd_unconfirmed_balance:.2f} USD")
    
        wallet_button = discord.ui.Button(style=discord.ButtonStyle.link, label="View Wallet", url=f"https://blockchair.com/litecoin/address/{ltcaddress}")

        view = discord.ui.View()
        view.add_item(wallet_button)

        await ctx.send(embed=embed, view=view)


    @command(aliases=["firstmsg"])
    async def firstmessage(self, ctx):
        try:
            async for message in ctx.channel.history(limit=1, oldest_first=True):
                break
            embed = discord.Embed(title="", description=message.jump_url, color=0x2b2d31)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="", description=f"> An error occurred: {e}", color=0x2b2d31)
        await ctx.send(embed=embed)

    @command()
    async def weather(self, ctx, *, location: str = None):
        api_key = "8a6da4142ac1e58adc9e46523a302b95"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    
        response = requests.get(base_url)
        data = response.json()
    
        if data["cod"] != "404":
            weather_description = data['weather'][0]['description'].capitalize()
            temperature = round(data['main']['temp'] - 273.15, 2) 
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
        
            embed = discord.Embed(title=f"Weather in {location}", color=0x2b2d31)
            embed.add_field(name="Sky Weather", value=weather_description, inline=False)
            embed.add_field(name="Temperature (C)", value=f"{temperature}°C", inline=True)
            embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
            embed.add_field(name="Wind Speed", value=f"{wind_speed} m/s", inline=True)
          
            await ctx.send(embed=embed)
        else:
            await ctx.send("> **City not found**. Please try again.")

    @command()
    async def github(ctx, username: str = None):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        user_data = response.json()
    
        repos_url = user_data['repos_url']
        repos_response = requests.get(repos_url)
        repos_data = repos_response.json()
    
        total_stars = sum(repo['stargazers_count'] for repo in repos_data)
    
        embed = discord.Embed(title=f"GitHub User - **{username}**", color=0x2b2d31)
        embed.set_thumbnail(url=user_data['avatar_url'])
        embed.add_field(name="Info", value=f"Followers - **{user_data['followers']}**\nFollowing - **{user_data['following']}**\nBio - **{user_data['bio']}**\n\n", inline=True)
        embed.add_field(name="Repos", value=f"Public Repos - **{user_data['public_repos']}**\nStars - **{total_stars}**", inline=True)
        embed.add_field(name="Extra Info", value=f"Created - **{user_data['created_at']}**", inline=False)
        profile_button = discord.ui.Button(style=discord.ButtonStyle.link, label="Profile", url=f"https://github.com/{username}")
        view = discord.ui.View()
        view.add_item(profile_button)
    
        await ctx.send(embed=embed, view=view)

    @command()
    async def spotify(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        spotify_activity = None
        for activity in user.activities:
            if isinstance(activity, discord.Spotify):
                spotify_activity = activity
                break
        if spotify_activity is None:
            embed = discord.Embed(title=f"{user.display_name} is not listening to a song.", color=0x2b2d31)
            await ctx.send(embed=embed)
        else:
            song_link = f"[{spotify_activity.title}]({spotify_activity.track_url})"
            embed = discord.Embed(title=f"{user.display_name} is listening to...", color=0x2b2d31)
            embed.add_field(name="Song", value=song_link)
            embed.add_field(name="Artist", value=spotify_activity.artist)
            embed.set_thumbnail(url=spotify_activity.album_cover_url)
            button = discord.ui.Button(style=discord.ButtonStyle.link, label="Listen Along", url=spotify_activity.track_url)
            view = discord.ui.View()
            view.add_item(button)
            await ctx.send(embed=embed, view=view)
       

    @command()
    async def fmlink(ctx, lastfm_user):
        lastfm_data = self.read_lastfm_data()
        lastfm_data[ctx.author.id] = lastfm_user
        self.write_lastfm_data(lastfm_data)
        embed = discord.Embed(
            description="**linking account...**",
            color=0x2b2d31
        )
        message = await ctx.send(embed=embed)
        await discord.utils.sleep_until(message.created_at + datetime.timedelta(seconds=3))
        embed.description = f"**connected** Last.fm user **'{lastfm_user}'** to {ctx.author.mention}."
        await message.edit(embed=embed)



    @command()
    async def fm(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        lastfm_data = self.read_lastfm_data()
        if user.id not in lastfm_data:
            embed = discord.Embed(
                title="Last.fm",
                description=f"{ctx.author.mention}, your account is not connected. Use `$fmlink` to link your Last.fm account.",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
            return
        lastfm_user = lastfm_data[user.id]
        API_KEY = '7a2036ce1b9a072c9dcb07bc76023af2'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={lastfm_user}&api_key={API_KEY}&format=json') as resp:
                data = await resp.json()
        if 'recenttracks' in data:
            tracks = data['recenttracks']['track']
            if tracks:
                track = tracks[0]
                artist = track.get('artist', {}).get('#text', 'Unknown Artist')
                track_name = track.get('name', 'Unknown Track')
                time = datetime.datetime.now().strftime('%H:%M')
                embed = discord.Embed(
                    title=f"{user}",
                    description=f"{user} is now listening to **[{track_name}](https://www.last.fm/user/{lastfm_user})**\n\nToday at {time}",
                    color=0x2b2d31
                )
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1212129989042896937/1220486132811432017/omnes-gif3.gif?ex=660f1d49&is=65fca849&hm=70f373d76767a9e3858379bc07e438aa0d975429193721503d19f4e9bb94a898&")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{user}",
                    description=f"{user.mention} is not listening to anything.",
                    color=0x2b2d31
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Last.fm",
                description=f"Last.fm user '**{lastfm_user}**' not found. Please relink with a valid username.",
                color=0x2b2d31
            )
            await ctx.send(embed=embed)
            
async def setup(bot):
    await bot.add_cog(misc(bot))