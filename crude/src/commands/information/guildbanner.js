const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {
    
  let banner = message.guild.bannerURL({ size: 2048 })

  if (banner) {
    banner = message.guild.bannerURL({ size: 2048 })

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setAuthor(message.guild.name, message.guild.iconURL({ dynamic: true }))
    .setImage(banner)

    message.channel.send({ embeds: [embed] }) 
  } else {
    message.channel.send(`This server doesn't have a banner`)
  }
}

module.exports.config = {
  name: "guildbanner",
  aliases: [],
  description: 'shows server banner',
  parameters: '',
  permissions: '',
  syntax: 'guildbanner',
  example: 'guildbanner'
}