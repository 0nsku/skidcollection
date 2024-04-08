const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {

  let totalSeconds = (client.uptime / 1000);
  let days = Math.floor(totalSeconds / 86400);
  totalSeconds %= 86400;
  let hours = Math.floor(totalSeconds / 3600);
  totalSeconds %= 3600;
  let minutes = Math.floor(totalSeconds / 60);
  let seconds = Math.floor(totalSeconds % 60);

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setDescription(`Crude has been running for **${days}d ${hours}h ${minutes}m ${seconds}s**`)
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "uptime",
  aliases: [],
  description: 'shows bot uptime',
  parameters: '',
  permissions: '',
  syntax: 'uptime',
  example: 'uptime'
}