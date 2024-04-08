const { MessageEmbed, Permissions } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0]);

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_MESSAGES)) return message.channel.send(`You're missing the \`manage messages\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_MESSAGES)) return message.channel.send(`I'm missing the \`manage messages\` permissions`)

  if(!user) return message.channel.send(`You didn't mention a user <:ayo_deny:909854484774125588>`)

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor('📊Known or Unknown📊')
  .setDescription(`${user}`)
  .setThumbnail(user.user.displayAvatarURL({dynamic: true}))    
  .setFooter(`Poll started by: ${message.author.username}`)
  .setTimestamp()
    
  let messageEmbed = await message.channel.send({ embeds: [embed] }).catch(err => console.log(err))
  messageEmbed.react('✔️')
  messageEmbed.react('❌')
}

module.exports.config = {
  name: "knownpoll",
  aliases: [],
  description: 'sees if a specified user is known',
  parameters: 'user',
  permissions: 'MANAGE MESSAGES',
  syntax: 'knownpoll [user]',
  example: 'knownpoll 261976182872866817'
}