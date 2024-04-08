const { MessageEmbed, Permissions } = require("discord.js");
const modlogSchema = require('../../database/modlog')

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0])

  const muterole = message.guild.roles.cache.find(role => role.name === 'Muted');

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) return message.channel.send(`You're missing the \`manage roles\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) return message.channel.send(`I'm missing the \`manage roles\` permissions`)

  if(!user) return message.channel.send(`You didn't mention a user <:ayo_deny:909854484774125588>`)

  if(user === message.member) return message.channel.send(`You can't mute yourself`) 

  if (user.roles.highest.position >= message.member.roles.highest.position) return message.channel.send(`You can't unmute someone above you`)

  if(!muterole) return message.channel.send('No muted role exist')

  user.roles.remove(muterole.id).then(() => {

    message.channel.send(`**${user.user.tag}** has been unmuted`)
  }).catch(() => {

    message.channel.send(`Couldn't mute that user <:ayo_deny:909854484774125588>`)
  })

  const modembed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor('Crude Moderation')
  .setDescription(`<:ayo_user:909855548399288320> **User**: ${user.user.tag}\n<:ayo_ban:909855911386959953> **Action**: Unmuted
  `)
  .setFooter(`Moderator: ${message.author.tag}`)
  .setThumbnail(message.guild.iconURL({ dynamic: true }))
  .setTimestamp()

  const data = await modlogSchema.findOne({
    GuildID: message.guild.id,
  });

  if (!data) return;

  const channel = message.guild.channels.cache.get(data.Modlog)

  if (!channel) return;

  channel.send({ embeds: [modembed] }).catch(err => console.log(err))
}

module.exports.config = {
  name: "unmute",
  aliases: ['um'],
  description: 'unmutes mentioned user',
  parameters: 'user',
  permissions: ['MANAGE ROLES'],
  syntax: 'unmute [user]',
  example: 'unmute @vayo'
}