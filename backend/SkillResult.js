const mongoose = require("mongoose");

const SkillResultSchema = new mongoose.Schema({
    role: String,
    found_skills: [String],
    missing_skills: [String],
    suggestions: Object
});

module.exports = mongoose.model("SkillResult", SkillResultSchema);
