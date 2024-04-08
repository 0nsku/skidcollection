const { MessageEmbed, Permissions } = require("discord.js")

module.exports.run = async (client, message, args) => {

  let icon = args[0]

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_GUILD)) return message.channel.send(`You're missing the \`manage guild\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_GUILD)) return message.channel.send(`I'm missing the \`manage guild\` permissions`)

  if (!icon) return message.channel.send('You need to provide a url <:ayo_deny:909854484774125588>')

  if (message.attachments.first()) {
    icon = message.attachments.first().url
    message.guild.setIcon(icon).then(() => {
    message.channel.send(`Sucessfully set the guild icon to ${icon}`)
  })
  } else {
    if (!icon) return message.channel.send('You need to provide a url or attachment to set icon')

    message.guild.setIcon(icon).then(() => {
      message.channel.send(`Sucessfully set the guild icon to ${icon}`)
    }).catch(() => {
      message.channel.send(`Couldn't set icon <:ayo_deny:909854484774125588>`)
    })
  }
}

module.exports.config = {
  name: "seticon",
  aliases: [],
  description: 'sets server icon',
  parameters: '',
  permissions: '',
  syntax: 'seticon [url]',
  example: 'seticon [url]'
}