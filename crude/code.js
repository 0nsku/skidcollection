setInterval(() => {
    const randompfp = client.users.cache.map((user) => user.displayAvatarURL({ dynamic: true, format: "png", size: 2048 }))

    console.log(randompfp)

    const embed = new MessageEmbed()

    .setColor('#36393F')
    .setDescription(`random pfp`)
    .setImage(randompfp)

    //client.channels.cache.get("909861982038028288").send({ embeds: [embed] })
  }, 10000)