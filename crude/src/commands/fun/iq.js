const { MessageEmbed } = require("discord.js");

module.exports.run = async (client, message, args) => {

  const user = message.mentions.users.first() || message.author;

  function ran(min, max) {
    // min and max included
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('🧠 IQ Machine 🧠')
  .addFields(
  { name: '\`Rating\`', value: `${user} iq is ${ran(0, 200)}`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "iq",
  aliases: [],
  description: 'iq rates user',
  parameters: 'user',
  permissions: '',
  syntax: 'iq [user]',
  example: 'iq @vayo'
}