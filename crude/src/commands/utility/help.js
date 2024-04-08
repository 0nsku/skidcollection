const { pagination } = require("reconlx")
const { MessageEmbed } = require("discord.js");
const { botprefix, support, invite, upvote } = require('../../../config.json')
const prefixSchema = require("../../database/prefix");

module.exports.run = async (client, message, args) => {

  const command = client.commands.get(args[0]) || client.commands.get(client.aliases.get(args[0]));

  const prefixData = await prefixSchema.findOne({
    GuildID: message.guild.id,
  }).catch(err => console.log(err))

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

  if (command) {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle(`Command: ${command.config.name}`)
    .setDescription(`${command.config.description}`)
    .addFields(
    { name: 'Aliases', value: `${command.config.aliases.join('\`, \`') ? command.config.aliases : "None"}`, inline: true },
    { name: 'Parameters', value: `${command.config.parameters ? command.config.parameters : "None"}`, inline: true },
    { name: 'Permissions', value: `${command.config.permissions ? command.config.permissions : "None"}`, inline: true },
    { name: 'Usage', value: `\`\`\`Syntax: ${guildprefix}${command.config.syntax}\nExample: ${guildprefix}${command.config.example}\`\`\``, inline: false },
    )
    
    message.channel.send({ embeds: [embed] })
  } else if (args.length > 0) {
     
    return message.channel.send(`This command does not exist, use \`${guildprefix}help\` for the list of commands`)
  } else {

  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`Crude Help Menu`)
  .setDescription(`Crude, multi-purpose rich bot theme loaded with 70+ commands that includes antinuke, antiraid, autorole, and much more. Click through the buttons below to see the commands for each category.`)
  .addFields(
  { name: '<:ayo_help:909487068533624872> \`Need Help?\`', value: `Use \`${guildprefix}help [command]\` for more information.`, inline: false },
  { name: '<:ayo_folder:909668346394476574> \`Categories\`', value: '・Configuration\n・Fun\n・Information\n・Moderation\n・Utility', inline: false },
  { name: '<:ayo_link:909487190898253846> \`Useful Links\`', value: `[Support](${support})・[Invite](${invite})・[Upvote](${upvote})`, inline: false },
  )
  .setThumbnail(`${client.user.displayAvatarURL({size: 256, dynamic: true})}`)
  
  const embed1 = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`Crude Help Menu`)
  .addFields(
  { name: '<:ayo_antinuke:909593706934448138> \`Anti-Nuke Commands\`', value: '\`antinuke\`, \`antinuke channelenable\`, \`antinuke channeldisable\`, \`antinuke whitelist\`, \`antinuke unwhitelist\`, \`antinuke whitelisted\`, \`antinuke enable\`, \`antinuke disable\`, \`antinuke settings\`', inline: false },
  { name: '<:ayo_configuration:909487027253305384> \`Configuration Commands\`', value: '\`autorole\`, \`autorole enable\`, \`autorole disable\`, \`messagelog enable\`, \`messagelog disable\`, \`modlog enable\`, \`modlog disable\`, \`prefix\`, \`prefix enable\`, \`prefix disable\`', inline: false },
  )

  const embed2 = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`Crude Help Menu`)
  .addFields(
  { name: '<:ayo_fun:909487214176645151> \`Fun Commands\`', value: '\`8ball\`, \`affect\`, \`beautiful\`, \`blur\`, \`circle\`, \`coinflip\`, \`facepalm\`, \`gay\`, \`gayrate\`, \`invert\`, \`iq\`, \`penis\`, \`rate\`, \`rip\`, \`simprate\`, \`trash\`, \`treeshrate\`, \`triggered\`', inline: false },
  { name: '<:ayo_info:909487156131668028> \`Information Commands\`', value: '\`avatar\`, \`botinfo\`, \`guildbanner\`, \`guildicon\`, \`help\`, \`invite\`, \`membercount\`, \`ping\`, \`serverinfo\`, \`support\`, \`uptime\`, \`userbanner\`, \`userinfo\`, \`version\`', inline: false },
  )

  const embed3 = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`Crude Help Menu`)
  .addFields(
  { name: '<:ayo_mod:909487300705148988> \`Moderation Commands\`', value: '\`ban\`, \`kick\`, \`lock\`, \`mute\`, \`role\`, \`role add\`, \`role create\`, \`role remove\`, \`purge\`, \`unban\`, \`unlock\`, \`unmute\`', inline: false },
  { name: '<:ayo_utility:909487256992088114> \`Utility Commands\`', value: '\`bancount\`, \`calculator\`, \`color\`, \`commandcount\`, \`copyembed\`, \`credits\`, \`firstmessage\`, \`knownpoll\`, \`quickpoll\`, \`servercount\`, \`seticon\`, \`spotify\`, \`urban\`', inline: false },
  )

  const embeds = [
    embed,
    embed1,
    embed2,
    embed3,
  ];
  
  pagination({
    embeds: embeds,
    channel: message.channel,
    author: message.author,
    time: 60000,
    button: [
      {
        name: 'first',
        emoji: '<:icons_leftarrow:912125752944787476>',
        style: 'PRIMARY',
      },
      {
        name: 'next',
        emoji: '<:icons_rightarrow:912125772850954301>',
        style: 'PRIMARY',
      },
      {
        name: 'previous',
        emoji: '<:icons_leftarrow:912125752944787476>',
        style: 'PRIMARY',
      },
      {
        name: 'last',
        emoji: '<:icons_rightarrow:912125772850954301>',
        style: 'PRIMARY',
      },
    ]
  })
  }
}

module.exports.config = {
  name: "help",
  aliases: [],
  description: 'shows help embed',
  parameters: '',
  permissions: '',
  syntax: 'help',
  example: 'help'
}