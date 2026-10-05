from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, ProjectSkill, Skill

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.title).all()

    return [
        {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "difficulty": project.difficulty,
            "github_url": project.github_url
        }
        for project in projects
    ]


@router.get("/{project_id}/skills")
def get_project_skills(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    results = (
        db.query(Skill)
        .join(
            ProjectSkill,
            ProjectSkill.skill_id == Skill.id
        )
        .filter(
            ProjectSkill.project_id == project_id
        )
        .order_by(Skill.name)
        .all()
    )

    return {
        "project": project.title,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "category": skill.category
            }
            for skill in results
        ]
    }
