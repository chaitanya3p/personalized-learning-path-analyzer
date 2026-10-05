import { useState } from "react";
import api from "../services/api";

function ResumeUpload({ onAnalysisComplete }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [skillGap, setSkillGap] = useState(null);
    const [learningPath, setLearningPath] = useState(null);
    const [error, setError] = useState("");
    const [completing, setCompleting] = useState(null);

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a PDF resume");
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);
        setSkillGap(null);
        setLearningPath(null);

        try {
            const formData = new FormData();
            formData.append("file", file);

            const resumeResponse = await api.post(
                "/resume/upload/1",
                formData
            );

            setResult(resumeResponse.data);

            if (onAnalysisComplete) {
                onAnalysisComplete(resumeResponse.data);
            }

            const gapResponse = await api.get("/skill-gaps/1");
            setSkillGap(gapResponse.data);

            const pathResponse = await api.post("/learning-paths/1");
            setLearningPath(pathResponse.data);
        } catch (err) {
            console.error(err);

            setError(
                err.response?.data?.detail ||
                "Resume analysis failed"
            );
        } finally {
            setLoading(false);
        }
    };

    const handleComplete = async (itemId) => {
        setCompleting(itemId);
        setError("");

        try {
            const response = await api.patch(
                `/learning-paths/items/${itemId}/complete`
            );

            setLearningPath(response.data);
        } catch (err) {
            console.error(err);

            setError(
                err.response?.data?.detail ||
                "Could not update course progress"
            );
        } finally {
            setCompleting(null);
        }
    };

    const startCourse = (url) => {
        if (!url) {
            setError("Course URL is not available");
            return;
        }

        window.open(url, "_blank");
    };

    return (
        <div className="card resume-card">
            <h2>Resume Analyzer</h2>

            <p>
                Upload your resume to automatically detect skills,
                predict your career, analyze skill gaps, and generate
                a personalized course learning path.
            </p>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button
                className="resume-button"
                onClick={handleUpload}
                disabled={loading}
            >
                {loading
                    ? "Building Your Learning Path..."
                    : "Upload & Analyze Resume"}
            </button>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {result && (
                <div className="resume-result">
                    <h3>Resume Analysis</h3>

                    <p>
                        <strong>Skills Detected:</strong>{" "}
                        {result.total_skills}
                    </p>

                    <p>
                        <strong>Predicted Career:</strong>{" "}
                        {result.predicted_career}
                    </p>

                    <p>
                        <strong>Confidence:</strong>{" "}
                        {result.confidence}%
                    </p>

                    <h4>Detected Skills</h4>

                    <div className="skill-tags">
                        {result.detected_skills.map((skill) => (
                            <span
                                className="skill-tag"
                                key={skill.id}
                            >
                                {skill.name}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {skillGap && (
                <div className="resume-result">
                    <h3>Skill Gap Analysis</h3>

                    <p>
                        <strong>Target Career:</strong>{" "}
                        {skillGap.career}
                    </p>

                    <div className="gap-list">
                        {skillGap.gaps.map((gap) => (
                            <div
                                className="gap-row"
                                key={gap.skill}
                            >
                                <div>
                                    <strong>{gap.skill}</strong>
                                    <span>{gap.category}</span>
                                </div>

                                <div>
                                    Current: {gap.current_level}
                                </div>

                                <div>
                                    Required: {gap.required_level}
                                </div>

                                <div>
                                    Gap: {gap.gap}
                                </div>

                                <div
                                    className={
                                        gap.status === "Ready"
                                            ? "status-ready"
                                            : gap.status === "Missing"
                                            ? "status-missing"
                                            : "status-improvement"
                                    }
                                >
                                    {gap.status}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {learningPath && (
                <div className="resume-result">
                    <h3>Personalized Learning Path</h3>

                    <p>
                        <strong>Career:</strong>{" "}
                        {learningPath.career}
                    </p>

                    <div className="learning-progress">
                        <div className="progress-header">
                            <strong>Learning Progress</strong>

                            <strong>
                                {learningPath.completed_items || 0} /{" "}
                                {learningPath.total_items} completed
                            </strong>
                        </div>

                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{
                                    width: `${learningPath.progress || 0}%`
                                }}
                            />
                        </div>

                        <div className="progress-percentage">
                            {learningPath.progress || 0}%
                        </div>
                    </div>

                    <div className="learning-list">
                        {learningPath.items.map((item) => (
                            <div
                                className={
                                    item.status === "completed"
                                        ? "learning-item completed"
                                        : "learning-item"
                                }
                                key={item.id}
                            >
                                <div className="sequence">
                                    {item.sequence}
                                </div>

                                <div className="learning-content">
                                    <strong>{item.title}</strong>

                                    <span>Course</span>

                                    {item.course && (
                                        <small>
                                            {item.course.duration_hours} hours
                                        </small>
                                    )}
                                </div>

                                <div className="learning-actions">
                                    <button
                                        className="start-course-button"
                                        onClick={() =>
                                            startCourse(item.course?.url)
                                        }
                                    >
                                        Start Course
                                    </button>

                                    <button
                                        className={
                                            item.status === "completed"
                                                ? "complete-button completed-button"
                                                : "complete-button"
                                        }
                                        onClick={() =>
                                            item.status !== "completed" &&
                                            handleComplete(item.id)
                                        }
                                        disabled={
                                            item.status === "completed" ||
                                            completing === item.id
                                        }
                                    >
                                        {item.status === "completed"
                                            ? "Completed ?"
                                            : completing === item.id
                                            ? "Updating..."
                                            : "Mark Complete"}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResumeUpload;
