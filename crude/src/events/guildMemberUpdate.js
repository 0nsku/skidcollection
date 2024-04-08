const { MessageEmbed, Permissions } = require("discord.js")
const { botprefix } = require('./../../config.json')
const prefixSchema = require("./../database/prefix");
const whitelistSchema = require("./../database/whitelist");
const antilogSchema = require('./../database/antilog')
const antinukeSchema = require('./../database/antinuke')

module.exports = async (client, member, newRole) => {

  const fetchedLogs = await member.guild.fetchAuditLogs({
	  limit: 1,
    type: "MEMBER_ROLE_UPDATE",
  }).catch((err) => {
  })
  
  if (!fetchedLogs) return;

  const owner = await member.guild.fetchOwner()

  const channellog = fetchedLogs.entries.first();

  if (!channellog) return;

  const { executor } = channellog;

  const data = await antilogSchema.findOne({
    GuildID: member.guild.id,
  });

  const antinukedata = await antinukeSchema.findOne({
    GuildID: member.guild.id,
  });

  const prefixData = await prefixSchema.findOne({
    GuildID: member.guild.id,
  });

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

  if (executor.id == member.guild.ownerId) return;
  if (executor.id == client.user.id) return;

  if(antinukedata) {

  if (!member.permissions.has(Permissions.FLAGS.ADMINISTRATOR) && newRole.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) {

  whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
  if (client) {
  } else {

	member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`ADMINISTRATOR\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })

    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })  
    })
    }
    })
   
    } else if (!member.permissions.has(Permissions.FLAGS.BAN_MEMBERS) && newRole.permissions.has(Permissions.FLAGS.BAN_MEMBERS)) {

    whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
    if (client) {
    } else {

    member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`BAN MEMBERS\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })

    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })
    })
    }
    })

    } else if (!member.permissions.has(Permissions.FLAGS.KICK_MEMBERS) && newRole.permissions.has(Permissions.FLAGS.KICK_MEMBERS)) {

    whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
    if (client) {
    } else {

    member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`KICK MEMBERS\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })

    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })  
    })
    }
    })

    } else if (!member.permissions.has(Permissions.FLAGS.MANAGE_WEBHOOKS) && newRole.permissions.has(Permissions.FLAGS.MANAGE_WEBHOOKS)) {

    whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
    if (client) {
    } else {

    member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`MANAGE WEBHOOKS\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })
    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })
    })
    }
    })

    } else if (!member.permissions.has(Permissions.FLAGS.MANAGE_GUILD) && newRole.permissions.has(Permissions.FLAGS.MANAGE_GUILD)) {

    whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
    if (client) {
    } else {

    member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`MANAGE GUILD\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })
    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })  
    })
    }
    })

    } else if (!member.permissions.has(Permissions.FLAGS.MANAGE_ROLES) && newRole.permissions.has(Permissions.FLAGS.MANAGE_ROLES)) {

    whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
    if (client) {
    } else {

    member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`MANAGE ROLES\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })
    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    }) 
    })
    }
    })

    } else if (!member.permissions.has(Permissions.FLAGS.MANAGE_CHANNELS) && newRole.permissions.has(Permissions.FLAGS.MANAGE_CHANNELS)) {

    whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
    if (client) {
    } else {

    member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Member Role Update: \`MANAGE CHANNELS\`
    `)
    .setThumbnail(member.guild.iconURL({ dynamic: true }))
    .setFooter(`Crude Anti-Nuke`)
    .setTimestamp()

    antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [embed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })
    }).catch(() => {

      const nopermembed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`I was unable to ban <@${executor.id}> because they are higher than me, if you want me to fully monitor the server please move my role up.`)
      .setTimestamp()

      antilogSchema.findOne({ GuildID: member.guild.id }, async function(err, client) {
    if (client) {

      const channel = member.guild.channels.cache.get(data.Antilog)

      if (!channel) return;

      channel.send({ embeds: [nopermembed] })

    } else if (!client) {

      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
    })  
    })
    }
    })
    } 
    } else if (!antinukedata) {

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`There was some unauthorized action taken place on your server, ${member.guild.name}. I couldn't stop the user from attacking your server because antinuke wasn't toggled on, run \`${guildprefix}antinuke enable\` in ${member.guild.name} to turn it on.`)
      .setTimestamp()
  }
}