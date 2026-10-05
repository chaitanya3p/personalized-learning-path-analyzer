from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(
    name: str,
    email: str,
    education: str,
    branch: str,
    graduation_year: int,
    db: Session = Depends(get_db)
):
    user = User(
        name=name,
        email=email,
        password_hash="not_set",
        education=education,
        branch=branch,
        graduation_year=graduation_year
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "education": user.education,
        "branch": user.branch,
        "graduation_year": user.graduation_year
    }
