module.exports.run = async (client, message, args) => {

  message.channel.send(`Websocket: **${Math.round(client.ws.ping)}** ms(${(Date.now() - message.createdTimestamp)})`)
}
  
module.exports.config = {
  name: "ping",
  aliases: [],
  description: 'shows bot ping',
  parameters: '',
  permissions: '',
  syntax: 'ping',
  example: 'ping'
}