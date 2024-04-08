const { MessageEmbed } = require("discord.js");

module.exports.run = async (client, message, args) => {

  const user = message.mentions.users.first() || message.author;

  function ran(min, max) {
    // min and max included
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('🥺 Simp Machine 🥺')
  .addFields(
  { name: '\`Rating\`', value: `${user} is ${ran(0, 100)}% simp!`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "simprate",
  aliases: [],
  description: 'simprate rates user',
  parameters: 'user',
  permissions: '',
  syntax: 'simprate [user]',
  example: 'simprate @vayo'
}