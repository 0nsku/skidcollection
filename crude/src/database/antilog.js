const mongoose = require("mongoose")

const antilogSchema = new mongoose.Schema({
  Antilog: String,
  GuildID: String,
});

module.exports = mongoose.model("antilog", antilogSchema)