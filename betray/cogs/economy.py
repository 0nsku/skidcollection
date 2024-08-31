import discord
from discord.ext import commands
from discord.ext.commands import command, Cog

class economy(Cog):
    def __init_(self, bot):
        self.bot = bot

    @command(aliases=['reg'])
    async def register(self, ctx):
        user_id = ctx.author.id
        with open('economylogs.txt', 'r') as f:
            for line in f:
                if str(user_id) in line:
                    embed = discord.Embed(title="", description="> you are **already registered**.", color=0x2b2d31)
                    await ctx.send(embed=embed)
                    return
        with open('economylogs.txt', 'a') as f:
            f.write(f"{user_id} 3000\n")
        embed = discord.Embed(description="> Registration successful. You've been given **3000 coins**.", color=0x2b2d31)
        await ctx.send(embed=embed)
    
    @command(aliases=['bal'])
    async def balance(self, ctx):
        user_id = ctx.author.id
        with open('economylogs.txt', 'r') as f:
            for line in f:
                if str(user_id) in line:
                    user_balance = int(line.split()[1])
                    embed = discord.Embed(title="Balance", description=f"> Your cash - **{user_balance}**", color=0x2b2d31)
                    await ctx.send(embed=embed)
                    return
        embed = discord.Embed(title="", description="> You are not **registered**.", color=0x2b2d31)
        await ctx.send(embed=embed)
    
    @command(aliases=['cf'])
    async def coinflip(self, ctx, coins: int, choice: str):
        if choice.lower() not in ['heads', 'tails']:
            embed = discord.Embed(title="Coin Flip", description="> please enter a valid amount of coins", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        if coins <= 0:
            embed = discord.Embed(title="Coin Flip", description="> please enter a positive amount :skull:.", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        if choice.lower() not in ['heads', 'tails']:
            embed = discord.Embed(title="Coin Flip", description="> please do $coinflip (amount) (heads or tails)", color=0x2b2d31)
            await ctx.send(embed=embed)
            return

        user_id = ctx.author.id
        with open('economylogs.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if str(user_id) in line:
                    user_balance = int(line.split()[1])
                    if user_balance < coins:
                        embed = discord.Embed(title="Coin Flip", description="> your **broke**, you dont got that money :skull:.", color=0x2b2d31)
                        await ctx.send(embed=embed)
                        return
                    lines[i] = f"{user_id} {user_balance - coins}\n"
                    break
            else:
                embed = discord.Embed(description="> You are not **registered**", color=0x2b2d31)
                await ctx.send(embed=embed)
                return

        with open('economylogs.txt', 'w') as f:
            f.writelines(lines)

        embed = discord.Embed(title="Coin Flip", color=0x2b2d31)
        result = random.choice(['heads', 'tails']) 
        if result == choice.lower():
            winnings = coins * 2
            embed.add_field(name="", value=f"> dam, you won {winnings} coins")
            log_transaction(f"{ctx.author.name} won {winnings} coins in a coin flip.")
        else:
            embed.add_field(name="", value=f"> lmao, you lost {coins}")
            log_transaction(f"{ctx.author.name} lost {coins} coins in a coin flip.")

        with open('economylogs.txt', 'w') as f:
            f.writelines(lines)

        await ctx.send(embed=embed)
    
    @command()
    async def givecash(self, ctx, user: discord.Member, amount: int):
        if amount <= 0:
            embed = discord.Embed(description="> enter an amount to give.", color=0x2b2d31)
            await ctx.send(embed=embed)
            return
        giver_id = ctx.author.id
        receiver_id = user.id
        with open('economylogs.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if str(giver_id) in line:
                    giver_balance = int(line.split()[1])
                    if giver_balance < amount:
                        embed = discord.Embed(description="> your **broke**, you dont got that money :skull:.", color=0x2b2d31)
                        await ctx.send(embed=embed)
                        return
                    lines[i] = f"{giver_id} {giver_balance - amount}\n"
                    break
            else:
                embed = discord.Embed(title="", description="You are not **registered**", color=0x2b2d31)
                await ctx.send(embed=embed)
                return

        with open('economylogs.txt', 'w') as f:
            f.writelines(lines)
        with open('economylogs.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if str(receiver_id) in line:
                    receiver_balance = int(line.split()[1])
                    lines[i] = f"{receiver_id} {receiver_balance + amount}\n"
                    break
            else:
                lines.append(f"{receiver_id} {amount}\n")

        with open('economylogs.txt', 'w') as f:
            f.writelines(lines)

        embed = discord.Embed(description=f"> you gave {amount} coins {user.mention}.", color=0x2b2d31)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(economy(bot))