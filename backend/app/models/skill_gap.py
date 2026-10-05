from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    current_level = Column(Integer, nullable=False)
    required_level = Column(Integer, nullable=False)
    gap = Column(Integer, nullable=False)