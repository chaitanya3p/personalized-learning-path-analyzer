from app.database import SessionLocal
from app.models import Skill, Career, CareerSkill, Course, Project, ProjectSkill


skills_data = [
    ("Python", "Programming"),
    ("Java", "Programming"),
    ("C", "Programming"),
    ("C++", "Programming"),
    ("JavaScript", "Programming"),
    ("HTML", "Frontend"),
    ("CSS", "Frontend"),
    ("Bootstrap", "Frontend"),
    ("React", "Frontend"),
    ("FastAPI", "Backend"),
    ("Flask", "Backend"),
    ("Django", "Backend"),
    ("Node.js", "Backend"),
    ("Express.js", "Backend"),
    ("REST API", "Backend"),
    ("SQL", "Database"),
    ("MySQL", "Database"),
    ("PostgreSQL", "Database"),
    ("MongoDB", "Database"),
    ("SQLite", "Database"),
    ("NumPy", "Data Science"),
    ("Pandas", "Data Science"),
    ("Matplotlib", "Data Science"),
    ("Jupyter", "Data Science"),
    ("Data Analysis", "Data Science"),
    ("Statistics", "Data Science"),
    ("Machine Learning", "AI/ML"),
    ("Scikit-learn", "AI/ML"),
    ("Deep Learning", "AI/ML"),
    ("Natural Language Processing", "AI/ML"),
    ("TensorFlow", "AI/ML"),
    ("PyTorch", "AI/ML"),
    ("Data Structures", "CS Fundamentals"),
    ("Algorithms", "CS Fundamentals"),
    ("OOP", "CS Fundamentals"),
    ("DBMS", "CS Fundamentals"),
    ("Operating Systems", "CS Fundamentals"),
    ("Computer Networks", "CS Fundamentals"),
    ("Git", "Tools"),
    ("GitHub", "Tools"),
    ("VS Code", "Tools"),
    ("Postman", "Tools"),
    ("Docker", "Tools"),
    ("AWS", "Cloud")
]


careers_data = [
    ("Data Analyst", "Analyze data and create useful insights using Python, SQL and visualization tools."),
    ("Data Scientist", "Build data-driven models and solve business problems using statistics and machine learning."),
    ("Machine Learning Engineer", "Build and deploy machine learning systems using Python and ML frameworks."),
    ("AI Engineer", "Build AI applications using machine learning, deep learning and modern AI tools."),
    ("Backend Developer", "Build APIs, databases and server-side applications."),
    ("Full Stack Developer", "Build complete web applications using frontend and backend technologies."),
    ("Frontend Developer", "Build interactive and responsive web interfaces.")
]


career_skills = {
    "Data Analyst": ["Python", "SQL", "Pandas", "NumPy", "Data Analysis", "Statistics", "Matplotlib"],
    "Data Scientist": ["Python", "SQL", "Pandas", "NumPy", "Data Analysis", "Statistics", "Machine Learning", "Scikit-learn"],
    "Machine Learning Engineer": ["Python", "SQL", "Machine Learning", "Scikit-learn", "TensorFlow", "PyTorch", "Docker", "Git"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "Natural Language Processing", "TensorFlow", "PyTorch", "FastAPI"],
    "Backend Developer": ["Python", "FastAPI", "SQL", "PostgreSQL", "REST API", "Git", "Docker"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git", "REST API"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Git", "REST API"]
}


