const mongoose = require("mongoose")

const antiNukeSchema = new mongoose.Schema({
  GuildName: String,
  GuildID: String,
});

module.exports = mongoose.model("antinuke", antiNukeSchema)