from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class LearningPathItem(Base):
    __tablename__ = "learning_path_items"

    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(
        Integer,
        ForeignKey("learning_paths.id"),
        nullable=False
    )
    item_type = Column(String(50), nullable=False)
    item_id = Column(Integer)
    title = Column(String(200), nullable=False)
    sequence = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")