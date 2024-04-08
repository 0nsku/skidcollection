module.exports.run = async (client, message, args) => {

  const answers = [
    'heads',
    'tails',
  ];
    
  const randomanswers = answers[Math.floor(Math.random() * answers.length)];
        
  message.channel.send(`<@${message.author.id}>, you flipped ${randomanswers}`)
}

module.exports.config = {
  name: "coinflip",
  aliases: [],
  description: 'flips coin',
  parameters: 'none',
  permissions: '',
  syntax: 'coinflip',
  example: 'coinflip'
}