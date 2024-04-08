const { MessageEmbed, Permissions } = require("discord.js")
const math = require("mathjs");

module.exports.run = async (client, message, args) => {

  const question = args.join(" ");

  if (!question) return message.channel.send('Provide a question plz')

  let answer;

  try {
    answer = math.evaluate(question)
  } catch (e) {
    return message.channel.send(`Provide a valid question`)
  }

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Calculator')
  .addFields(
  { name: '<:ayo_fun:909487214176645151> \`Question\`', value: `${question}`, inline: false },
  { name: '<:ayo_reason:909855408183730206> \`Answer\`', value: `${answer}`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "calculator",
  aliases: [],
  description: 'calculates math problem',
  parameters: '',
  permissions: '',
  syntax: 'calculator [problem]',
  example: 'calculator 9+3'
}