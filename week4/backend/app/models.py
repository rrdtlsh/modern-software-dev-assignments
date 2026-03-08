from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Note(Base):
    """Database model for persisted notes."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)


class ActionItem(Base):
    """Database model for persisted action items."""

    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
