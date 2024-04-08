import discord, random
import aiohttp
import os
import datetime
from discord.ext import commands, tasks
from discord.ui import View, Button
import json
from datetime import datetime, timedelta
import psutil
from discord.ext.commands import Cog, command, Context, AutoShardedBot as Bot, hybrid_command, hybrid_group, group, check
import contextlib
import requests

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.btc_notifier.start()
    
    # conversions 
        
    @commands.command(
    usage="<cm> <kg> <gender (boy/girl/female/male/m/f)>",
    description="calculate the body mass index of someone using the required information"
)
    async def bmi(self, ctx, cm: float, kg: float, gender: str):

        if gender.lower() == 'other':
            await ctx.send_warning("Your BMI is **133.33**, which means you are **obese**")
            return

        if gender.lower() not in ['boy', 'girl', 'male', 'female', 'm', 'f']:
            embed = discord.Embed(
                description="> They is only **two** __scientific__ genders, `male` and `female`",
                color=self.bot.color
            )
            await ctx.send(embed=embed)
            return

        if gender.lower() in ['boy', 'girl']:
            gender = 'male' if gender.lower() == 'boy' else 'female'

        if gender.lower() in ['male', 'female']:
            gender = gender[0]  

        bmi = kg / ((cm / 100) ** 2)
        category = ""
        if gender.lower() == 'm':
            category = "underweight" if bmi < 20.7 else "healthy" if 20.7 <= bmi < 26.4 else "overweight" if 26.4 <= bmi < 27.8 else "obese"
        else:
            category = "underweight" if bmi < 19.1 else "healthy" if 19.1 <= bmi < 25.8 else "overweight" if 25.8 <= bmi < 27.3 else "obese"

        description = f"> Your BMI is **{bmi:.2f}**, which means you are **{category}**" if gender.lower() != 'other' else "Please provide a valid gender."

        embed = discord.Embed(
            description=description,
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, name="cm")
    async def cmgroup(self, ctx):
        await ctx.send_help(ctx.command)

    @cmgroup.command(description="converts inches to centimeters", usage="<inch>")
    async def inch(self, ctx, inch: float):
        if inch < 0:
            await ctx.send_warning("Please provide a positive value for inches.")
            return

        cm = inch * 2.54
        await ctx.send(embed = discord.Embed(
            description=f"> **{inch}** inches is equal to **{cm:.2f}** centimeters",
            color=self.bot.color
        ))

    @cmgroup.command(description="converts feet to centimeters", usage="<ft>")
    async def feet(self, ctx, ft: float):
        """Converts feet to centimeters"""
        cm = ft * 30.48
        await ctx.send(embed = discord.Embed(
            description=f"> **{ft}** feet is equal to **{cm:.2f}** centimeters",
            color=self.bot.color
        ))

    @commands.group(invoke_without_command=True, name="inch")
    async def inchgroup(self, ctx):
        await ctx.send_help(ctx.command)

    @inchgroup.command(description=f"converts centimeters to inches", usage="<cm>")
    async def cm(self, ctx, cm: float):
        inch = cm * 0.393701
        await ctx.send(embed = discord.Embed(
            description=f"> **{cm}** centimeters is equal to **{inch:.2f}** inches",
            color=self.bot.color
        ))

    @inchgroup.command(description="converts feet to inches", usage="<ft>")
    async def feet(self, ctx, ft: float):
        inch = ft * 12
        await ctx.send(embed = discord.Embed(
            description=f"> **{ft}** feet is equal to **{inch:.2f}** inches",
            color=self.bot.color
        ))

    @commands.group(invoke_without_command=True, name="feet", aliases=["ft"])
    async def feetgroup(self, ctx):
        await ctx.send_help(ctx.command)

    @feetgroup.command(description="converts centimeters to feet", usage="<cm>")
    async def cm(self, ctx, cm: float):
        feet = cm * 0.0328084
        await ctx.send(embed = discord.Embed(
            description=f"> **{cm}** centimeters is equal to **{feet:.2f}** feet",
            color=self.bot.color
        ))

    @feetgroup.command(description="converts inches to feet", usage="<inch>")
    async def inch(self, ctx, inch: float):
        feet = inch / 12
        await ctx.send(embed = discord.Embed(
            description=f"> **{inch}** inches is equal to **{feet:.2f}** feet",
            color=self.bot.color
        ))

    @commands.group(invoke_without_command=True, name="kg")
    async def kggroup(self, ctx):
        await ctx.send_help(ctx.command)

    @kggroup.command(description="converts pounds to kilograms", usage="<lbs>")
    async def lbs(self, ctx, lbs: float):
        kg = lbs * 0.453592
        await ctx.send(embed=discord.Embed(
            description=f"> **{lbs}** pounds is equal to **{kg:.2f}** kilograms",
            color=self.bot.color
        ))

    @kggroup.command(description="converts stone to kilograms", usage="<stone>")
    async def stone(self, ctx, stone: float):
        kg = stone * 6.35029
        await ctx.send(embed=discord.Embed(
            description=f"> **{stone}** stone is equal to **{kg:.2f}** kilograms",
            color=self.bot.color
        ))

    @kggroup.command(description="converts ounces to kilograms", usage="<ounce>")
    async def ounce(self, ctx, ounce: float):
        kg = ounce * 0.0283495
        await ctx.send(embed=discord.Embed(
            description=f"> **{ounce}** ounces is equal to **{kg:.2f}** kilograms",
            color=self.bot.color
    ))
        
    @commands.group(invoke_without_command=True)
    async def lbsgroup(self, ctx):
        await ctx.send_help(ctx.command)

    @lbsgroup.command(description="converts kilograms to pounds", usage="<kg>")
    async def kg(self, ctx, kg: float):
        pounds = kg * 2.20462
        await ctx.send(embed=discord.Embed(
            description=f"> **{kg}** kilograms is equal to **{pounds:.2f}** pounds",
            color=self.bot.color
        ))

    @lbsgroup.command(description="converts stone to pounds", usage="<stone>")
    async def stone(self, ctx, stone: float):
        pounds = stone * 14
        await ctx.send(embed=discord.Embed(
            description=f"> **{stone}** stone is equal to **{pounds:.2f}** pounds",
            color=self.bot.color
        ))

    @lbsgroup.command(description="converts ounces to pounds", usage="<ounce>")
    async def ounce(self, ctx, ounce: float):
        pounds = ounce / 16
        await ctx.send(embed=discord.Embed(
            description=f"> **{ounce}** ounces is equal to **{pounds:.2f}** pounds",
            color=self.bot.color
        ))

    @commands.group(invoke_without_command=True, name="stone")
    async def stone_group(self, ctx):
        await ctx.send_help(ctx.command)

    @stone_group.command(description="converts pounds to stone", usage="<lbs>")
    async def lbs(self, ctx, lbs: float):
        stone = lbs / 14
        embed = discord.Embed(
            description=f"> **{lbs}** pounds is equal to **{stone:.2f}** stone",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @stone_group.command(description="converts kilograms to stone", usage="<kg>")
    async def kg(self, ctx, kg: float):
        stone = kg * 0.157473
        embed = discord.Embed(
            description=f"> **{kg}** kilograms is equal to **{stone:.2f}** stone",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @stone_group.command(description="converts ounces to stone", usage="<ounce>")
    async def ounce(self, ctx, ounce: float):
        stone = ounce / 224
        embed = discord.Embed(
            description=f"> **{ounce}** ounces is equal to **{stone:.2f}** stone",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, name="ounce")
    async def ounce_group(self, ctx):
        await ctx.send_help(ctx.command)

    @ounce_group.command(description="Converts pounds to ounces", usage="<lbs>")
    async def lbs(self, ctx, lbs: float):
        ounce = lbs * 16
        embed = discord.Embed(
            description=f"> **{lbs}** pounds is equal to **{ounce:.2f}** ounces",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @ounce_group.command(description="Converts kilograms to ounces", usage="<kg>")
    async def kg(self, ctx, kg: float):
        ounce = kg * 35.274
        embed = discord.Embed(
            description=f"> **{kg}** kilograms is equal to **{ounce:.2f}** ounces",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    @ounce_group.command(description="Converts stone to ounces", usage="<stone>")
    async def stone(self, ctx, stone: float):
        ounce = stone * 224
        embed = discord.Embed(
            description=f"> **{stone}** stone is equal to **{ounce:.2f}** ounces",
            color=self.bot.color
        )
        await ctx.send(embed=embed)

    # Crypto
        
    def require_dm():
        """Check if the bot can DM the user"""
        async def predicate(ctx: commands.Context):
            try:
                await ctx.author.send()
            except discord.HTTPException as error:
                if error.code == 50007:
                    raise commands.CommandError("You need to enable **DMs** to use this command")

            return True
        return commands.check(predicate)
        
    @staticmethod
    def shorten(value: str) -> str:
        return (value[: 20 - 2] + "..") if len(value) > 20 else value

    @tasks.loop(seconds=60)
    async def btc_notifier(self):
        subscriptions = await self.bot.db.fetch("SELECT * FROM btc_subscriptions")
        if subscriptions:
            for subscription in subscriptions:
                if user := self.bot.get_user(subscription.get("user_id")):
                    confirmed = await self.check_transaction_status(subscription.get("transaction"))

                    if not confirmed:
                        continue  

                    with contextlib.suppress(discord.HTTPException):
                        await user.send(
                            embed=discord.Embed(
                                color=self.bot.color,
                                description=(
                                "> Your **transaction**"
                                f" [`{self.shorten(subscription.get('transaction'))}`](https://mempool.space/tx/{subscription.get('transaction')})"
                                " has received a **confirmation**!"
                            ),
                        )
                    )

                    await self.bot.db.execute(
                    "DELETE FROM btc_subscriptions WHERE user_id = $1 AND transaction = $2",
                    subscription.get("user_id"),
                    subscription.get("transaction"),
                )

    @commands.group(
        name="btc",
        usage="(address)",
        example="bc1qe5vaz29nw0zkyayep..",
        aliases=["bitcoin"],
        invoke_without_command=True,
    )
    async def btc(self, ctx: commands.Context, address: str):
        """View information about a bitcoin address"""

        response = requests.get(f"https://blockchain.info/rawaddr/{address}")
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return await ctx.warn(f"Couldn't find an **address** for `{address}`")

        response_price = requests.get(
            "https://min-api.cryptocompare.com/data/price",
            params=dict(fsym="BTC", tsyms="USD"),
        )
        response_price.raise_for_status()
        price_data = response_price.json()
        price = price_data.get("USD")

        embed = discord.Embed(
            url=f"https://mempool.space/address/{address}",
            title="Bitcoin Address",
            color=self.bot.color
        )

        embed.add_field(
            name="Balance",
            value=f"{(data['final_balance'] / 100000000 * price):,.2f} USD",
        )
        embed.add_field(
            name="Received",
            value=f"{(data['total_received'] / 100000000 * price):,.2f} USD",
        )
        embed.add_field(name="Sent", value=f"{(data['total_sent'] / 100000000 * price):,.2f} USD")
        if data["txs"]:
            embed.add_field(
                name="Transactions",
                value="\n".join(
                    f"> [`{tx['hash'][:19]}..`](https://mempool.space/tx/{tx['hash']}) {(tx['result'] / 100000000 * price):,.2f} USD"
                    for tx in data["txs"][:5]
                ),
            )

        await ctx.send(embed=embed)


    @staticmethod
    async def check_transaction_status(transaction: str) -> bool:
        url = f"https://mempool.space/api/tx/{transaction}/status"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("confirmed", False)
        return False

    @btc.command(
        name="subscribe",
        usage="(transaction)",
        example="2083b2e0e3983882755cc..",
        aliases=["sub", "notify", "watch"],
    )
    @require_dm()
    async def btc_subscribe(self, ctx: commands.Context, transaction: str):
        """Send a notification when a transaction is confirmed"""

        confirmed = await self.check_transaction_status(transaction)

        if confirmed:
            return await ctx.send_warning(
                f"Transaction [`{self.shorten(transaction)}`](https://mempool.space/tx/{transaction}) already has a **confirmation**"
            )

        try:
            await self.bot.db.execute(
                "INSERT INTO btc_subscriptions (user_id, transaction) VALUES ($1, $2)",
                ctx.author.id,
                transaction.upper(),
            )
        except:
            await ctx.send_warning(
                f"Already subscribed to [`{self.shorten(transaction)}`](https://mempool.space/tx/{transaction})"
            )
        else:
            await ctx.send_success(
                f"Subscribed to [`{self.shorten(transaction)}`](https://mempool.space/tx/{transaction})"
            )

        

async def setup(bot):
    await bot.add_cog(Utility(bot))   