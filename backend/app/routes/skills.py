from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Skill

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/")
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).order_by(Skill.name).all()

    return [
        {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category
        }
        for skill in skills
    ]
