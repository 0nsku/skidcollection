const { support } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  message.channel.send(`<@${message.author.id}>, join this server for any help or questions — ${support}`)
}

module.exports.config = {
  name: "support",
  aliases: [],
  description: 'shows bot support',
  parameters: '',
  permissions: '',
  syntax: 'support',
  example: 'support'
}