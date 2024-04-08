const { MessageEmbed } = require("discord.js")
const urban = require('relevant-urban');
const { color } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const urbanword = args.join(" ");

  if (!urbanword) return message.channel.send('Provide a word smart guy')

  try {

    const word = await urban(`${urbanword}`)

    const embed = new MessageEmbed()

    .setColor(color)
    .setTitle(word.word)
    .setURL(word.urbanURL)
    .setDescription(word.definition)
    .addFields(
    { name: '**example**', value: `\`\`\`${word.example}\`\`\``, inline: false },
    )

    message.channel.send({ embeds: [embed] })

  } catch {
    message.channel.send('No results found')
  }
}
  
module.exports.config = {
  name: "urban",
  aliases: ['ub'],
  description: 'shows specificed word from urb dictionary',
  parameters: 'word',
  permissions: '',
  syntax: 'urban [word]',
  example: 'urban skid'
}