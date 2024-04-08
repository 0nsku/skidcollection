const { MessageEmbed } = require("discord.js");

module.exports.run = async (client, message, args) => {

  const user = message.mentions.users.first() || message.author;

  function ran(min, max) {
    // min and max included
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('📈 Rate Machine 📈')
  .addFields(
  { name: '\`Rating\`', value: `${user} a  ${ran(0, 10)}/10`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "rate",
  aliases: [],
  description: 'rates user',
  parameters: 'user',
  permissions: '',
  syntax: 'rate [user]',
  example: 'rate @vayo'
}