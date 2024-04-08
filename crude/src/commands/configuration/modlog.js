const { MessageEmbed, Permissions } = require("discord.js")
const prefixSchema = require("../../database/prefix");
const modlogSchema = require('../../database/modlog')
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

  const data = await modlogSchema.findOne({
    GuildID: message.guild.id,
  });

  const modlogchannel = message.mentions.channels.first() || client.guilds.cache.get(message.guild.id).channels.cache.get(args[1])

  if (!args[0]) {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)
    
  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Getting started with Crude modlog')
  .addFields(
  { name: '<:ayo_utility:909487256992088114> \`Setup\`', value: `The bot must have administrator permissions for the modlog to work.`, inline: false },
  { name: '<:ayo_reason:909855408183730206> \`Modlog\`', value: `You first have to enable the modlog by using \`${guildprefix}modlog enable <mention/id>\`.\nYou can disable the modlog by using \`${guildprefix}modlog disable\`.`, inline: false },
  )
  .setFooter('Crude Configuration')
        
  return message.channel.send({ embeds: [embed] })
  }

  if (args[0] === 'enable') {

    if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)

    if (!modlogchannel || modlogchannel.type !== 'GUILD_TEXT') return message.channel.send(`You forgot to provide a channel`)

    if (data) {
    await modlogSchema.findOneAndRemove({
      GuildID: message.guild.id,
    });

    let newData = new modlogSchema({
      Modlog: modlogchannel.id,
      GuildID: message.guild.id,
    });
    newData.save();

    message.channel.send(`Successfully set the modlog to **${modlogchannel.name}** <:ayo_approve:909854401311678474>`)
  } else if (!data) {
  
    let newData = new modlogSchema({
      Modlog: modlogchannel.id,
      GuildID: message.guild.id,
    });
    newData.save();

    message.channel.send(`Successfully set the modlog to **${modlogchannel.name}** <:ayo_approve:909854401311678474>`)
   }
  }

  if (args[0] === 'disable') {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)

  const data = await modlogSchema.findOne({
    GuildID: message.guild.id,
  });

  if (data) {
    await modlogSchema.findOneAndRemove({
      GuildID: message.guild.id,
    });

  message.channel.send('Successfully disabled modlog <:ayo_approve:909854401311678474>')
  }
  }
}

module.exports.config = {
  name: "modlog",
  aliases: [],
  description: 'Views how to setup modlog',
  parameters: '',
  permissions: 'ADMINISTRATOR',
  syntax: 'modlog [command]',
  example: 'modlog disable'
}