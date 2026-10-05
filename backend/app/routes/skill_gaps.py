from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    User,
    UserSkill,
    Skill,
    Career,
    CareerSkill,
    Prediction,
    SkillGap
)

router = APIRouter(prefix="/skill-gaps", tags=["Skill Gap"])


@router.get("/{user_id}")
def get_skill_gaps(
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

    prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=400,
            detail="Career prediction not found. Run prediction first."
        )

    career = db.query(Career).filter(
        Career.name == prediction.predicted_career
    ).first()

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Predicted career not found"
        )

    user_skills = db.query(UserSkill).filter(
        UserSkill.user_id == user_id
    ).all()

    user_skill_map = {
        item.skill_id: item.proficiency
        for item in user_skills
    }

    required_skills = (
        db.query(Skill, CareerSkill.importance)
        .join(
            CareerSkill,
            CareerSkill.skill_id == Skill.id
        )
        .filter(
            CareerSkill.career_id == career.id
        )
        .order_by(Skill.name)
        .all()
    )

    gaps = []

    for skill, importance in required_skills:
        current_level = user_skill_map.get(skill.id, 0)
        required_level = 3
        gap = max(0, required_level - current_level)

        existing = db.query(SkillGap).filter(
            SkillGap.user_id == user_id,
            SkillGap.career_id == career.id,
            SkillGap.skill_id == skill.id
        ).first()

        if existing:
            existing.current_level = current_level
            existing.required_level = required_level
            existing.gap = gap
        else:
            db.add(
                SkillGap(
                    user_id=user_id,
                    career_id=career.id,
                    skill_id=skill.id,
                    current_level=current_level,
                    required_level=required_level,
                    gap=gap
                )
            )

        if current_level == 0:
            status = "Missing"
        elif gap > 0:
            status = "Needs Improvement"
        else:
            status = "Ready"

        gaps.append({
            "skill": skill.name,
            "category": skill.category,
            "current_level": current_level,
            "required_level": required_level,
            "gap": gap,
            "status": status
        })

    db.commit()

    return {
        "user_id": user_id,
        "career": career.name,
        "gaps": gaps
    }
