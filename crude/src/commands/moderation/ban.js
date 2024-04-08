const { MessageEmbed, Permissions } = require("discord.js")
const modlogSchema = require('../../database/modlog')

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0]);

  let reason = args.slice(1).join(" ");

  if (!reason) reason = 'No Reason'

  if(!message.member.permissions.has(Permissions.FLAGS.BAN_MEMBERS)) return message.channel.send(`You're missing the \`ban members\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.BAN_MEMBERS)) return message.channel.send(`I'm missing the \`ban members\` permissions`)

  if(!user) return message.channel.send(`You didn't mention a user <:ayo_deny:909854484774125588>`)

  if(user === message.member) return message.channel.send(`You can't ban yourself`) 

  if(user === client.user.id) return message.channel.send('Lol nice try')

  //if (message.member.roles.highest.position <= user.roles.highest.position)

  if (user.roles.highest.position >= message.member.roles.highest.position) return message.channel.send('You cant ban someone above you')

  if (!user.bannable) return message.channel.send(`I can't ban someone above me`)

  const userembed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Crude Moderation')
  .setDescription(`<:ayo_user:909855548399288320> **Moderator**: ${message.author.tag}\n<:ayo_ban:909855911386959953> **Action**: Banned from ${message.guild.name}\n<:ayo_reason:909855408183730206> **Reason**: ${reason}
  `)
  .setThumbnail(message.guild.iconURL({ dynamic: true }))
  .setTimestamp()

  user.send({ embeds: [userembed] }).catch(err => console.log(err))
  
  user.ban({ reason: `${reason}` }).then(() => {
  message.channel.send(`**${user.user.tag}** has been banned`)
  }).catch(err => console.log(err))

  const data = await modlogSchema.findOne({
    GuildID: message.guild.id,
  });

  if (!data) return;
    
  const modembed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor('Crude Moderation')
  .setDescription(`
  <:ayo_user:909855548399288320> **User**: ${user.user.tag}
  <:ayo_ban:909855911386959953> **Action**: Banned
  <:ayo_reason:909855408183730206> **Reason**: ${reason}
  `)
  .setFooter(`Moderator: ${message.author.tag}`)
  .setThumbnail(message.guild.iconURL({ dynamic: true }))
  .setTimestamp()

  const channel = message.guild.channels.cache.get(data.Modlog)

  if (!channel) return;

  channel.send({ embeds: [modembed] }).catch(err => console.log(err))
}

module.exports.config = {
  name: "ban",
  aliases: ['b'],
  description: 'bans mentioned user',
  parameters: 'user',
  permissions: ['BAN MEMBERS'],
  syntax: 'ban [user]',
  example: 'ban @vayo'
}