const { MessageEmbed, Permissions } = require("discord.js")

module.exports.run = async (client, message, args) => {

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_MESSAGES)) return message.channel.send(`You're missing the \`manage messages\` permissions`)

  if(!message.guild.me.permissions.has(Permissions.FLAGS.MANAGE_MESSAGES)) return message.channel.send(`I'm missing the \`manage messages\` permissions`)

  if (!args[0]) return message.channel.send('Provide a message id')

  try {

    const embed = await message.channel.messages.fetch(args[0])

    if (!embed) return message.channel.send('provide a message id')

    if (!embed.embeds || !embed.embeds.length) return message.channel.send(`i couldn't find that message`)

    const json = toJSON(embed.content, embed.embeds[0])

    const copyembed = new MessageEmbed()

    .setColor('#36393F')
    .setDescription(`the current embed message:\n\`\`\`json\n${json}\`\`\``)
    .setFooter('successfully copied the embed code')

    message.channel.send({ embeds: [copyembed] })

  } catch (error) {

    if (error.code === 404) {
      message.channel.send(`i couldn't copy that embed url`)
    } else {
      return message.channel.send(`i couldn't copy that embed url`)
    }
  }

  function toJSON(content, messageEmbed) {
	let json = {};
	if (content)
		json.content = content;
	json.embed = {};
	if (messageEmbed.title)
		json.embed.title = messageEmbed.title;
	if (messageEmbed.description)
		json.embed.description = messageEmbed.description;
	if (messageEmbed.url)
		json.embed.url = messageEmbed.url;
	if (messageEmbed.color)
		json.embed.color = messageEmbed.color;
	if (messageEmbed.timestamp)
		json.embed.timestamp = new Date(messageEmbed.timestamp);
	if (messageEmbed.footer) {
		json.embed.footer = {};
		if (messageEmbed.footer.iconURL)
			json.embed.footer.icon_url = messageEmbed.footer.iconURL;
		if (messageEmbed.footer.text)
			json.embed.footer.text = messageEmbed.footer.text;
	}
	if (messageEmbed.thumbnail) {
		json.embed.thumbnail = {};
		if (messageEmbed.thumbnail.url)
			json.embed.thumbnail.url = messageEmbed.thumbnail.url;
	}
	if (messageEmbed.image) {
		json.embed.image = {};
		if (messageEmbed.image.url)
			json.embed.image.url = messageEmbed.image.url;
	}
	if (messageEmbed.author) {
		json.embed.author = {};
		if (messageEmbed.author.url)
			json.embed.author.url = messageEmbed.author.url;
		if (messageEmbed.author.name)
			json.embed.author.name = messageEmbed.author.name;
		if (messageEmbed.author.iconURL)
			json.embed.author.icon_url = messageEmbed.author.iconURL;
	}
	if (messageEmbed.fields)
		json.embed.fields = messageEmbed.fields;
	return JSON.stringify(json, undefined, 2);
}
}

module.exports.config = {
  name: "copyembed",
  aliases: [],
}