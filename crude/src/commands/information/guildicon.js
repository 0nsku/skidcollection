const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {
    
  let icon = message.guild.iconURL({ size: 2048, dynamic: true })

  if (icon) {
    icon = message.guild.iconURL({ size: 2048, dynamic: true })

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setAuthor(message.guild.name, message.guild.iconURL({ dynamic: true }))
    .setImage(icon)

    message.channel.send({ embeds: [embed] }) 
  } else {
    message.channel.send(`This server doesn't have a icon`)
  }
}

module.exports.config = {
  name: "guildicon",
  aliases: [],
  description: 'shows server icon',
  parameters: '',
  permissions: '',
  syntax: 'guildicon',
  example: 'guildicon'
}