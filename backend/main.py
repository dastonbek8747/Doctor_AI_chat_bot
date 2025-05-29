from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import schemas
import services

app = FastAPI(
    title="Medical Diagnosis Bot",
    description="A bot for medical diagnosis and chat using BioMistral or LLaMA3.2",
    version="1.0.0"
)

# Jadvallarni avtomatik yaratish
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to the Medical Diagnosis Bot"}


# ==================== USER ENDPOINTS ====================
@app.get("/users", tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    users = services.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@app.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", tags=["users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        services.create_user(db, user)
        return {"message": "User created successfully"}
    except:
        return {"message": "User already exists"}


# ==================== SYMPTOM ENDPOINTS ====================
@app.get("/symptoms", tags=["symptoms"])
async def get_symptoms(db: Session = Depends(get_db)):
    symptoms = services.get_symptoms(db)
    if not symptoms:
        raise HTTPException(status_code=404, detail="No symptoms found")
    return symptoms


@app.get("/symptoms/{symptom_id}", tags=["symptoms"])
async def get_symptom_by_id(symptom_id: int, db: Session = Depends(get_db)):
    symptom = services.get_symptom_by_id(db, symptom_id)
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom


@app.post("/symptoms", tags=["symptoms"])
async def create_symptom(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    return services.create_symptom(db, symptom)


# ==================== DIAGNOSIS ENDPOINTS ====================
@app.get("/diagnoses", tags=["diagnoses"])
async def get_diagnoses(db: Session = Depends(get_db)):
    diagnoses = services.get_diagnoses(db)
    if not diagnoses:
        raise HTTPException(status_code=404, detail="No diagnoses found")
    return diagnoses


@app.get("/diagnoses/{diagnosis_id}", tags=["diagnoses"])
async def get_diagnosis_by_id(diagnosis_id: int, db: Session = Depends(get_db)):
    diagnosis = services.get_diagnosis_by_id(db, diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis


@app.post("/diagnoses", tags=["diagnoses"])
async def create_diagnosis(diagnosis: schemas.DiagnosisCreate, db: Session = Depends(get_db)):
    return services.create_diagnosis(db, diagnosis)


# ==================== USER-SPECIFIC ENDPOINTS ====================
@app.get("/users/{user_id}/symptoms", tags=["Get User Symptoms"])
async def get_symptoms_by_user_id(user_id: int, db: Session = Depends(get_db)):
    symptoms = services.get_symptoms_by_user_id(db, user_id)
    if not symptoms:
        raise HTTPException(status_code=404, detail="No symptoms found for this user")
    return symptoms


@app.get("/users/{user_id}/diagnoses", tags=["Get User Diagnoses"])
async def get_diagnoses_by_user_id(user_id: int, db: Session = Depends(get_db)):
    diagnoses = services.get_diagnoses_by_user_id(db, user_id)
    if not diagnoses:
        raise HTTPException(status_code=404, detail="No diagnoses found for this user")
    return diagnoses


# ==================== CHAT ENDPOINTS ====================
@app.get("/users/{user_id}/chat-history", tags=["Chat History"])
async def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    chat_history = services.get_chat_history_by_user_id(db, user_id)
    if not chat_history:
        raise HTTPException(status_code=404, detail="No chat history found for this user")
    return chat_history


@app.post("/users/{user_id}/chat", tags=["Chat"])
async def chat_with_user(user_id: int, message: schemas.ChatHistoryCreate, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # LLM bilan suhbat
    response = services.chat_with_llm(user_id, message.message, db)

    # Chat tarixiga saqlash
    chat_message = services.create_chat_message(db, user_id=user_id, message=message.message, sender="user")
    chat_response = services.create_chat_message(db, user_id=user_id, message=response, sender="ai")
    return chat_response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="localhost", port=8000)
