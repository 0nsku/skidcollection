const { MessageEmbed } = require("discord.js")
const moment = require("moment")

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0]) || message.member;

  let userroles = user.roles.cache
  .map((x) => x)
  .filter((z) => z.name !== "@everyone");

  if (userroles.length > 100) {
    userroles = "More than 100 roles";
  }

  if (userroles.length < 1) {
    userroles = "None";
  }
    
  const embed = new MessageEmbed()

  .setColor('#36393F')
  .setTitle(`User information for ${user.user.tag}`)
  .addFields(
  { name: '<:icons_calender:912518128725032960> Dates', value: `Registered: ${moment(user.user.createdTimestamp).format("MM/DD/YYYY, h:mm:ss a")}\nJoined: ${moment(user.joinedAt).format("MM/DD/YYYY, h:mm:ss a")}`, inline: false },
  { name: '<:icons_id:912146134028415016> ID', value: `${user.id}`, inline: false },
  { name: '<:ayo_user:909855548399288320> Roles', value: `${userroles}`, inline: false },
  )
  .setThumbnail(user.user.displayAvatarURL({size: 512, dynamic: true}))
  
  message.channel.send({ embeds: [embed] })
}

module.exports.config = {
  name: "userinfo",
  aliases: ['ui'],
  description: 'shows mentioned users info',
  parameters: 'user',
  permissions: '',
  syntax: 'ui [user]',
  example: 'ui @vayo'
}