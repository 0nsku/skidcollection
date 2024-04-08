const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {
    
  let user

  if (message.mentions.users.first())
  {
    
  user = message.mentions.users.first();

  } else if (args[0]) {

  user = message.guild.members.cache.get(args[0]).user;

  } else {
    
  user = message.author;
  }

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor(`${user.tag}`, user.displayAvatarURL({ dynamic: true }))
  .setImage(user.displayAvatarURL({size: 1024, dynamic: true}))

  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "avatar",
  aliases: ['av', 'pfp'],
  description: 'shows mentioned users profile picture',
  parameters: '',
  permissions: '',
  syntax: 'av [user]',
  example: 'av @vayo'
}