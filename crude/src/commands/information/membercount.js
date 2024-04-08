const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const usercount = message.guild.memberCount

  const botcount = message.guild.members.cache.filter(m => m.user.bot).size

  const humans = usercount - botcount

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`${message.guild.name} membercount`)
  .addFields(
  { name: '<:icons_globe:910983418366525451> \`Total\`', value: `${usercount}`, inline: true },
  { nalme: '<:ayo_user:909855548399288320> \`Humans\`', value: `${humans}`, inline: true },
  { name: '<:ayo_bot:909593239932244008> \`Bots\`', value: `${botcount}`, inline: true },
  )
  // .setDescription(`**${usercount}** members (**${humans}** humans & **${botcount}** bots)`)

  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "membercount",
  aliases: ['mc'],
  description: 'shows member count',
  parameters: '',
  permissions: '',
  syntax: 'membercount',
  example: 'membercount'
}