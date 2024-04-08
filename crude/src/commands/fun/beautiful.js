const { MessageAttachment } = require("discord.js");
const DIG = require("discord-image-generation");

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0]) || message.member;

  const avatar = user.user.displayAvatarURL({ dynamic: false, format: 'png', size: 1024 });

  new DIG.Beautiful().getImage(avatar, 43);

  const img = await new DIG.Beautiful().getImage(avatar);

  const attach = new MessageAttachment(img, "beautiful.png");

  message.channel.send({ files: [attach] })
}

module.exports.config = {
  name: "beautiful",
  aliases: [],
  description: 'manipulates user avatar',
  parameters: 'user',
  permissions: '',
  syntax: 'beautiful [user]',
  example: 'beautiful @vayo'
}