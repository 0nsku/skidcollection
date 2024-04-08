const { MessageAttachment } = require("discord.js")
const DIG = require("discord-image-generation");

module.exports.run = async (client, message, args) => {

  if (!args[0]) return message.channel.send('You need to provide a hex code')

  try {

    const img = await new DIG.Color().getImage(args[0]);

    const attach = new MessageAttachment(img, `${args[0]}.png`);

    message.channel.send({ files: [attach] })
  } catch (err) {
    message.channel.send('Not a valid hex code')
  }
}

module.exports.config = {
  name: "color",
  aliases: [],
  description: 'shows color',
  parameters: '',
  permissions: '',
  syntax: 'color [hexcode]',
  example: 'color 36393F'
}