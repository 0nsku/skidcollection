const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setDescription(`Crude — v13.2.0`)
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "version",
  aliases: [],
  description: 'shows bot version',
  parameters: '',
  permissions: '',
  syntax: 'version',
  example: 'version'
}