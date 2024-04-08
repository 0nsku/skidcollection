const mongoose = require('mongoose')
const { MessageEmbed } = require('discord.js')
const { mongooseConnectionString } = require('../../config.json')

module.exports = (client) => {

  console.log('Crude Online!')

  //const userCount = client.guilds.cache.map((guild) => guild.memberCount).reduce((p, c) => p + c, 0);

  const arrayOfStatus = [
    `$help | ${client.guilds.cache.size} servers`,
    `solo.to/crudebot`,
  ]

  let index = 0;
  setInterval(() => {
    if(index === arrayOfStatus.length) index = 0;
    const status = arrayOfStatus[index];
    client.user.setActivity(status, { type: 'STREAMING', url: 'https://www.twitch.tv/ayo', })
    index++;
  }, 10000)

  if(!mongooseConnectionString) return;
    
  mongoose.connect(mongooseConnectionString, {
      // useFindAndModify: true,
      useUnifiedTopology: true,
  })
}