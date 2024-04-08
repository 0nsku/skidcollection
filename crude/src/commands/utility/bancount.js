module.exports.run = async (client, message, args) => {

  const bancount = message.guild.bans.cache.size
  
  message.channel.send(`${message.guild.name} has **${bancount}** bans`)
}

module.exports.config = {
  name: "bancount",
  aliases: ['bc'],
  description: 'shows guild ban count',
  parameters: '',
  permissions: '',
  syntax: 'bancount',
  example: 'bancount'
}