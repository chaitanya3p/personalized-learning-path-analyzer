from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    User,
    Career,
    Prediction,
    SkillGap,
    LearningPath,
    LearningPathItem,
    Course
)

router = APIRouter(
    prefix="/learning-paths",
    tags=["Learning Paths"]
)

SKILL_COURSE_MAP = {
    "Python": [
        "Python Basics for Beginners",
        "Python Practice and Problem Solving"
    ],
    "SQL": [
        "SQL Basics",
        "SQL Queries and Joins",
        "MySQL for Students"
    ],
    "Pandas": [
        "Pandas Basics",
        "Data Cleaning with Pandas"
    ],
    "NumPy": [
        "NumPy Basics"
    ],
    "Machine Learning": [
        "Machine Learning Basics",
        "Machine Learning with Scikit-learn"
    ],
    "Scikit-learn": [
        "Machine Learning with Scikit-learn"
    ],
    "Deep Learning": [
        "Deep Learning Fundamentals"
    ],
    "Natural Language Processing": [
        "Natural Language Processing Basics"
    ],
    "HTML": [
        "HTML Fundamentals"
    ],
    "CSS": [
        "CSS Fundamentals"
    ],
    "JavaScript": [
        "JavaScript Basics",
        "JavaScript DOM and Events"
    ],
    "React": [
        "React Fundamentals",
        "React Hooks and Components",
        "Build a React Project"
    ],
    "REST API": [
        "REST API Fundamentals"
    ],
    "FastAPI": [
        "FastAPI Basics",
        "FastAPI Database Project"
    ],
    "Git": [
        "Git Basics",
        "GitHub for Students"
    ],
    "GitHub": [
        "GitHub for Students"
    ],
    "Docker": [
        "Docker Basics"
    ],
    "Statistics": [
        "Statistics for Data Science"
    ],
    "Matplotlib": [
        "Data Visualization with Matplotlib"
    ]
}


def course_data(course):
    if not course:
        return None

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "provider": course.provider,
        "url": course.url,
        "difficulty": course.difficulty,
        "duration_hours": course.duration_hours
    }


def learning_path_data(path, db):
    items = (
        db.query(LearningPathItem)
        .filter(
            LearningPathItem.learning_path_id == path.id
        )
        .order_by(LearningPathItem.sequence)
        .all()
    )

    result_items = []

    for item in items:
        course = None

        if item.item_type == "course" and item.item_id:
            course = (
                db.query(Course)
                .filter(Course.id == item.item_id)
                .first()
            )

        result_items.append({
            "id": item.id,
            "type": item.item_type,
            "item_id": item.item_id,
            "title": item.title,
            "sequence": item.sequence,
            "status": item.status,
            "course": course_data(course)
        })

    total_items = len(items)
    completed_items = sum(
        1 for item in items
        if item.status == "completed"
    )

    progress = 0

    if total_items > 0:
        progress = round(
            (completed_items / total_items) * 100,
            1
        )

    return {
        "id": path.id,
        "user_id": path.user_id,
        "career_id": path.career_id,
        "title": path.title,
        "status": path.status,
        "career": db.query(Career)
            .filter(Career.id == path.career_id)
            .first().name,
        "total_items": total_items,
        "completed_items": completed_items,
        "progress": progress,
        "items": result_items
    }


@router.post("/{user_id}")
def generate_learning_path(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

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
            detail="Career prediction not found"
        )

    career = (
        db.query(Career)
        .filter(Career.name == prediction.predicted_career)
        .first()
    )

    if not career:
        raise HTTPException(
            status_code=404,
            detail="Career not found"
        )

    existing_path = (
        db.query(LearningPath)
        .filter(
            LearningPath.user_id == user_id,
            LearningPath.career_id == career.id
        )
        .order_by(LearningPath.created_at.desc())
        .first()
    )

    if existing_path:
        return learning_path_data(
            existing_path,
            db
        )

    gaps = (
        db.query(SkillGap)
        .filter(
            SkillGap.user_id == user_id,
            SkillGap.career_id == career.id,
            SkillGap.gap > 0
        )
        .order_by(SkillGap.gap.desc())
        .all()
    )

    path = LearningPath(
        user_id=user_id,
        career_id=career.id,
        title=f"{career.name} Learning Path",
        status="active"
    )

    db.add(path)
    db.commit()
    db.refresh(path)

    sequence = 1
    added_courses = set()

    for gap in gaps:
        from app.models import Skill

        skill = (
            db.query(Skill)
            .filter(Skill.id == gap.skill_id)
            .first()
        )

        if not skill:
            continue

        course_titles = SKILL_COURSE_MAP.get(
            skill.name,
            []
        )

        for course_title in course_titles:
            if course_title in added_courses:
                continue

            course = (
                db.query(Course)
                .filter(Course.title == course_title)
                .first()
            )

            if not course:
                continue

            item = LearningPathItem(
                learning_path_id=path.id,
                item_type="course",
                item_id=course.id,
                title=course.title,
                sequence=sequence,
                status="pending"
            )

            db.add(item)

            added_courses.add(course_title)
            sequence += 1

    db.commit()

    return learning_path_data(
        path,
        db
    )


@router.get("/{user_id}")
def get_learning_path(
    user_id: int,
    db: Session = Depends(get_db)
):
    path = (
        db.query(LearningPath)
        .filter(LearningPath.user_id == user_id)
        .order_by(LearningPath.created_at.desc())
        .first()
    )

    if not path:
        raise HTTPException(
            status_code=404,
            detail="Learning path not found"
        )

    return learning_path_data(
        path,
        db
    )


@router.patch("/items/{item_id}/complete")
def complete_learning_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(LearningPathItem)
        .filter(LearningPathItem.id == item_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Learning path item not found"
        )

    item.status = "completed"

    path = (
        db.query(LearningPath)
        .filter(
            LearningPath.id == item.learning_path_id
        )
        .first()
    )

    if not path:
        raise HTTPException(
            status_code=404,
            detail="Learning path not found"
        )

    db.commit()

    return learning_path_data(
        path,
        db
    )
