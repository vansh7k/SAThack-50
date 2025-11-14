const express = require("express");
const multer = require("multer");
const cors = require("cors");
const axios = require("axios");
const FormData = require("form-data");

const app = express();
app.use(cors());
const upload = multer();

app.post("/api/analyze", upload.single("resume"), async (req, res) => {
    try {
        const { role } = req.body;
        const file = req.file;

        if (!file) {
            return res.status(400).json({ error: "No file uploaded" });
        }

        console.log("Forwarding to Flask:", { filename: file.originalname, role });

        // Forward to Python AI service (Flask)
        const form = new FormData();
        form.append('resume', Buffer.from(file.buffer), { filename: file.originalname });
        form.append('role', role);

        const flaskRes = await axios.post(
            "http://localhost:5001/analyze",
            form,
            {
                headers: form.getHeaders()
            }
        );

        console.log("Flask response:", flaskRes.data);

        // Return the full analysis including courses and roadmap
        res.json({
            found_skills: flaskRes.data.found_skills,
            missing_skills: flaskRes.data.missing_skills,
            suggestions: flaskRes.data.suggestions,
            courses: flaskRes.data.courses,
            roadmap: flaskRes.data.roadmap
        });
    } catch (err) {
        console.error("Error analyzing resume:", err.response?.data || err.message);
        res.status(500).json({ error: err.message });
    }
});

app.listen(5000, () => {
    console.log('Backend listening on port 5000');
});
