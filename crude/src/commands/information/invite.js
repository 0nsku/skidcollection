const { MessageEmbed } = require("discord.js")
const { invite } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setDescription(`Add crude to your server — [invite](${invite})`)

  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "invite",
  aliases: [],
  description: 'shows bot invite',
  parameters: '',
  permissions: '',
  syntax: 'invite',
  example: 'invite'
}