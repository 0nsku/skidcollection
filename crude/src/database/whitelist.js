const mongoose = require("mongoose")

const whitelistSchema = mongoose.Schema({
  GuildID: String,
  UserID: String,
});

module.exports = mongoose.model("whitelist", whitelistSchema);