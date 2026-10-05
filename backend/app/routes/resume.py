from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import tempfile
import joblib

from app.database import get_db
from app.models import User, Skill, UserSkill, Prediction
from app.services.resume_parser import extract_resume_text
from app.services.skill_extractor import extract_skills

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

model = joblib.load("app/ml/career_model.pkl")


@router.post("/upload/{user_id}")
async def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
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

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported"
        )

    contents = await file.read()

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        text = extract_resume_text(temp_path)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF"
        )

    skills = db.query(Skill).order_by(Skill.name).all()

    detected_skills = extract_skills(
        text,
        skills
    )

    saved_skills = []

    for skill in detected_skills:
        existing = db.query(UserSkill).filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill.id
        ).first()

        if not existing:
            db.add(
                UserSkill(
                    user_id=user_id,
                    skill_id=skill.id,
                    proficiency=1
                )
            )

        saved_skills.append({
            "id": skill.id,
            "name": skill.name,
            "category": skill.category
        })

    db.commit()

    if not detected_skills:
        raise HTTPException(
            status_code=400,
            detail="No recognizable skills found in the resume"
        )

    skill_text = " ".join(
        skill.name
        for skill in detected_skills
    )

    predicted_career = model.predict(
        [skill_text]
    )[0]

    probabilities = model.predict_proba(
        [skill_text]
    )[0]

    confidence = max(probabilities) * 100

    prediction = Prediction(
        user_id=user_id,
        predicted_career=predicted_career,
        confidence=round(confidence / 100, 4)
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    grouped_skills = {}

    for skill in saved_skills:
        category = skill["category"] or "Other"

        if category not in grouped_skills:
            grouped_skills[category] = []

        grouped_skills[category].append(
            skill["name"]
        )

    return {
        "user_id": user_id,
        "filename": file.filename,
        "message": "Resume analyzed successfully",
        "text_length": len(text),
        "total_skills": len(saved_skills),
        "detected_skills": saved_skills,
        "skills_by_category": grouped_skills,
        "predicted_career": predicted_career,
        "confidence": round(confidence, 2),
        "prediction_id": prediction.id
    }
