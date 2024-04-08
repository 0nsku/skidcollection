const { MessageEmbed, Permissions } = require("discord.js");
const modlogSchema = require('../../database/modlog')

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0])

  let reason = args.slice(1).join(" ");

  if (!reason) reason = 'No Reason'

  const muterole = message.guild.roles.cache.find(role => role.name === 'Muted');

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) return message.channel.send(`You're missing the \`manage roles\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) return message.channel.send(`I'm missing the \`manage roles\` permissions`)

  if(!user) return message.channel.send(`You didn't mention a user :thumbsdown:`)

  if(user === message.member) return message.channel.send(`You can't mute yourself`) 

  if (user.roles.highest.position >= message.member.roles.highest.position) return message.channel.send(`You can't mute someone above you`)

  if(!muterole) { 

    try {
      muteRole = await message.guild.roles.create({
        name: 'Muted',
        color: 'DEFAULT',
      })
      message.guild.channels.cache.forEach(async (channel) => {
        await channel.permissionOverwrites.edit(muteRole, {
            SEND_MESSAGES: false,
            ADD_REACTIONS: false,
            SPEAK: false,
            CONNECT: false,
        })
      })
  } catch (e) {
    console.log(e)
    }
  }

  const muterole2 = message.guild.roles.cache.find(role => role.name === 'Muted');

  if (user.roles.cache.has(muterole2.id)) return message.channel.send('User is already muted')

  user.roles.add(muterole).then(() => {

    const userembed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('Crude Moderation')
    .setDescription(`<:ayo_user:909855548399288320> **Moderator**: ${message.author.tag}\n<:ayo_ban:909855911386959953> **Action**: Muted in ${message.guild.name}\n<:ayo_reason:909855408183730206> **Reason**: ${reason}
    `)
    .setThumbnail(message.guild.iconURL({ dynamic: true }))
    .setTimestamp()

    user.send({ embeds: [userembed] }).catch(err => console.log(err))

    message.channel.send(`**${user.user.tag}** has been muted`)
  }).catch((err) => {

    message.channel.send(`Couldn't mute that user <:ayo_deny:909854484774125588>`)
  })

  const modembed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor('Crude Moderation')
  .setDescription(`<:ayo_user:909855548399288320> **User**: ${user.user.tag}\n<:ayo_ban:909855911386959953> **Action**: Muted\n<:ayo_reason:909855408183730206> **Reason**: ${reason}
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
  name: "mute",
  aliases: ['m'],
  description: 'mutes mentioned user',
  parameters: 'user',
  permissions: ['MANAGE ROLES'],
  syntax: 'mute [user]',
  example: 'mute @vayo'
}