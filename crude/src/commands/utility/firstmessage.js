const { MessageEmbed } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const guild = message.guild.id

  const channel = message.channel.id

  const fetchMessages = await message.channel.messages.fetch({
    after: 1,
    limit: 1,
  });
  const firstmessage = fetchMessages.first();

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setDescription(`
  The first message in ${message.channel} — click [here](https://discord.com/channels/${guild}/${channel}/${firstmessage.id})
  `)  

  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "firstmessage",
  aliases: [],
  description: 'shows first message',
  parameters: '',
  permissions: '',
  syntax: 'firstmessage',
  example: 'firstmessage'
}