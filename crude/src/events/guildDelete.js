const { MessageEmbed }  = require("discord.js")

module.exports = async (client, message) => {

  const logchannel = client.channels.cache.get("")

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Guild Leave Logs')
  .setDescription(`Left server **${message.name}** with **${message.memberCount}** members | Guild ID: **${message.id}**`)
  .setTimestamp()

  logchannel.send({ embeds: [embed] })
}