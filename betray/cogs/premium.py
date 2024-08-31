@bot.command(aliases=['forcem'])
async def forcemarry(ctx, user: discord.User):
    if not has_premium(ctx.author.id):
        embed = discord.Embed(description="You need to have premium to use this command", color=0x2b2d31)
        embed.add_field(name="Premium Access", value="[Click here](https://betray.vip/premium)")
        return await ctx.send(embed=embed)
    embed = None
    if ctx.author == user:
        embed = discord.Embed(title="", description=f"> you can not marry yourself :skull:.", color=0x2b2d31)
    elif marriages.get(ctx.author.id):
        embed = discord.Embed(title="", description=f"> you're already married.", color=0x2b2d31)
    elif marriages.get(user.id):
        embed = discord.Embed(title="", description=f"> they are already married.", color=0x2b2d31)
    else:
        marriages[ctx.author.id] = user.id
        marriages[user.id] = ctx.author.id
        save_marriages(marriages)
        embed = discord.Embed(title="", description=f"> You forced {user.mention} to marry you.", color=0x2b2d31)
    await ctx.send(embed=embed)
    
    
@bot.command(aliases=['selfclear'])
async def selfpurge(ctx, amount: int):
    if not has_premium(ctx.author.id):
        embed = discord.Embed(description="You need to have premium to use this command", color=0x2b2d31)
        embed.add_field(name="Premium Access", value="[Click here](https://betray.vip/premium)")
        return await ctx.send(embed=embed)
    amount = max(1, min(amount, 100))
    deleted = await ctx.channel.purge(limit=amount + 1, check=lambda msg: msg.author == ctx.author)
    embed = discord.Embed(description=f"Deleted {len(deleted)} messages from {ctx.author.mention}", color=0x2b2d31)
    
    await ctx.send(embed=embed)
    
@bot.command()
async def checkpremium(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    premium_users = []
    with open("premiumusers.txt", "r") as file:
        for line in file:
            premium_users.append(int(line.strip()))

    if user.id in premium_users:
        embed = discord.Embed(description=f"{user.mention} has **premium** <:spark:1217958768852078784>", color=0x2b2d31)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"{user.mention} is **broke** they dont have **premium**.", color=0x2b2d31)
        await ctx.send(embed=embed)

    premium_users = []
    with open("premiumusers.txt", "r") as file:
        for line in file:
            premium_users.append(int(line.strip()))
    if premium_users:
        user_mentions = [f"<@{user_id}>" for user_id in premium_users]
        embed = discord.Embed(
            title="Premium users",
            description="\n".join(user_mentions),
            color=0x2b2d31
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="No Premium Users",
            description="No users have premium.",
            color=0x2b2d31
        )
        await ctx.send(embed=embed)
        
@bot.command()
async def forcepurge(ctx, user: discord.User, amount: int):
    if not has_premium(ctx.author.id):
        embed = discord.Embed(description="You need to have premium to use this command", color=0x2b2d31)
        embed.add_field(name="Premium Access", value="[Click here](https://discord.gg/betray)")
        return await ctx.send(embed=embed)
    await ctx.channel.purge(limit=amount, check=lambda message: message.author == user)
    embed = discord.Embed(description=f"> Purged {user.mention}'s messages", color=0x2b2d31)
    await ctx.send(embed=embed)
    
@bot.command(aliases=['s'])
async def silent(ctx, user: discord.User, amount: int):
    if not has_premium(ctx.author.id):
        embed = discord.Embed(description="You need to have premium to use this command", color=0x2b2d31)
        embed.add_field(name="Premium Access", value="[Click here](https://discord.gg/betray)")
        return await ctx.send(embed=embed)
    amount = min(amount, 50)
    user_deletion_count[(ctx.guild.id, user.id)] = amount
    
    embed = discord.Embed(description=f"{user.mention} silent for the next {amount} messages", color=0x2b2d31)
    await ctx.send(embed=embed)
