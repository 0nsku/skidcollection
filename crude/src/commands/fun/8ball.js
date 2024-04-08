const { MessageEmbed } = require("discord.js")
const prefixSchema = require("../../database/prefix");
const { botprefix, invite } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const prefixData = await prefixSchema.findOne({
    GuildID: message.guild.id,
  }).catch(err => console.log(err))

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

  const question = args.join(" ");

  const answers = [
    'No you weak fuck',
    'Yes but ur a skid',
    'Lmao no but where yo mom at?',
    'Nope but add this bot to ur server',
    'No',
    'Yes',
    'Tt is certain',
    `Click [here](${invite})`,
    'Outlook not so good',
    'Concentrate and ask again',
    'Tts best not to tell u now',
    'Most likely',
    'Ask again later dickhead',
    'Indeed my good sir',
  ];
    
  const randomanswers = answers[Math.floor(Math.random() * answers.length)];
    
  if (!question) return message.channel.send(`You did not provide a question <:ayo_deny:909854484774125588>`)

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('🎱 8ball Machine 🎱')
  .addFields(
  { name: '<:ayo_fun:909487214176645151> \`Question\`', value: `${question}`, inline: false },
  { name: '<:ayo_reason:909855408183730206> \`Answer\`', value: `${randomanswers}`, inline: false },
  )
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "8ball",
  aliases: ['8b'],
  description: 'ask the magic 8-ball a question',
  parameters: 'question',
  permissions: '',
  syntax: '8ball [question]',
  example: '8ball is picasso a good bot?'
}