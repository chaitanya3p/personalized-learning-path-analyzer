from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import joblib

from app.database import get_db
from app.models import User, UserSkill, Skill, Prediction

router = APIRouter(prefix="/predictions", tags=["Predictions"])

model = joblib.load("app/ml/career_model.pkl")


@router.post("/{user_id}")
def predict_career(
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
        .all()
    )

    if not results:
        raise HTTPException(
            status_code=400,
            detail="User has no skills"
        )

    skill_text = " ".join(
        skill.name
        for skill, proficiency in results
        for _ in range(max(1, proficiency))
    )

    predicted_career = model.predict([skill_text])[0]

    probabilities = model.predict_proba([skill_text])[0]
    confidence = max(probabilities) * 100

    prediction = Prediction(
        user_id=user_id,
        predicted_career=predicted_career,
        confidence=round(confidence / 100, 4)
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "user_id": user_id,
        "predicted_career": predicted_career,
        "confidence": round(confidence, 2),
        "prediction_id": prediction.id,
        "skills_used": [
            {
                "skill": skill.name,
                "proficiency": proficiency
            }
            for skill, proficiency in results
        ]
    }
