const { MessageEmbed }  = require("discord.js")
const { invite, support, upvote } = require('../../config.json')

module.exports = async (client, message) => {

  const channel = message.channels.cache.find(channel => channel.type === 'GUILD_TEXT' && channel.permissionsFor(message.me).has('SEND_MESSAGES'))

  if (message.memberCount < 0) {

    const guildembed = new MessageEmbed()

    .setColor('#36393F')
    .setDescription(`I cannot be in this server as it is below 30 members. You can reinvite me using this invite link once reaching the limit above 30 members by clicking [here.](${invite}) If you want more information join our support server by clicking [here!](${support})`)

    channel.send({ embeds: [guildembed] }).catch((err) => console.log(err))
    message.leave()
  } else {

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setDescription(`Thanks for using Crude, crude is a multipurpose bot that includes configuration, fun, image, information, moderation, and utility commands. It’s a great bot to manage your discord server with plenty of useful utility commands. Crude has a highly polished feature rich bot that has a smooth and clean theme. It’s loaded with 70+ commands that includes antinuke, antiraid, autorole, and much more!
  `)
  .addFields(
  { name: '<:ayo_link:909487190898253846> \`Useful Links\`', value: `[Support](${support})・[Invite](${invite})・[Upvote](${upvote})`, inline: false },
  )
  .setThumbnail(`${client.user.displayAvatarURL({dynamic: true })}`)
  .setTimestamp()

  const logchannel = client.channels.cache.get("910421090457763871")

  const logembed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Guild Join Logs')
  .setDescription(`Joined server **${message.name}** with **${message.memberCount}** members | Guild ID: **${message.id}**`)
  .setTimestamp()

  if (!channel) return;

  channel.send({ embeds: [embed] }).catch(err => console.log(err))
  logchannel.send({ embeds: [logembed] }).catch(err => console.log(err))
  }
}