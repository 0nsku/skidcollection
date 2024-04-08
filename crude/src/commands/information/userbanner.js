const { MessageEmbed } = require("discord.js")
const axios = require("axios")
const { token } = require('../../../config.json')

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0]) || message.author;
    
  axios.get(`https://discord.com/api/users/${user.id}`, {
    headers: {
      Authorization: `Bot ${token}`
    },
  })
  .then((res) => {
    const { banner } = res.data;

    if (banner) {
      const extension = banner.startsWith("a_") ? ".gif" : ".png";
      const url = `https://cdn.discordapp.com/banners/${user.id}/${banner}${extension}?size=2048`;

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor(`${user.tag}`, user.displayAvatarURL({ dynamic: true }))
      .setImage(url)
        
      message.channel.send({ embeds: [embed] })
    } else {
      message.channel.send(`This user doesn't have a banner <:ayo_deny:909854484774125588>`)
    }
  })
}

module.exports.config = {
  name: "userbanner",
  aliases: ['ubanner'],
  description: 'shows mentioned users profile banner',
  parameters: 'user',
  permissions: '',
  syntax: 'ubanner [user]',
  example: 'ubanner @vayo'
}