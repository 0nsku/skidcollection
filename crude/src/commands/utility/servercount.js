module.exports.run = async (client, message, args) => {

  const servercount = client.guilds.cache.size
  
  message.channel.send(`Crude is in **${servercount}** servers`)
}

module.exports.config = {
  name: "servercount",
  aliases: [],
  description: 'shows server count',
  parameters: '',
  permissions: '',
  syntax: 'servercount',
  example: 'servercount'
}