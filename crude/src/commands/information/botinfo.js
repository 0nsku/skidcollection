const { MessageEmbed } = require("discord.js")
const { jaylin, jayv, brando, commands } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const servercount = client.guilds.cache.size

  const usercount = client.guilds.cache.map((guild) => guild.memberCount).reduce((p, c) => p + c, 0);

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`Crude Bot Information`)
  .setDescription(`Developed by <@795386105901744200>`)
  .addFields(
  { name: '<:icons_globe:910983418366525451> \`Guilds\`', value: `${servercount} servers`, inline: true },
  { name: '<:ayo_reason:909855408183730206> \`Users\`', value: `${usercount} users`, inline: true },
  { name: '<:icons_cmd:910983578517659649> \`Commands\`', value: `${commands} cmds`, inline: true },
  { name: '<:icons_discordjs:910982035676495903> \`Library\`', value: `Discord.js`, inline: true },
  { name: '<:icons_nodejs:912512662624141433> \`Environment\`', value: `Node.js`, inline: true },
  { name: '<:icons_pings:911295687533150308> \`Ping\`', value: `${Math.round(client.ws.ping)}ms`, inline: true },
  )
  .setFooter('Crude/v13.2.0')
  .setThumbnail(`${client.user.displayAvatarURL({size: 256, dynamic: true})}`)
  
  message.channel.send({ embeds: [embed] })

}

module.exports.config = {
  name: "botinfo",
  aliases: ['about'],
  description: 'shows information about bot',
  parameters: '',
  permissions: '',
  syntax: 'botinfo',
  example: 'botinfo'
}