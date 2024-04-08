const { commands } = require('../../../config.json')

module.exports.run = async (client, message, args) => {
  
  message.channel.send(`Crude has **${commands}** commands`)
}

module.exports.config = {
  name: "commandcount",
  aliases: [],
  description: 'shows command count',
  parameters: '',
  permissions: '',
  syntax: 'commandcount',
  example: 'commandcount'
}