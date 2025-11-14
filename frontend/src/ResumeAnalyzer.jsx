import React, { useState } from 'react';
import axios from 'axios';

const roles = [
{ value: 'web_developer', label: 'Web Developer' },
{ value: 'data_analyst', label: 'Data Analyst' }
];

export default function ResumeAnalyzer({ user, onSignOut }) {
const [file, setFile] = useState(null);
const [role, setRole] = useState(roles[0].value);
const [result, setResult] = useState(null);
const [loading, setLoading] = useState(false);

const handleUpload = e => setFile(e.target.files[0]);

async function handleAnalyze() {
if (!file) { alert("Please upload a PDF."); return; }
setLoading(true);
const formData = new FormData();
formData.append("resume", file);
formData.append("role", role);
try {
    const { data } = await axios.post("http://localhost:5000/api/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" }
    });
    setResult(data);
} catch (err) {
    console.error("Error:", err);
    alert("Could not analyze resume. Try again!");
}
setLoading(false);
}

return (
<div className="bg-white p-8 rounded-lg shadow-md w-80">
    <div className="flex justify-between mb-2">
    <span className="text-sm text-gray-500">Welcome {user?.email}</span>
    <button onClick={onSignOut} className="text-xs text-red-500 hover:underline ml-2">Sign Out</button>
    </div>
    <h2 className="text-2xl font-bold text-blue-700 mb-2 text-center">SKILLBRIDGE</h2>
    <p className="text-sm text-center mb-4">AI Resume analyzer</p>
    <input
    type="file"
    accept="application/pdf"
    onChange={handleUpload}
    className="mb-3 w-full border p-2 rounded"
    />
    <select value={role} onChange={e => setRole(e.target.value)} className="mb-3 w-full border rounded p-2">
    {roles.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
    </select>
    <button
    className="bg-blue-500 text-white py-2 px-4 rounded mb-3 w-full hover:bg-blue-700 transition"
    onClick={handleAnalyze} disabled={loading}
    >
    {loading ? "Analyzing..." : "Analyze"}
    </button>
    {result && (
    <div className="space-y-4">
        {/* Found & Missing Skills */}
        <div className="flex gap-4">
        <div className="flex-1">
            <span className="font-semibold text-green-600 block mb-2">Found Skills:</span>
            <div className="flex flex-wrap gap-1">
            {result.found_skills.map(skill => (
                <span key={skill} className="bg-green-100 text-green-700 rounded px-2 py-1 text-xs">{skill}</span>
            ))}
            </div>
        </div>
        <div className="flex-1">
            <span className="font-semibold text-red-600 block mb-2">Missing Skills:</span>
            <div className="flex flex-wrap gap-1">
            {result.missing_skills.map(skill => (
                <span key={skill} className="bg-red-100 text-red-700 rounded px-2 py-1 text-xs">{skill}</span>
            ))}
            </div>
        </div>
        </div>

        {/* Suggestions */}
        {result.suggestions && result.suggestions.length > 0 && (
        <div className="bg-blue-50 p-3 rounded">
            <span className="font-semibold text-blue-700 block mb-2">Recommendations:</span>
            <ul className="text-sm text-blue-600 space-y-1">
            {result.suggestions.map((suggestion, idx) => (
                <li key={idx}>• {suggestion}</li>
            ))}
            </ul>
        </div>
        )}

        {/* Course Recommendations */}
        {result.courses && result.courses.length > 0 && (
        <div className="bg-purple-50 p-3 rounded">
            <span className="font-semibold text-purple-700 block mb-2">📚 Recommended Courses ({result.courses.length}):</span>
            <div className="space-y-2">
            {result.courses.map((course, idx) => (
                <div key={idx} className="bg-white p-3 rounded border border-purple-200 hover:shadow-md transition">
                <div className="flex justify-between items-start mb-2">
                    <p className="font-semibold text-sm text-purple-700">{course.skill}</p>
                    <span className="text-xs bg-purple-200 text-purple-700 px-2 py-1 rounded">{course.difficulty}</span>
                </div>
                <p className="text-xs text-gray-600 mb-2">{course.description}</p>
                <div className="flex justify-between items-center mb-2">
                    <span className="text-xs text-gray-500">⏱️ {course.duration}</span>
                </div>
                <div className="flex gap-2">
                    <a href={course.udemy} target="_blank" rel="noreferrer" 
                    className="flex-1 text-center text-xs bg-blue-500 text-white px-2 py-2 rounded hover:bg-blue-600 transition font-semibold">
                    Udemy
                    </a>
                    <a href={course.unacademy} target="_blank" rel="noreferrer" 
                    className="flex-1 text-center text-xs bg-orange-500 text-white px-2 py-2 rounded hover:bg-orange-600 transition font-semibold">
                    Unacademy
                    </a>
                </div>
                </div>
            ))}
            </div>
        </div>
        )}

        {/* Learning Roadmap */}
        {result.roadmap && result.roadmap.phase1 && (
        <div className="bg-green-50 p-3 rounded">
            <span className="font-semibold text-green-700 block mb-3">🗺️ Personalized Learning Roadmap</span>
            {["phase1", "phase2", "phase3"].map(phase => (
            <div key={phase} className="mb-2">
                <p className="font-semibold text-sm text-green-700">{result.roadmap[phase].title}</p>
                <p className="text-xs text-gray-600 mb-1">{result.roadmap[phase].description}</p>
                {result.roadmap[phase].skills_to_learn && result.roadmap[phase].skills_to_learn.length > 0 ? (
                <div className="flex flex-wrap gap-1">
                    {result.roadmap[phase].skills_to_learn.map(skill => (
                    <span key={skill} className="bg-yellow-200 text-yellow-800 rounded px-2 py-0.5 text-xs font-semibold">
                        {skill}
                    </span>
                    ))}
                </div>
                ) : (
                <span className="text-xs text-gray-500">All skills covered ✓</span>
                )}
            </div>
            ))}
        </div>
        )}
    </div>
    )}
    <p className="text-xs text-gray-500 mt-3">We compare your resume to your selected role and recommend courses for missing skills!</p>
</div>
);
}
