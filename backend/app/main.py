from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import (
    User,
    Skill,
    Career,
    UserSkill,
    CareerSkill,
    Course,
    Project,
    ProjectSkill,
    Prediction,
    SkillGap,
    LearningPath,
    LearningPathItem
)

from app.routes.skills import router as skills_router
from app.routes.careers import router as careers_router
from app.routes.courses import router as courses_router
from app.routes.projects import router as projects_router
from app.routes.users import router as users_router
from app.routes.user_skills import router as user_skills_router
from app.routes.predictions import router as predictions_router
from app.routes.skill_gaps import router as skill_gaps_router
from app.routes.learning_paths import router as learning_paths_router
from app.routes.resume import router as resume_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personalized Learning Path API",
    description="ML-powered skill gap and career recommendation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(skills_router)
app.include_router(careers_router)
app.include_router(courses_router)
app.include_router(projects_router)
app.include_router(users_router)
app.include_router(user_skills_router)
app.include_router(predictions_router)
app.include_router(skill_gaps_router)
app.include_router(learning_paths_router)
app.include_router(resume_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Personalized Learning Path API is running"
    }


@app.get("/db-test")
def database_test():
    try:
        with engine.connect():
            return {
                "status": "success",
                "message": "PostgreSQL connected successfully"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
