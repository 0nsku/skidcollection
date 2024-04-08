const mongoose = require("mongoose")

const autoroleSchema = new mongoose.Schema({
  RoleID: String,
  GuildID: String,
});

module.exports = mongoose.model("autorole", autoroleSchema)