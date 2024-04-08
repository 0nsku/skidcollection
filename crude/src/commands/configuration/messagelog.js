const { MessageEmbed, Permissions } = require("discord.js")
const prefixSchema = require("../../database/prefix");
const messagelogSchema = require('../../database/messagelog')
const { botprefix } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const prefixData = await prefixSchema.findOne({
    GuildID: message.guild.id,
  }).catch(err => console.log(err))

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

  const data = await messagelogSchema.findOne({
    GuildID: message.guild.id,
  });

  const messagelogchannel = message.mentions.channels.first() || client.guilds.cache.get(message.guild.id).channels.cache.get(args[1])

  if (!args[0]) {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)
    
  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Getting started with Crude messagelog')
  .addFields(
  { name: '<:ayo_utility:909487256992088114> \`Setup\`', value: `The bot must have administrator permissions for the messagelog to work.`, inline: false },
  { name: '<:ayo_reason:909855408183730206> \`Messagelog\`', value: `You first have to enable the messagelog by using \`${guildprefix}messagelog enable <mention/id>\`.\nYou can disable the messagelog by using \`${guildprefix}messagelog disable\`.`, inline: false },
  )
  .setFooter('Crude Configuration')
        
  return message.channel.send({ embeds: [embed] })
  }

  if (args[0] === 'enable') {

    if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)

    if (!messagelogchannel || messagelogchannel.type !== 'GUILD_TEXT') return message.channel.send(`You forgot to provide a channel`)

    if (data) {
    await messagelogSchema.findOneAndRemove({
      GuildID: message.guild.id,
    });

    let newData = new messagelogSchema({
      Messagelog: messagelogchannel.id,
      GuildID: message.guild.id,
    });
    newData.save();

    message.channel.send(`Successfully set the messagelog to **${messagelogchannel.name}** <:ayo_approve:909854401311678474>`)
  } else if (!data) {
  
    let newData = new messagelogSchema({
      Messagelog: messagelogchannel.id,
      GuildID: message.guild.id,
    });
    newData.save();

    message.channel.send(`Successfully set the messagelog to **${messagelogchannel.name}** <:ayo_approve:909854401311678474>`)
   }
  }

  if (args[0] === 'disable') {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)

  const data = await messagelogSchema.findOne({
    GuildID: message.guild.id,
  });

  if (data) {
    await messagelogSchema.findOneAndRemove({
      GuildID: message.guild.id,
    });

  message.channel.send('Successfully disabled messagelog <:ayo_approve:909854401311678474>')
  }
  }
}

module.exports.config = {
  name: "messagelog",
  aliases: [],
  description: 'Views how to setup messagelog',
  parameters: '',
  permissions: 'ADMINISTRATOR',
  syntax: 'messagelog [command]',
  example: 'messagelog disable'
}