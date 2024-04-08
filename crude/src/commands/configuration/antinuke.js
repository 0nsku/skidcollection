const { MessageEmbed, Permissions } = require("discord.js")
const prefixSchema = require("../../database/prefix");
const whitelistSchema = require("../../database/whitelist");
const antiNukeSchema = require('../../database/antinuke')
const antilogSchema = require('../../database/antilog')
const { botprefix } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[1])

  const antilogchannel = message.mentions.channels.first() || client.guilds.cache.get(message.guild.id).channels.cache.get(args[1])

  const antinukedata = await antiNukeSchema.findOne({
    GuildID: message.guild.id,
  });

  const antilogdata = await antilogSchema.findOne({
    GuildID: message.guild.id,
  });

  const prefixData = await prefixSchema.findOne({
    GuildID: message.guild.id,
  }).catch(err => console.log(err))

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

  const greencheck = '<:on:908397171466973195>'

  let antinuketoggle

  let antilogtoggle

  if (antinukedata) {
    antinuketoggle = '<:on:908397171466973195>'
  } else {
    antinuketoggle = '<:off:908397107235405825>'
  }

  if (antilogdata) {
    antilogtoggle = '<:on:908397171466973195>'
  } else {
    antilogtoggle = '<:off:908397107235405825>'
  }

  if (!args[0]) {

    if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command`)

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setTitle('Getting started with Crude Anti-Nuke')
    .addFields(
    { name: '<:ayo_utility:909487256992088114> Setup', value: `
    The bot must be above every role in the server for it to fully operate. Crude will watch over your server 24/7 and provides protection on the following below.`, inline: false},
    { name: '<\`Features\`', value: `
    ㆍAnti-Ban
    ㆍAnti-Kick
    ㆍAnti-Channel Creation/Deletion
    ㆍAnti-Role Creation/Deletion
    ㆍAnti-Role Update
    ㆍAnti-User Role Update`, inline: false },
    { name: '\`Whitelist / Unwhitelist\`', value: `To whitelist someone from being banned, \`use ${guildprefix}antinuke whitelist <@user/id>\`. To unwhitelist, you use \`${guildprefix}antinuke unwhitelist <@user/id>\`. Only the owner of the server can use this command.`, inline: false},
    { name: '\`Logs\`', value: `Crude comes with a log channel command where you can set a channel to log anytime the bot bans someone for attempting to raid/nuke. To set the log channel, use \`${guildprefix}antinuke channelenable <mention/id>\`.`, inline: false},
    )
    .setFooter('Crude Configuration')
  
    return message.channel.send({ embeds: [embed] })
  }

  if (args[0] === 'channelenable') {

    if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions`)

    if(antinukedata) {

      if (!antilogchannel || antilogchannel.type !== 'GUILD_TEXT') return message.channel.send(`You forgot to provide a channel`)

      if (antilogdata) {
        await antilogSchema.findOneAndRemove({
          GuildID: message.guild.id,
      });
    
      let newData = new antilogSchema({
        Antilog: antilogchannel.id,
        GuildID: message.guild.id,
      });
      newData.save();

      message.channel.send(`**${antilogchannel.name}** is now set as antinuke logs`)

      } else if (!antilogdata) {
      
       let newData = new antilogSchema({
         Antilog: antilogchannel.id,
         GuildID: message.guild.id,
       });
       newData.save();

       message.channel.send(`**${antilogchannel.name}** is now set as antinuke logs`)

      }
    } else if (!antinukedata) {

      const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
    }
  }

  if (args[0] === 'channeldisable') {

    if(!message.member.permissions.has(Permissions.FLAGS.ADMINISTRATOR)) return message.channel.send(`You're missing the \`administrator\` permissions`)

    if(antinukedata) {

    const data = await antilogSchema.findOne({
      GuildID: message.guild.id,
    });
  
    if (data) {
      await antilogSchema.findOneAndRemove({
        GuildID: message.guild.id,
    });

    message.channel.send('Antinuke logs have been disabled')
    } else if (!data) {
      message.channel.send('No antinuke logs exists')
    }

  } else if (!antinukedata) {

    const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
   }
  }

  // WHITELIST

  if (args[0] === 'whitelist') {

    if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command`)

    if(antinukedata) {

    if (!user) return message.channel.send(`You didn't mention a user <:ayo_deny:909854484774125588>`)

    if(user) {

        whitelistSchema.findOne({ GuildID: message.guild.id, UserID: user.id }, async function(err, client) {
          if (!client) {
            const newWhiteList = new whitelistSchema({
              GuildID: message.guild.id,
              UserID: user.id
          });  
      
          newWhiteList.save().catch(err => console.log(`[ERROR] ${err}`));

          const embed = new MessageEmbed()

          .setColor('#36393F')
          .setDescription(`<@${user.id}> is now whitelisted`)

          message.channel.send({ embeds: [embed] })

        } else {

            const embed = new MessageEmbed()

            .setColor('#36393F')
            .setDescription(`<@${user.id}> is already whitelisted`)

            message.channel.send({ embeds: [embed] })
        }
      })
    }
    } else if (!antinukedata) {

      const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
    }
   }

   // UNWHITELIST

   if (args[0] === 'unwhitelist') {

    if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command`)

    if(antinukedata) {

    if (!user) return message.channel.send(`You didn't mention a user <:ayo_deny:909854484774125588>`)
   
    if(user) {

        whitelistSchema.findOneAndDelete({ GuildID: message.guild.id, UserID: user.id }, async function(err, client) {
         if (!client) {
     
           const embed = new MessageEmbed()
     
           .setColor('#36393F')
           .setDescription(`<@${user.id}> not found on the database <:ayo_deny:909854484774125588>`)
         
           message.channel.send({ embeds: [embed] })

          } else {

            const embed = new MessageEmbed()
      
            .setColor('#36393F')
            .setDescription(`<@${user.id}> is now unwhitelisted`)
          
            message.channel.send({ embeds: [embed] })
        }
      })
    }
    } else if (!antinukedata) {

      const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
    }
   }

   // WHITELISTED

   if (args[0] === 'whitelisted') {

    if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command`)

    if(antinukedata) {

        whitelistSchema.find({ GuildID: message.guild.id }, function(err, guildID) {
        if (err) return console.log(err);
        let user = "";

        guildID.forEach(guild => {
        user += `<@${guild.UserID}>\n`;
        });
            
        const embed = new MessageEmbed()
          
        .setColor('#36393F')
        .setAuthor(`Whitelisted Users`)
        .setDescription(user.length ? `${user}` : "No users found")
        
        message.channel.send({ embeds: [embed] })
        })

    } else if (!antinukedata) {

      const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
     }
   }
   
   // ENABLE

   if (args[0] === 'enable') {

    if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command`)

    if(antinukedata) {

      message.channel.send(`Anti-Nuke toggle is currently enable, use \`${guildprefix}antinuke disable\``)

    } else if (!antinukedata) {

        const embed = new MessageEmbed()

        .setColor('#36393F')
        .setDescription(`Toggled antinuke on`)
     
        message.channel.send({ embeds: [embed] })

      let newData = new antiNukeSchema({
          GuildID: message.guild.id,
      });
      newData.save();
     }
    }

    // DISABLE

    if (args[0] === 'disable') {

     if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command`)

     if(antinukedata) {

        await antiNukeSchema.findOneAndRemove({
            GuildID: message.guild.id,
        });

        const embed = new MessageEmbed()

        .setColor('#36393F')
        .setDescription(`Toggled antinuke off`)
     
        message.channel.send({ embeds: [embed] })

     } else if (!antinukedata) {

      const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
      }
    }

    if (args[0] === 'settings') {

    if (message.author.id !== message.guild.ownerId) return message.channel.send(`Only the guild owner can use this command.`)

    if(antinukedata) {

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setTitle(`<:ayo_settings:909972377620844584> | ${message.guild.name} Settings`)
      .addFields(
      { name: '\`Anti-Nuke\`', value: `${antinuketoggle}`, inline: true },
      { name: '\`Anti-Logs\`', value: `${antilogtoggle}`, inline: true },
      { name: '\`Anti-Ban\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Channel Create\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Channel Delete\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Bot Add\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Permission Update\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Kick\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Role Create\`', value: `${greencheck}`, inline: true },
      { name: '\`Anti-Role Delete\`', value: `${greencheck}`, inline: true },
      )
      .setFooter('Crude Anti-Nuke')

      message.channel.send({ embeds: [embed] })

    } else if (!antinukedata) {

      const embed = new MessageEmbed()
      
      .setColor('#36393F')
      .setDescription(`Anti-Nuke toggle is currently disabled, use \`${guildprefix}antinuke enable\``)
 
      message.channel.send({ embeds: [embed] })
      }
    }
}
    
module.exports.config = {
  name: "antinuke",
  aliases: ['an'],
  description: 'Views how to setup anti-nuke',
  parameters: '',
  permissions: ['ADMINISTRATOR', 'OWNER'],
  syntax: 'antinuke [command]',
  example: 'antinuke whitelist'
}