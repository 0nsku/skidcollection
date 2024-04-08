const mongoose = require("mongoose")

const messagelogSchema = new mongoose.Schema({
  Messagelog: String,
  GuildID: String,
});

module.exports = mongoose.model("messagelog", messagelogSchema)