const { MessageEmbed, Permissions } = require("discord.js")
const prefixSchema = require("../../database/prefix");
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

  if (!args[0]) {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)
    
  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle('Getting started with Crude prefix')
  .addFields(
  { name: '<:ayo_utility:909487256992088114> \`Setup\`', value: `The bot must have administrator permissions for the prefix to work.`, inline: false },
  { name: '<:ayo_fun:909487214176645151> \`Prefix\`', value: `You first have to enable the autorole by using \`${guildprefix}autorole enable <mention/id>\`.\nYou can disable the autorole by using \`${guildprefix}autorole disable\`.`, inline: false },
  { name: '<:ayo_reason:909855408183730206> \`Current Prefixes\`', value: `Global Prefix: \`${botprefix}\`\nServer Prefix: \`${guildprefix}\``, inline: false },
  )
  .setFooter('Crude Configuration')
        
  return message.channel.send({ embeds: [embed] })
  }

  if (args[0] === 'enable') {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)

  const prefixname = args[1]

  if (!prefixname) return message.channel.send(`You did not provide a prefix <:ayo_deny:909854484774125588>`)

  if(args[1].length > 3) return message.channel.send('Prefix cant be over 3 letters')

  if(args[2]) return message.channel.send(`Can't have a spaced prefix.`)

  if (prefixdata) {
      await prefixSchema.findOneAndRemove({
        GuildID: message.guild.id,
      });

    let newData = new prefixSchema({
      Prefix: prefixname,
      GuildID: message.guild.id,
    });
    newData.save();

    message.channel.send(`Successully enabled prefix as **${prefixname}** <:ayo_approve:909854401311678474>`)
  } else if (!prefixdata) {

    let newData = new prefixSchema({
      Prefix: prefixname,
      GuildID: message.guild.id,
    });
    newData.save();

    message.channel.send(`Successully enabled prefix as **${prefixname}** <:ayo_approve:909854401311678474>`)
  }
  }

  if (args[0] === 'disable') {

  if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions.`)

  const data = await prefixSchema.findOne({
    GuildID: message.guild.id,
  });

  if (data) {
    await prefixSchema.findOneAndRemove({
      GuildID: message.guild.id,
    });
  }
  
  message.channel.send('Successfully disabled prefix <:ayo_approve:909854401311678474>')
  }
}

module.exports.config = {
  name: "prefix",
  aliases: [],
  description: 'Views how to setup prefix',
  parameters: '',
  permissions: 'ADMINISTRATOR',
  syntax: 'prefix [command]',
  example: 'prefix disable'
}