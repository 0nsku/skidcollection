const { MessageEmbed, Permissions } = require("discord.js")

module.exports.run = async (client, message, args) => {

  const pollquestion = args.join(" ");

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_MESSAGES)) return message.channel.send(`You're missing the \`manage messages\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_MESSAGES)) return message.channel.send(`I'm missing the \`manage messages\` permissions`)

  if (!pollquestion) return message.channel.send('Provide a question plz')

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Poll')
  .addFields(
  { name: '<:ayo_fun:909487214176645151> \`Question\`', value: `<:ayo_reason:909855408183730206> ${pollquestion}`, inline: false },
  )

  let messageEmbed = await message.channel.send({ embeds: [embed] }).catch(err => console.log(err))
  messageEmbed.react('✔️')
  messageEmbed.react('❌')
}

module.exports.config = {
  name: "quickpoll",
  aliases: [],
  description: 'poll yes/no question',
  parameters: 'user',
  permissions: 'MANAGE MESSAGES',
  syntax: 'knownpoll [user]',
  example: 'knownpoll 261976182872866817'
}