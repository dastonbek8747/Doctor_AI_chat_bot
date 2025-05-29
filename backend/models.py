from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)

    # Munosabatlar
    symptoms = relationship("Symptom", back_populates="user", cascade="all, delete")
    diagnoses = relationship("Diagnosis", back_populates="user", cascade="all, delete")


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    date_save = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship("User", back_populates="symptoms")


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    date_save = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship("User", back_populates="diagnoses")


class Chat_History(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
