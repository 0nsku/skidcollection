const { MessageEmbed } = require("discord.js");

module.exports.run = async (client, message, args) => {

  const user = message.mentions.users.first() || message.author;

  function ran(min, max) {
    // min and max included
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('💁‍♀️ Treesh Machine 💁‍♀️')
  .addFields(
  { name: '\`Rating\`', value: `${user} is ${ran(0, 100)}% treeshy!`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "treeshrate",
  aliases: [],
  description: 'treeshrate rates user',
  parameters: 'user',
  permissions: '',
  syntax: 'treeshrate [user]',
  example: 'treeshrate @vayo'
}