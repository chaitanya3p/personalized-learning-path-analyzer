from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Course

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).order_by(Course.title).all()

    return [
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "provider": course.provider,
            "url": course.url,
            "difficulty": course.difficulty,
            "duration_hours": course.duration_hours
        }
        for course in courses
    ]
