from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    provider = Column(String(100))
    url = Column(String(500))
    difficulty = Column(String(50))
    duration_hours = Column(Integer)