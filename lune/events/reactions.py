from discord.ext import commands 
import discord

class Reactions(commands.Cog): 
  def __init__(self, bot: commands.AutoShardedBot): 
   self.bot = bot 
   
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent): 
   guild = self.bot.get_guild(payload.guild_id)
   member = guild.get_member(payload.user_id)  
   if member is None: return
   if member.bot: return
   await self.bot.db.execute("INSERT INTO reactionsnipe VALUES ($1,$2,$3,$4,$5,$6,$7)", guild.id, payload.channel_id, member.name, member.display_avatar.url, payload.emoji.name, payload.emoji.url, payload.message_id)  

async def setup(bot: commands.AutoShardedBot) -> None: 
  await bot.add_cog(Reactions(bot))  
