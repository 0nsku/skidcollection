const { MessageEmbed } = require("discord.js")
const convert = require('parse-ms');

module.exports.run = async (client, message, args) => {

  let user

  if (message.mentions.users.first())
  {
    
  user = message.mentions.members.first();

  } else {
    
  user = message.member;
  } 
  
  let status;
  if (user.presence.activities.length === 1) status = user.presence.activities[0];
  else if (user.presence.activities.length > 1) status = user.presence.activities[1];

  if (user.presence.activities.length === 0 || status.name !== "Spotify" && status.type !== "LISTENING") {
    return message.channel.send('User is not listening to spotify')
  }

  if (status !== null && status.type === "LISTENING" && status.name === "Spotify" && status.assets !== null) {

      let name = status.details,
      artist = status.state,
      album = status.assets.largeText

      timeStart = status.timestamps.start,
      timeEnd = status.timestamps.end,
      timeConvert = convert(timeEnd - timeStart);

      let minutes = timeConvert.minutes < 10 ? `0${timeConvert.minutes}` : timeConvert.minutes;
      let seconds = timeConvert.seconds < 10 ? `0${timeConvert.seconds}` : timeConvert.seconds;
      let time = `${minutes}:${seconds}`;

      const embed = new MessageEmbed()

      .setColor('#36393F')
      .setAuthor('Spotify', 'https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png')
      .addFields(
      { name: '<:ayo_user:909855548399288320> \`Artist\`', value: `${artist}`, inline: false },
      { name: '<:ayo_reason:909855408183730206> \`Song\`', value: `${name}`, inline: false },
      { name: '<:icons_queue:911739401208471673> \`Album\`', value: `${album}`, inline: false },
      )
      .setFooter(`Duration: ${time}`)
      .setThumbnail(`https://i.scdn.co/image/${status.assets.largeImage.slice(8)}`)
 
      return message.channel.send({ embeds: [embed] })
  }
}

module.exports.config = {
  name: "spotify",
  aliases: [],
  description: 'shows what specificed user is playing on spotify',
  parameters: 'user',
  permissions: '',
  syntax: 'spotify [user]',
  example: 'spotify @vayo'
}