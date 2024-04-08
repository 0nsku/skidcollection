const { MessageEmbed, Collection } = require("discord.js")
const messagelogSchema = require('./../database/messagelog')
const snipes = new Collection();

module.exports = async (client, message) => {

  messagelogSchema.findOne({ GuildID: message.guild.id }, async function(err, client) {
    if (client) {

      snipes.set(message.channel.id, message)

      const data = await messagelogSchema.findOne({
        GuildID: message.guild.id,
      });

      const channel = message.guild.channels.cache.get(data.Messagelog)

      if (!channel) return;

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor(message.author.tag, message.author.displayAvatarURL({ dynamic: true }))
      .setDescription(`**Message deleted in**: ${message.channel}\n**Content**: ${message.content ? message.content : "None"}
      `)
      .setTimestamp()

      channel.send({ embeds: [embed] }).catch(err => console.log(err))

    } else if (!client) {
      //console.log(`Anti Nuke Log isn't on in ${member.guild.name}`)
    }
  })
}