setInterval(() => {
    //const randompfp = client.users.cache.map((user) => user.displayAvatarURL({ dynamic: true, format: "png", size: 256 }))

    const randompfp = client.users.cache((user) => user.tag)

    //console.log(randompfp)

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setDescription(`random pfp`)
    .setImage(randompfp)

    const channel = client.channels.cache.get("909861342423441508")
    channel.send({ embeds: [embed] })
  }, 10000)