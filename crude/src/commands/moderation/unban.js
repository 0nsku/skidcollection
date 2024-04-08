const { MessageEmbed, Permissions } = require("discord.js");
const modlogSchema = require('../../database/modlog')

module.exports.run = async (client, message, args) => {

  const bannedUserAudit = await message.guild.bans.fetch()

  const user = bannedUserAudit.get(args[0])

  if(!message.member.permissions.has(Permissions.FLAGS.BAN_MEMBERS)) return message.channel.send(`You're missing the \`ban members\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.BAN_MEMBERS)) return message.channel.send(`I'm missing the \`ban members\` permissions`)

  if(!user) return message.channel.send(`You didn't provide a userid <:ayo_deny:909854484774125588>`)

  message.guild.members.unban(user.user.id).then(() => {
    message.channel.send(`**${user.user.tag}** has been unbanned`)
  }).catch(() => {
    message.channel.send(`**${user.user.tag}** couldn't be unbanned <:ayo_deny:909854484774125588>`)
  })

  const modembed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor('Crude Moderation')
  .setDescription(`<:ayo_user:909855548399288320> **User**: ${user.user.tag}\n<:ayo_ban:909855911386959953> **Action**: Unban
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
  name: "unban",
  aliases: ['ub'],
  description: 'unbans userid',
  parameters: 'user',
  permissions: ['BAN MEMBERS'],
  syntax: 'unban [userid]',
  example: 'unban 261976182872866817'
}