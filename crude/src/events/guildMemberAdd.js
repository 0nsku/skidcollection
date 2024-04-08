const { MessageEmbed }  = require("discord.js")
const { botprefix, invite } = require('./../../config.json')
const prefixSchema = require("./../database/prefix");
const whitelistSchema = require("./../database/whitelist");
const antilogSchema = require('./../database/antilog')
const antinukeSchema = require('./../database/antinuke')
const antiraidSchema = require('../database/antiraid')
const autoroleSchema = require('../database/autorole')

module.exports = async (client, member) => {

  const channel = member.guild.channels.cache.find(channel => channel.type === 'GUILD_TEXT' && channel.permissionsFor(client.user).has('SEND_MESSAGES'))

  if (member.user.bot) {

  const fetchedLogs = await member.guild.fetchAuditLogs({
	  limit: 1,
    type: "BOT_ADD",
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

  whitelistSchema.findOne({ GuildID: member.guild.id, UserID: executor.id }, async function(err, client) {
  if (client) {
  } else {

	member.guild.members.ban(executor.id).then(() => {

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('<:ayo_warning:909853615592726529> | Anti-Nuke Detected')
    .setDescription(`<:ayo_user:909855548399288320> **User**: <@${executor.id}>\n<:ayo_ban:909855911386959953> **Action**: Banned\n<:ayo_reason:909855408183730206> **Reason**: Bot Add
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

    } else if (!antinukedata) {

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Crude Anti-Nuke')
      .setDescription(`There was some unauthorized action taken place on your server, ${member.guild.name}. I couldn't stop the user from attacking your server because antinuke wasn't toggled on, run \`${guildprefix}antinuke enable\` in ${member.guild.name} to turn it on.`)
      .setTimestamp()

      
    }
  }

  antiraidSchema.findOne({ GuildID: member.guild.id }, async (err, data) => {
		const kickReason = 'Anti-raid'
		if (!data) return;
		if (data) {
      try {

        const userembed = new MessageEmbed()

        .setColor('#36393F')
        .setTitle('Crude Moderation')
        .setDescription(`
        <:ayo_user:909855548399288320> **Moderator**: ${message.author.tag}\n<:ayo_ban:909855911386959953> **Action**: Kicked from ${message.guild.name}\n<:ayo_reason:909855408183730206> **Reason**: ${kickReason}
        `)
       .setThumbnail(message.guild.iconURL({ dynamic: true }))
       .setTimestamp()

        member.send({ embeds: [userembed] })
        } catch(e){
          console.log(e)
        }
			member.kick(kickReason).then(() => {
        console.log('Kicked User for anti-raid on.')
        }).catch(() => {
        console.log(`Couldn't kick user for anti-raid.`)
      })
		}
	})

  autoroleSchema.findOne({ GuildID: member.guild.id }, async(err, data) => {
    if (!data) return;
    if(data) {
      const autorole = member.guild.roles.cache.get(data.RoleID)

      if (!autorole) return;

      if (!channel) return;

      member.roles.add(autorole).catch(() => {
      channel.send(`I could not set the autorole because it is higher than my role, autorole: ${autorole}.`).catch((err) => console.log(err))
      })
    } 
  })
}