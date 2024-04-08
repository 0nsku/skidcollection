const mongoose = require("mongoose")

const modlogSchema = new mongoose.Schema({
  Modlog: String,
  GuildID: String,
});

module.exports = mongoose.model("modlog", modlogSchema)