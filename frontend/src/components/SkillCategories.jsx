import { useState } from "react";

function SkillCategories({
    skills,
    selectedSkills,
    saving,
    handleProficiencyChange,
    saveSkill,
    skillSearch
}) {
    const [openCategory, setOpenCategory] = useState(null);

    const categories = {};
    const search = skillSearch.toLowerCase().trim();

    const filteredSkills = skills.filter((skill) =>
        skill.name.toLowerCase().includes(search)
    );

    filteredSkills.forEach((skill) => {
        const category = skill.category || "Other";

        if (!categories[category]) {
            categories[category] = [];
        }

        categories[category].push(skill);
    });

    const toggleCategory = (category) => {
        setOpenCategory(
            openCategory === category ? null : category
        );
    };

    return (
        <div className="skill-categories">
            {Object.entries(categories).map(([category, categorySkills]) => (
                <div className="skill-category" key={category}>
                    <button
                        className="category-header"
                        onClick={() => toggleCategory(category)}
                    >
                        <span>
                            {category} ({categorySkills.length} skills)
                        </span>
                        <span>
                            {openCategory === category ? "-" : "+"}
                        </span>
                    </button>

                    {openCategory === category && (
                        <div className="skill-list">
                            {categorySkills.map((skill) => {
                                const level = selectedSkills[skill.id] || 1;
                                const percentage = (level / 5) * 100;

                                return (
                                    <div className="skill-row" key={skill.id}>
                                        <div>
                                            <strong>{skill.name}</strong>
                                            <span>
                                                {skill.category || "Technical Skill"}
                                            </span>
                                        </div>

                                        <div className="proficiency-info">
                                            <span>{level}/5</span>
                                            <div className="proficiency-bar">
                                                <div
                                                    className="proficiency-fill"
                                                    style={{
                                                        width: `${percentage}%`
                                                    }}
                                                />
                                            </div>
                                        </div>

                                        <select
                                            value={level}
                                            onChange={(event) =>
                                                handleProficiencyChange(
                                                    skill.id,
                                                    event.target.value
                                                )
                                            }
                                        >
                                            <option value="1">1 - Beginner</option>
                                            <option value="2">2 - Basic</option>
                                            <option value="3">3 - Intermediate</option>
                                            <option value="4">4 - Advanced</option>
                                            <option value="5">5 - Expert</option>
                                        </select>

                                        <button
                                            onClick={() => saveSkill(skill.id)}
                                            disabled={saving === skill.id}
                                        >
                                            {saving === skill.id
                                                ? "Saving..."
                                                : "Save"}
                                        </button>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            ))}

            {filteredSkills.length === 0 && (
                <p>No skills found.</p>
            )}
        </div>
    );
}

export default SkillCategories;
