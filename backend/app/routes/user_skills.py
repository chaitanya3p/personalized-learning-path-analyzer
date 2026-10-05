from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Skill, UserSkill

router = APIRouter(prefix="/users", tags=["User Skills"])


@router.post("/{user_id}/skills")
def add_user_skill(
    user_id: int,
    skill_id: int,
    proficiency: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    if proficiency < 1 or proficiency > 5:
        raise HTTPException(
            status_code=400,
            detail="Proficiency must be between 1 and 5"
        )

    existing = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_id == skill_id
    ).first()

    if existing:
        existing.proficiency = proficiency
    else:
        db.add(
            UserSkill(
                user_id=user_id,
                skill_id=skill_id,
                proficiency=proficiency
            )
        )

    db.commit()

    return {
        "message": "User skill saved successfully",
        "user_id": user_id,
        "skill_id": skill_id,
        "skill": skill.name,
        "proficiency": proficiency
    }


@router.get("/{user_id}/skills")
def get_user_skills(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    results = (
        db.query(Skill, UserSkill.proficiency)
        .join(
            UserSkill,
            UserSkill.skill_id == Skill.id
        )
        .filter(
            UserSkill.user_id == user_id
        )
        .order_by(Skill.name)
        .all()
    )

    return {
        "user_id": user_id,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name,
                "category": skill.category,
                "proficiency": proficiency
            }
            for skill, proficiency in results
        ]
    }
