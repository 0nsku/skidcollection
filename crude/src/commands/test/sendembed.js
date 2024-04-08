const { MessageEmbed } = require('discord.js')

module.exports.run = async (client, message, args) => {

  const embed = new MessageEmbed()

  .setColor(color)

  if (!args[0]) return message.channel.send({ embeds: [embed] })

  try {

    const json = JSON.parse(args.join(' '))
    const { text = '' } = json

    if ({}.hasOwnProperty.call(json, "thumbnail")) {
      json.thumbnail = { url: json.thumbnail };
    }
      
    if ({}.hasOwnProperty.call(json, "image")) {
      json.image = { url: json.image };
    }

    message.channel.send({ embeds: [json] })
    } catch (e) {
      message.channel.send('error occured 👎');
    }
}

module.exports.config = {
  name: "sendembed",
  aliases: ['se'],
}