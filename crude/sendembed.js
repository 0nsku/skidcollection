const { MessageEmbed, Permissions } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const json = JSON.parse(args.join(' '))

  if (!args[0]) return message.channel.send('Provide a valid json, example: {"title": "embed", "description": "this is an embed"}')

  try {
  //if ({}.hasOwnProperty.call(json, "thumbnail")) {
  //  json.thumbnail = { url: json.thumbnail };
  //}
  //if ({}.hasOwnProperty.call(json, "image")) {
  //  json.image = { url: json.image };
  //}
  message.channel.send({ embeds: [json] })
 // message.channel.send({ embeds: [text] })
  } catch (err) {
    console.log(err)
    message.channel.send('Invalid json, try again')
  }
}

module.exports.config = {
  name: "sendembed",
  aliases: [],
  description: 'sends specific embed json',
  parameters: '',
  permissions: 'MANAGE MESSAGES',
  syntax: 'sendembed [json]',
  example: 'sendembed {"title": "embed", "description": "this is an embed"}'
}