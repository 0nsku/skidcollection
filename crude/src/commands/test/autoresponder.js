const { MessageEmbed, Permissions } = require("discord.js");
const { color, botprefix } = require('../../../config.json')
const prefixSchema = require("../../database/prefix");
const autoresponderSchema = require("../../database/autoresponder/trigger");

module.exports.run = async (client, message, args) => {

  const prefixData = await prefixSchema.findOne({
    GuildID: message.guild.id,
  }).catch(err => console.log(err))

  if (prefixData) {
    var guildprefix = prefixData.Prefix
  } else if (!prefixData) {
    guildprefix = botprefix
  }

  if(!message.member.permissions.has(Permissions.FLAGS.MANAGE_GUILD)) return message.channel.send(`this command requires \`manage server\` permission`)

  if (!args[0]) {

    const embed = new MessageEmbed()

    .setColor(color)
    .setTitle(`${guildprefix}autoresponder`)
    .setDescription('automatically respond to specific triggers')
    .addFields(
    { name: 'subcommands', value: `${guildprefix}autoresponder add - add a response trigger\n${guildprefix}autoresponder clear - remove all autoresponders\n${guildprefix}autoresponder list - list all response triggers\n${guildprefix}autoresponder remove - remove a response trigger`, inline: false },
    { name: 'usage', value: `${guildprefix}autoresponder`, inline: false },
    { name: 'aliases', value: `ar, autoresponse, autorespond, trigger`, inline: false },
    )

    return message.channel.send({ embeds: [embed] })
  }

  if (args[0] === 'add') {

    const trigger = args[1]; 
    
    const response = args.slice(2).join(" ");

    const embed = new MessageEmbed()

    .setColor(color)
    .setTitle(`${guildprefix}autoresponder add`)
    .setDescription(`add a response trigger`)
    .addFields(
    { name: 'usage', value: `${guildprefix}autoresponder add "trigger" hello world`, inline: false },
    )

    if(!trigger) return message.channel.send({ embeds: [embed] });
    if(!response) return message.channel.send({ embeds: [embed] });

    const data = await autoresponderSchema.findOne({ GuildID: message.guild.id, Trigger: trigger });

    if (data) {
      message.channel.send(`an autoresponder for **${trigger}** already exists`)
    } else {

    const newData = new autoresponderSchema({
      GuildID: message.guild.id,
      Trigger: trigger,
      Response: response
    })
    
    await newData.save();

    message.channel.send(`created an autoresponder for **${trigger}** 👍`)
    } 
  }

  if (args[0] === 'clear') {

    const data = await autoresponderSchema.findOne({
      GuildID: message.guild.id,
    });

    if (data) {
      await autoresponderSchema.findOneAndRemove({
        GuildID: message.guild.id,
      });

    message.channel.send('removed all autoresponders 👍')
    }
  }

  if (args[0] === 'list') {

    const data = await autoresponderSchema.find({ GuildID: message.guild.id });
       
    if(!data) return message.channel.send('there are no autoresponders set up');

    const embed = new MessageEmbed()

    .setColor(color)
    .setTitle('autoresponders')
    .setDescription(data.map((cmd, i) => `${i + 1} — **${cmd.Trigger}**`).join('\n'))

    message.channel.send({ embeds: [embed] })
  }

  if (args[0] === 'remove') {

    const name = args[1];

    const embed = new MessageEmbed()

    .setColor(color)
    .setTitle(`${guildprefix}autoresponder remove`)
    .setDescription(`remove a response trigger`)
    .addFields(
    { name: 'usage', value: `${guildprefix}autoresponder remove [trigger]`, inline: false },
    )

    if(!name) return message.channel.send({ embeds: [embed] });

    const data = autoresponderSchema.findOne({ GuildID: message.guild.id, Trigger: name });

    if (data) {
      await autoresponderSchema.findOneAndRemove({
        GuildID: message.guild.id,
        Trigger: name
      });

      message.channel.send(`removed the autoresponder for **${name}** 👍`)

    } else {
      return message.channel.send(`no autoresponder for **${name}** exists`);
    }
  }
}

module.exports.config = {
  name: "autoresponder",
  aliases: ['create', 'trigger'],
}