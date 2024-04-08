const { MessageAttachment } = require("discord.js");
const DIG = require("discord-image-generation");

module.exports.run = async (client, message, args) => {

  const user = message.mentions.members.first() || message.guild.members.cache.get(args[0]) || message.member;

  const avatar = user.user.displayAvatarURL({ dynamic: false, format: 'png', size: 1024 });

  new DIG.Facepalm().getImage(avatar, 43);

  const img = await new DIG.Facepalm().getImage(avatar);

  const attach = new MessageAttachment(img, "facepalm.png");

  message.channel.send({ files: [attach] })
}

module.exports.config = {
  name: "facepalm",
  aliases: [],
  description: 'manipulates user avatar',
  parameters: 'user',
  permissions: '',
  syntax: 'facepalm [user]',
  example: 'facepalm @vayo'
}