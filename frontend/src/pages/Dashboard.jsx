import { useEffect, useState } from "react";
import api from "../services/api";
import ResumeUpload from "../components/ResumeUpload";
import SkillCategories from "../components/SkillCategories";

function Dashboard() {
    const [skills, setSkills] = useState([]);
const [skillSearch, setSkillSearch] = useState("");
    const [selectedSkills, setSelectedSkills] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(null);
    const [predicting, setPredicting] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [completing, setCompleting] = useState(null);
    const [message, setMessage] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [skillGaps, setSkillGaps] = useState(null);
    const [learningPath, setLearningPath] = useState(null);

    const userId = 1;

    const getResourceUrl = (item) => {
        if (item?.course?.url) {
            return item.course.url;
        }

        return null;
    };
    useEffect(() => {
        api.get("/skills/")
            .then((response) => {
                setSkills(response.data);
            })
            .catch((error) => {
                console.error(error);
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    const handleProficiencyChange = (skillId, value) => {
        setSelectedSkills((previous) => ({
            ...previous,
            [skillId]: Number(value)
        }));
    };

    const saveSkill = async (skillId) => {
        const proficiency = selectedSkills[skillId] || 1;

        setSaving(skillId);
        setMessage("");

        try {
            await api.post(
                `/users/${userId}/skills`,
                null,
                {
                    params: {
                        skill_id: skillId,
                        proficiency: proficiency
                    }
                }
            );

            setMessage("Skill saved successfully.");
        } catch (error) {
            console.error(error);
            setMessage("Failed to save skill.");
        } finally {
            setSaving(null);
        }
    };

    const predictCareer = async () => {
        setPredicting(true);
        setMessage("");
        setPrediction(null);
        setSkillGaps(null);
        setLearningPath(null);

        try {
            const response = await api.post(`/predictions/${userId}`);
            setPrediction(response.data);
        } catch (error) {
            console.error(error);
            setMessage(
                error.response?.data?.detail ||
                "Career prediction failed."
            );
        } finally {
            setPredicting(false);
        }
    };

    const analyzeSkillGap = async () => {
        setAnalyzing(true);
        setMessage("");

        try {
            const response = await api.get(`/skill-gaps/${userId}`);
            setSkillGaps(response.data);
        } catch (error) {
            console.error(error);
            setMessage(
                error.response?.data?.detail ||
                "Skill gap analysis failed."
            );
        } finally {
            setAnalyzing(false);
        }
    };

    const generateLearningPath = async () => {
        setGenerating(true);
        setMessage("");

        try {
            const response = await api.post(`/learning-paths/${userId}`);
            setLearningPath(response.data);
        } catch (error) {
            console.error(error);
            setMessage(
                error.response?.data?.detail ||
                "Learning path generation failed."
            );
        } finally {
            setGenerating(false);
        }
    };

    const loadLearningPath = async () => {
        try {
            const response = await api.get(`/learning-paths/${userId}`);
            setLearningPath(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    const completeItem = async (itemId) => {
        setCompleting(itemId);
        setMessage("");

        try {
            await api.patch(
                `/learning-paths/items/${itemId}/complete`
            );

            await loadLearningPath();

            setMessage("Learning item completed successfully.");
        } catch (error) {
            console.error(error);
            setMessage(
                error.response?.data?.detail ||
                "Failed to complete learning item."
            );
        } finally {
            setCompleting(null);
        }
    };

    return (
        <div className="dashboard">
            <h1>Personalized Learning Path</h1>

            <p>
                Select your skills and set your proficiency level.
            </p>

            {message && (
                <div className="message">
                    {message}
                </div>
            )}

            <ResumeUpload onAnalysisComplete={setPrediction} />

            <div className="card">
                <h2>Your Skills</h2>

                <input
                    type="text"
                    className="skill-search"
                    placeholder="Search skills..."
                    value={skillSearch}
                    onChange={(event) => setSkillSearch(event.target.value)}
                />

                <div className="proficiency-legend">
                    <strong>Proficiency Levels:</strong>
                    <div className="proficiency-levels">
                        <span className="proficiency-level">1 - Beginner</span>
                        <span className="proficiency-level">2 - Basic</span>
                        <span className="proficiency-level">3 - Intermediate</span>
                        <span className="proficiency-level">4 - Advanced</span>
                        <span className="proficiency-level">5 - Expert</span>
                    </div>
                </div>



                {loading ? (
                    <p>Loading skills...</p>
                ) : (
                    <SkillCategories
                        skills={skills}
                        selectedSkills={selectedSkills}
                        saving={saving}
                        handleProficiencyChange={handleProficiencyChange}
                        saveSkill={saveSkill}
                        skillSearch={skillSearch}
                    />
                )}

                <button
                    className="predict-button"
                    onClick={predictCareer}
                    disabled={predicting}
                >
                    {predicting
                        ? "Predicting..."
                        : "Predict My Career"}
                </button>
            </div>

            {prediction && (
                <div className="card prediction-card">
                    <h2>Career Prediction</h2>

                    <h3>{prediction.predicted_career}</h3>

                    <p>
                        Confidence: {prediction.confidence}%
                    </p>

                    <p>
                        Skills used: {(prediction.skills_used || prediction.detected_skills || []).length}
                    </p>

                    <button
                        className="analyze-button"
                        onClick={analyzeSkillGap}
                        disabled={analyzing}
                    >
                        {analyzing
                            ? "Analyzing..."
                            : "Analyze Skill Gap"}
                    </button>
                </div>
            )}

            {skillGaps && (
                <div className="card gap-card">
                    <h2>Skill Gap Analysis</h2>

                    <p>
                        Target Career:{" "}
                        <strong>{skillGaps.career}</strong>
                    </p>

                    <div className="gap-list">
                        {skillGaps.gaps.map((gap) => (
                            <div
                                className="gap-row"
                                key={gap.skill}
                            >
                                <div>
                                    <strong>{gap.skill}</strong>
                                    <span>
                                        {gap.category ||
                                            "Technical Skill"}
                                    </span>
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

                    <button
                        className="learning-button"
                        onClick={generateLearningPath}
                        disabled={generating}
                    >
                        {generating
                            ? "Generating Learning Path..."
                            : "Generate Personalized Learning Path"}
                    </button>
                </div>
            )}

            {learningPath && (
                <div className="card learning-card">
                    <h2>Personalized Learning Path</h2>

                    <p>
                        Career:{" "}
                        <strong>
                            {learningPath.career || "Data Scientist"}
                        </strong>
                    </p>

                    <div className="progress-section">
                        <div className="progress-header">
                            <strong>Learning Progress</strong>
                            <span>
                                {learningPath.progress || 0}%
                            </span>
                        </div>

                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{
                                    width: `${learningPath.progress || 0}%`
                                }}
                            />
                        </div>

                        <p>
                            {learningPath.completed_items || 0} of{" "}
                            {learningPath.total_items ||
                                learningPath.items.length}{" "}
                            completed
                        </p>
                    </div>

                    <div className="learning-list">
                        {learningPath.items.map((item) => {
                            const resourceUrl = getResourceUrl(item);

                            return (
                                <div
                                    className={`learning-item ${
                                        item.status === "completed"
                                            ? "completed-item"
                                            : ""
                                    }`}
                                    key={item.id}
                                >
                                    <div className="sequence">
                                        {item.sequence}
                                    </div>

                                    <div>
                                        <strong>{item.title}</strong>

                                        <span>
                                            {item.type === "course"
                                                ? "Course"
                                                : "Project"}
                                        </span>
                                    </div>

                                    <div className="learning-actions">
                                        {item.course?.url && (
    <a
        className="resource-button"
        href={item.course.url}
        target="_blank"
        rel="noopener noreferrer"
    >
        Start Course
    </a>
)}

                                        {item.status === "completed" ? (
                                            <div className="completed">
                                                Completed
                                            </div>
                                        ) : (
                                            <button
                                                className="complete-button"
                                                onClick={() =>
                                                    completeItem(item.id)
                                                }
                                                disabled={
                                                    completing === item.id
                                                }
                                            >
                                                {completing === item.id
                                                    ? "Updating..."
                                                    : "Mark Complete"}
                                            </button>
                                        )}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}

export default Dashboard;


















