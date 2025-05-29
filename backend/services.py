from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas
# ==================== USER CRUD ====================
def create_user(db: Session, user: schemas.UserCreate):
    """
    Yangi foydalanuvchi yaratish
    """
    db_user = models.User(
        username=user.username,
        last_name=user.last_name,
        age=user.age,
        gender=user.gender,
        phone=user.phone,
        password=user.password,  # Eslatma: Haqiqiy loyihada parolni shifrlash kerak
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    """
    Barcha foydalanuvchilarni olish
    """
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    """
    Foydalanuvchini ID bo'yicha olish
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


# ==================== SYMPTOM CRUD ====================
def create_symptom(db: Session, symptom: schemas.SymptomCreate):
    """
    Yangi simptom yaratish
    """
    db_symptom = models.Symptom(
        user_id=symptom.user_id,
        description=symptom.description,
        date_save=datetime.now()
    )
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom


def get_symptoms(db: Session):
    """
    Barcha simptomlarni olish
    """
    return db.query(models.Symptom).all()


def get_symptom_by_id(db: Session, symptom_id: int):
    """
    Simptomni ID bo'yicha olish
    """
    return db.query(models.Symptom).filter(models.Symptom.id == symptom_id).first()


def get_symptoms_by_user_id(db: Session, user_id: int):
    """
    Foydalanuvchi ID bo'yicha simptomlarni olish
    """
    return db.query(models.Symptom).filter(models.Symptom.user_id == user_id).all()


# ==================== DIAGNOSIS CRUD ====================
def create_diagnosis(db: Session, diagnosis: schemas.DiagnosisCreate):
    """
    Yangi diagnostika yaratish
    """
    db_diagnosis = models.Diagnosis(
        user_id=diagnosis.user_id,
        description=diagnosis.description,
        date_save=datetime.now()
    )
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis


def get_diagnoses(db: Session):
    """
    Barcha diagnostikalarni olish
    """
    return db.query(models.Diagnosis).all()


def get_diagnosis_by_id(db: Session, diagnosis_id: int):
    """
    Diagnostikani ID bo'yicha olish
    """
    return db.query(models.Diagnosis).filter(models.Diagnosis.id == diagnosis_id).first()


def get_diagnoses_by_user_id(db: Session, user_id: int):
    """
    Foydalanuvchi ID bo'yicha diagnostikalarni olish
    """
    return db.query(models.Diagnosis).filter(models.Diagnosis.user_id == user_id).all()


# ==================== CHAT HISTORY CRUD ====================
def create_chat_message(db: Session, user_id: int, message: str, sender: str):
    """
    Chat tarixiga yangi xabar qo'shish
    """
    db_chat = models.Chat_History(
        user_id=user_id,
        message=message,
        sender=sender,
        timestamp=datetime.now()
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_chat_history_by_user_id(db: Session, user_id: int):
    """
    Foydalanuvchi ID bo'yicha chat tarixini olish
    """
    return db.query(models.Chat_History).filter(models.Chat_History.user_id == user_id).order_by(
        models.Chat_History.timestamp).all()


def get_recent_chat_history(db: Session, user_id: int, limit: int = 5):
    """
    Foydalanuvchi ID bo'yicha so'nggi chat xabarlarini olish (cheklangan miqdor)
    """
    return db.query(models.Chat_History).filter(models.Chat_History.user_id == user_id).order_by(
        models.Chat_History.timestamp.desc()).limit(limit).all()
