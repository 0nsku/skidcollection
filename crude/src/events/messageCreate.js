const { Collection }  = require("discord.js")
const { botprefix } = require('../../config.json')
const prefixSchema = require("./../database/prefix");
const cooldowns = new Collection();

module.exports = async (client, message) => {

	const messageArray = message.content.split(' ');
	const cmd = messageArray[0];
	const args = messageArray.slice(1);

	if (message.author.bot || message.channel.type === 'dm') return;

  const prefixData = await prefixSchema.findOne({
    GuildID: message.guild.id,
  });

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

	if (message.content.match(new RegExp(`^<@!?${client.user.id}>( |)$`))) return message.channel.send(`prefix: \`${guildprefix}\``)
 
	if (!message.content.startsWith(guildprefix)) return;
  
	const commandfile = client.commands.get(cmd.slice(guildprefix.length).toString().toLowerCase()) || client.commands.get(client.aliases.get(cmd.slice(guildprefix.length).toString().toLowerCase()));;

  if (!commandfile) return message.channel.send(`This command does not exist, use \`${guildprefix}help\` for the list of commands`)
  
  if (!cooldowns.has(commandfile.name)) {
    cooldowns.set(commandfile.name, new Collection());
  }
            
  const now = Date.now();
  const timestamps = cooldowns.get(commandfile.name);
  const cooldownAmount = (commandfile.cooldown || 3) * 1000;
            
  if (timestamps.has(message.author.id)) {
    const expirationTime = timestamps.get(message.author.id) + cooldownAmount;
            
  if (now < expirationTime) {
    const timeLeft = (expirationTime - now) / 1000;
    return message.reply(`Wait **${timeLeft.toFixed(1)}** more seconds before using commands again`)
    }
   }
  timestamps.set(message.author.id, now);
  setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);

  if (commandfile) {
		commandfile.run(client, message, args);
	}
}