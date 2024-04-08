const mongoose = require("mongoose")

const antiraidSchema = new mongoose.Schema({
  GuildID: String,
});

module.exports = mongoose.model("antiraid", antiraidSchema)