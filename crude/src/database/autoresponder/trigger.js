const mongoose = require("mongoose")

const autoresponderSchema = new mongoose.Schema({
  GuildID: String,
  Trigger: String,
  Response: String
});

module.exports = mongoose.model("autoresponder", autoresponderSchema)