import re


SKILL_ALIASES = {
    "ml": "Machine Learning",
    "ai/ml": "Machine Learning",
    "machine learning": "Machine Learning",

    "dl": "Deep Learning",
    "deep learning": "Deep Learning",

    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",

    "oop": "Object Oriented Programming",
    "object oriented programming": "Object Oriented Programming",
    "object-oriented programming": "Object Oriented Programming",

    "js": "JavaScript",
    "javascript": "JavaScript",

    "ts": "TypeScript",
    "typescript": "TypeScript",

    "react.js": "React",
    "reactjs": "React",
    "react": "React",

    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "mongo": "MongoDB",
    "mongodb": "MongoDB",

    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",

    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",

    "pytorch": "PyTorch",

    "github": "GitHub",
    "git hub": "GitHub",

    "aws": "AWS",
    "amazon web services": "AWS",

    "azure": "Microsoft Azure",
    "microsoft azure": "Microsoft Azure",

    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",

    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",

    "api": "REST API",
    "rest api": "REST API",
    "restful api": "REST API"
}


def normalize_text(text):
    text = text.lower()
    text = text.replace("/", " ")
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text, skills):
    normalized_text = normalize_text(text)

    detected_names = set()

    for alias, canonical_name in SKILL_ALIASES.items():
        alias_pattern = re.escape(alias)

        if re.search(
            r"(?<![a-z0-9])" + alias_pattern + r"(?![a-z0-9])",
            normalized_text
        ):
            detected_names.add(canonical_name)

    for skill in skills:
        skill_name = skill.name.lower().strip()

        pattern = r"(?<![a-z0-9])" + re.escape(skill_name) + r"(?![a-z0-9])"

        if re.search(pattern, normalized_text):
            detected_names.add(skill.name)

    detected_skills = []

    for skill in skills:
        if skill.name in detected_names:
            detected_skills.append(skill)

    return detected_skills
