const { MessageEmbed } = require("discord.js")
const { brando, cari } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Crude credits')
  .setDescription(`
  Inspiration: **haunt & bleed**
  `)  

  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "credits",
  aliases: [],
  description: 'shows bot credits',
  parameters: '',
  permissions: '',
  syntax: 'credits',
  example: 'credits'
}