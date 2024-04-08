const { MessageEmbed, Permissions } = require("discord.js");
const { botprefix } = require('../../../config.json')
const prefixSchema = require("../../database/prefix");
const modlogSchema = require('../../database/modlog')

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

      if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) return message.channel.send(`You're missing the \`manage roles\` permissions`)

      if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) return message.channel.send(`I'm missing the \`manage roles\` permissions`)

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setTitle('Getting started with Crude roles')
      .addFields(
      { name: '<:ayo_utility:909487256992088114> \`Setup\`', value: `The bot must be above the roles it's going to give users.`, inline: false },
      { name: '<:ayo_info:909487156131668028> \`Role Add\`', value: `You can add roles to specific users by using ${guildprefix}role add.`, inline: false },
      { name: '<:ayo_info:909487156131668028> \`Role Create\`', value: `You can create roles by using ${guildprefix}role create.`, inline: false },
      { name: '<:ayo_info:909487156131668028> \`Role Remove\`', value: `You can remove from specific users by using ${guildprefix}role remoe.`, inline: false },
      )
      .setFooter('Crude Configuration')
                    
      return message.channel.send({ embeds: [embed] })
    }

    if (args[0] === 'add') {

        const role = message.mentions.roles.first() || message.guild.roles.cache.get(args[1]);

        if (!user) return message.channel.send(`You didn't mention a user <:ayo_deny:909854484774125588>`)

        if (role.position >= message.member.roles.highest.position) return message.channel.send(`You cant role someone above you`)

        if (role.position >= client.user.roles.highest.position) return message.channel.send(`I cant role someone above me`)

        user.roles.add(role.id).then(() => {
            message.channel.send(`Added **${role.name}** to **${user.user.tag}**`)
        }).catch(() => {
            message.channel.send(`Couldn't role user <:ayo_deny:909854484774125588>`)
        })
    }

    if (args[0] === 'create') {

        const rolename = args.join(" ")

        if (!rolename) return message.channel.send('You need to provide a name')

        message.guild.roles.create({
          name: rolename,
        }).then(() => {
            message.channel.send(`Created a role named **${rolename.name}**`)
        }).catch(() => {
            message.channel.send(`Couldn't create role <:ayo_deny:909854484774125588>`)
        })

        const data = await modlogSchema.findOne({
            GuildID: message.guild.id,
          });
        
        if (!data) return;

        const modembed = new MessageEmbed()

        .setColor('#36393F')
        .setAuthor('Crude Moderation')
        .setDescription(`<:ayo_ban:909855911386959953> **Action**: Role Create`)
       .setFooter(`Moderator: ${message.author.tag}`)
       .setThumbnail(message.guild.iconURL({ dynamic: true }))
       .setTimestamp()
                
       const channel = message.guild.channels.cache.get(data.Modlog)
        
       if (!channel) return;
        
       channel.send({ embeds: [modembed] }).catch(err => console.log(err))
    }

    if (args[0] === 'remove') {

      const user = message.mentions.roles.first() || message.guild.roles.cache.get(args[1]);

      if (!user) return message.channel.send(`You didn't mention a user :thumbsdown:`)

      if (role.position >= message.member.roles.highest.position) return message.channel.send(`You cant remove that role someone above you`)

      if (role.position >= client.user.roles.highest.position) return message.channel.send(`I cant remove that role from someone above me`)

      user.roles.remove(role.id).then(() => {
          message.channel.send(`Removed **${role.name}** from **${user.user.tag}**`)
      }).catch(() => {
          message.channel.send(`Couldn't remove role from user <:ayo_deny:909854484774125588>`)
      })
    }

}

module.exports.config = {
  name: "role",
  aliases: ['r'],
  description: 'Views how to use roles',
  parameters: 'user, role',
  permissions: ['MANAGE ROLES'],
  syntax: 'role [command]',
  example: 'role create crude'
}