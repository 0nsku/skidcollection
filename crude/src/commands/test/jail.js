module.exports.run = async (client, message, args) => {

  const jailrole = message.guild.roles.cache.find(role => role.name === 'jailed');

  if(!jailrole) { 

    try {
      jailrole = await message.guild.roles.create({
        name: 'jailed',
        color: 'DEFAULT',
      })
      message.guild.channels.create('jailed', {
	      type: 'GUILD_TEXT',
	      permissionOverwrites: [
		      {
			      id: message.guild.id,
			      deny: [Permissions.FLAGS.VIEW_CHANNEL],
		      },
        ]
      })
  } catch (e) {
    console.log(e)
    }
  }




}

module.exports.config = {
  name: "jail",
  aliases: [],
}