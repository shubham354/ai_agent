from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, List
import pandas as pd
import json
from datetime import datetime, timedelta
import os

from database import get_db, init_db
from models import User, Chat, DataAnalysis, UserPreference
from services.ai_service import ai_service
from schemas import (
    UserCreate, UserResponse, ChatRequest, ChatResponse,
    AnalysisResponse, UserPreferenceUpdate
)
from security import (
    get_password_hash, verify_password,
    create_access_token, get_current_user
)

app = FastAPI(title="AI Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's chat history and preferences
    recent_chats = (
        db.query(Chat)
        .filter(Chat.user_id == current_user.id)
        .order_by(Chat.created_at.desc())
        .limit(5)
        .all()
    )
    
    preferences = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    
    # Build context from history and preferences
    context = {
        "recent_chats": [
            {"message": chat.message, "response": chat.response}
            for chat in recent_chats
        ],
        "preferences": preferences.visualization_preferences if preferences else None
    }
    
    # Generate AI response
    response = await ai_service.generate_response(request.message, context)
    
    # Store chat in database
    chat = Chat(
        user_id=current_user.id,
        message=request.message,
        response=response,
        context=context
    )
    db.add(chat)
    db.commit()
    
    return ChatResponse(message=response)

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Read file content
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload CSV or Excel files."
            )
        
        # Analyze data using AI service
        analysis_results = await ai_service.analyze_data(df)
        
        # Store analysis in database
        analysis = DataAnalysis(
            user_id=current_user.id,
            file_name=file.filename,
            file_path=f"uploads/{file.filename}",
            analysis_results=analysis_results["analysis"],
            insights=analysis_results["insights"]
        )
        db.add(analysis)
        db.commit()
        
        return AnalysisResponse(
            analysis=analysis_results["analysis"],
            visualizations=analysis_results["visualizations"],
            insights=analysis_results["insights"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/preferences")
async def update_preferences(
    preferences: UserPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_preferences = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    
    if not db_preferences:
        db_preferences = UserPreference(
            user_id=current_user.id,
            visualization_preferences=preferences.visualization_preferences,
            interaction_history={}
        )
        db.add(db_preferences)
    else:
        db_preferences.visualization_preferences = preferences.visualization_preferences
        db_preferences.updated_at = datetime.utcnow()
    
    db.commit()
    return {"status": "success"}

@app.post("/feedback/{chat_id}")
async def provide_feedback(
    chat_id: int,
    score: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat.feedback_score = score
    db.commit()
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 