courses_data = [
    ("Python Basics for Beginners", "Learn Python syntax, variables, conditions, loops and functions.", "Programming", "Beginner", 8),
    ("Python Practice and Problem Solving", "Practice Python programming through beginner-friendly problems.", "Programming", "Beginner", 10),
    ("JavaScript Basics", "Learn variables, functions, arrays, objects and basic JavaScript programming.", "Web Development", "Beginner", 8),
    ("JavaScript DOM and Events", "Learn how JavaScript interacts with HTML pages and user actions.", "Web Development", "Beginner", 6),
    ("HTML Fundamentals", "Learn how to create web pages using HTML elements and forms.", "Frontend", "Beginner", 5),
    ("CSS Fundamentals", "Learn selectors, layouts, flexbox, grid and responsive styling.", "Frontend", "Beginner", 7),
    ("Bootstrap for Beginners", "Build responsive interfaces using Bootstrap components.", "Frontend", "Beginner", 5),
    ("React Fundamentals", "Learn React components, props, state and basic application structure.", "Frontend", "Beginner", 10),
    ("React Hooks and Components", "Learn useState, useEffect and reusable React components.", "Frontend", "Intermediate", 8),
    ("Build a React Project", "Create a practical React project using modern frontend concepts.", "Frontend", "Intermediate", 12),
    ("SQL Basics", "Learn tables, SELECT, WHERE, ORDER BY and basic SQL queries.", "Database", "Beginner", 6),
    ("SQL Queries and Joins", "Learn joins, grouping, aggregate functions and subqueries.", "Database", "Beginner", 8),
    ("MySQL for Students", "Practice database creation, queries and CRUD operations using MySQL.", "Database", "Beginner", 7),
    ("REST API Fundamentals", "Understand APIs, HTTP methods, requests, responses and JSON.", "Backend", "Beginner", 6),
    ("FastAPI Basics", "Build beginner-friendly APIs using FastAPI and Python.", "Backend", "Beginner", 8),
    ("FastAPI Database Project", "Build a FastAPI application connected to a database.", "Backend", "Intermediate", 12),
    ("Git Basics", "Learn repositories, commits, branches and basic Git commands.", "Tools", "Beginner", 4),
    ("GitHub for Students", "Learn repositories, README files, branches and collaboration.", "Tools", "Beginner", 5),
    ("NumPy Basics", "Learn arrays, indexing, slicing and numerical operations.", "Data Science", "Beginner", 6),
    ("Pandas Basics", "Learn Series, DataFrames and basic data manipulation.", "Data Science", "Beginner", 7),
    ("Data Cleaning with Pandas", "Learn how to clean, transform and prepare datasets.", "Data Science", "Intermediate", 8),
    ("Data Visualization with Matplotlib", "Create charts and visualizations from data.", "Data Science", "Beginner", 6),
    ("Statistics for Data Science", "Learn mean, median, probability and basic statistical concepts.", "Data Science", "Beginner", 8),
    ("Machine Learning Basics", "Understand supervised learning, training, testing and evaluation.", "AI/ML", "Beginner", 10),
    ("Machine Learning with Scikit-learn", "Build beginner-friendly machine learning models using Scikit-learn.", "AI/ML", "Intermediate", 12),
    ("Deep Learning Fundamentals", "Understand neural networks and basic deep learning concepts.", "AI/ML", "Intermediate", 12),
    ("Natural Language Processing Basics", "Learn text preprocessing and basic NLP concepts.", "AI/ML", "Intermediate", 10),
    ("Docker Basics", "Learn containers, images and basic Docker commands.", "DevOps", "Beginner", 5),
    ("Build and Deploy a Student Project", "Combine your skills into a practical portfolio project.", "Projects", "Intermediate", 15)
]


projects_data = [
    ("Student Result Management System", "Build a system to manage students, subjects, marks and results.", "Beginner"),
    ("Personalized Learning Path Predictor", "Build an ML-based system that predicts careers and recommends learning resources.", "Intermediate"),
    ("Sales Data Analysis Dashboard", "Analyze sales data and create useful visualizations.", "Beginner"),
    ("Machine Learning Prediction API", "Create an ML model and expose predictions through an API.", "Intermediate"),
    ("React Task Management App", "Build a task management application using React.", "Intermediate"),
    ("AI Chatbot", "Build a simple AI-powered chatbot application.", "Intermediate")
]


def seed():
    db = SessionLocal()

    try:
        for name, category in skills_data:
            existing = db.query(Skill).filter(Skill.name == name).first()
            if not existing:
                db.add(Skill(name=name, category=category))

        db.commit()

        for name, description in careers_data:
            existing = db.query(Career).filter(Career.name == name).first()
            if not existing:
                db.add(Career(name=name, description=description))

        db.commit()

        for career_name, skill_names in career_skills.items():
            career = db.query(Career).filter(
                Career.name == career_name
            ).first()

            for skill_name in skill_names:
                skill = db.query(Skill).filter(
                    Skill.name == skill_name
                ).first()

                if career and skill:
                    existing = db.query(CareerSkill).filter(
                        CareerSkill.career_id == career.id,
                        CareerSkill.skill_id == skill.id
                    ).first()

                    if not existing:
                        db.add(
                            CareerSkill(
                                career_id=career.id,
                                skill_id=skill.id,
                                importance=3
                            )
                        )

        db.commit()

        for title, description, provider, difficulty, duration in courses_data:
            existing = db.query(Course).filter(
                Course.title == title
            ).first()

            if not existing:
                db.add(
                    Course(
                        title=title,
                        description=description,
                        provider=provider,
                        difficulty=difficulty,
                        duration_hours=duration
                    )
                )

        db.commit()

        for title, description, difficulty in projects_data:
            existing = db.query(Project).filter(
                Project.title == title
            ).first()

            if not existing:
                db.add(
                    Project(
                        title=title,
                        description=description,
                        difficulty=difficulty
                    )
                )

        db.commit()

        print("Student-friendly course data seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()

