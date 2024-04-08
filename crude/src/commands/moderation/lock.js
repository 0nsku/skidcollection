const { MessageEmbed, Permissions } = require("discord.js");
const modlogSchema = require('../../database/modlog')

module.exports.run = async (client, message, args) => {

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_CHANNELS)) return message.channel.send(`You're missing the \`manage channels\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_CHANNELS)) return message.channel.send(`I'm missing the \`manage channels\` permissions`)

  const lockchannel = message.channel;

  message.guild.roles.cache.forEach(role => {
    lockchannel.permissionOverwrites.edit(role, {
        SEND_MESSAGES: false,
        ADD_REACTIONS: false,
    });
  }).then(() => {

    message.channel.send(`**#${lockchannel.name}** has been locked <:ayo_locked:909854630593302560>`)

  }).catch((err) => console.log(err))  

  const modembed = new MessageEmbed()

  .setColor('#36393F')
  .setAuthor('Crude Moderation')
  .setDescription(`<:ayo_user:909855548399288320> **Moderator**: ${message.author.tag}\n<:ayo_ban:909855911386959953> **Action**: Lock Channel
  `)
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
  name: "lock",
  aliases: ['lc'],
  description: 'locks channel',
  parameters: '',
  permissions: ['MANAGE CHANNELS'],
  syntax: 'lock',
  example: 'lock'
}