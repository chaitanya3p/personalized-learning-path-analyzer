from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Career, CareerSkill, Skill

router = APIRouter(prefix="/careers", tags=["Careers"])


@router.get("/")
def get_careers(db: Session = Depends(get_db)):
    careers = db.query(Career).order_by(Career.name).all()

    return [
        {
            "id": career.id,
            "name": career.name,
            "description": career.description
        }
        for career in careers
    ]


@router.get("/{career_id}/skills")
def get_career_skills(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(
        Career.id == career_id
    ).first()

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    results = (
        db.query(Skill, CareerSkill.importance)
        .join(
            CareerSkill,
            CareerSkill.skill_id == Skill.id
        )
        .filter(
            CareerSkill.career_id == career_id
        )
        .order_by(Skill.name)
        .all()
    )

    return {
        "career": career.name,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "category": skill.category,
                "importance": importance
            }
            for skill, importance in results
        ]
    }
