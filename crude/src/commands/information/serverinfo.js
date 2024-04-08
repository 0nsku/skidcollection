const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const owner = await message.guild.fetchOwner()

  const channelscount = message.guild.channels.cache

  const membercount = message.guild.memberCount

  const botcount = message.guild.members.cache.filter(m => m.user.bot).size
    
  function checkDays(date) {
    let now = new Date();
    let diff = now.getTime() - date.getTime();
    let days = Math.floor(diff / 86400000);
    return days + (days == 1 ? " day" : " days") + " old";
  };

  const verificationlevels = {
    NONE: 'None',
    LOW: 'Low',
    MEDIUM: 'Medium',
    HIGH: 'High',
    VERY_HIGH: 'Highest'
  };

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`Server information for ${message.guild.name}`)
  .setDescription(`<:icons_id:912146134028415016> ID: \`${message.guild.id}\`\n<:ayo_reason:909855408183730206> Server Age: \`${checkDays(message.channel.guild.createdAt)}\``)
  .addFields(
  { name: '<:ayo_user:909855548399288320> Owner', value: `${owner.user.tag}`, inline: true },
  { name: '<:icons_nitroboost:912523207620313118> Boost', value: `Level ${message.guild.premiumTier >= 1 ? `${message.guild.premiumTier}` : `0`}\n${message.guild.premiumSubscriptionCount >= 1 ? `${message.guild.premiumSubscriptionCount}` : `0`} Boosts`, inline: true },
  { name: '<:icons_defaultperms:912521873227673661> Members', value: `${message.guild.memberCount} members total\n${membercount - botcount} humans & ${botcount} bots`, inline: true },
  { name: '<:icons_list:912521740045930506> Channels', value: `${channelscount.filter(channel => channel.type === 'GUILD_TEXT').size} Text channels\n${channelscount.filter(channel => channel.type === 'GUILD_VOICE').size} Voice channels\n${channelscount.filter(channel => channel.type === 'GUILD_CATEGORY').size} categories
  `, inline: true },
  { name: '<:ayo_fun:909487214176645151> Other', value: `${message.guild.roles.cache.size} Roles\n${message.guild.emojis.cache.size} Emojis\n${message.guild.stickers.cache.size} Stickers`, inline: true },
  { name: '<:ayo_info:909487156131668028> Information', value: `Region: Not supported\nVerification Level: ${verificationlevels[message.guild.verificationLevel]}`, inline: true },
  )
  .setThumbnail(message.guild.iconURL({ dynamic: true }))

  message.channel.send({ embeds: [embed] }) 
}

module.exports.config = {
  name: "serverinfo",
  aliases: ['si'],
  description: 'shows server info',
  parameters: '',
  permissions: '',
  syntax: 'serverinfo',
  example: 'serverinfo'
}