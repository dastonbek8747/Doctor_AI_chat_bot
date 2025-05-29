from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    username: str
    last_name: str
    age: int
    gender: str
    phone: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    symptoms: Optional[List["Symptom"]] = []
    diagnoses: Optional[List["Diagnosis"]] = []

    class Config:
        from_attributes = True

# Symptom schemas
class SymptomBase(BaseModel):
    description: str

class SymptomCreate(SymptomBase):
    pass

class Symptom(SymptomBase):
    id: int
    user_id: int
    date_save: datetime

    class Config:
        from_attributes = True

# Diagnosis schemas
class DiagnosisBase(BaseModel):
    description: str

class DiagnosisCreate(DiagnosisBase):
    pass

class Diagnosis(DiagnosisBase):
    id: int
    user_id: int
    date_save: datetime

    class Config:
        from_attributes = True

# Chat_History schemas
class ChatHistoryBase(BaseModel):
    message: str
    sender: str

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistory(ChatHistoryBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True