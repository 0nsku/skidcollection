const { MessageEmbed } = require("discord.js");

module.exports.run = async (client, message, args) => {

const user = message.mentions.users.first() || message.author;

  const replies = [
    "8D",
    "8=D",
    "8==D",
    "8===D",
    "8====D",
    "8=====D",
    "8======D",
    "8========D",
    "8=========D",
    "8==========D",
    "8===========D",
    "8============D",
    "8=============D",
    "pp is nonexistent",
    "pp too big"
  ];

  const random = Math.floor(Math.random() * replies.length);

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('🍆 Penis Machine 🍆')
  .addFields(
  { name: '\`Rating\`', value: `${user} penis\n${replies[random]}`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "penis",
  aliases: [],
  description: 'penis rates user',
  parameters: 'user',
  permissions: '',
  syntax: 'penis [user]',
  example: 'penis @vayo'
}