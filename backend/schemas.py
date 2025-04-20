from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str

class VisualizationData(BaseModel):
    type: str
    title: str
    data: str  # JSON string of plotly figure

class AnalysisResponse(BaseModel):
    analysis: Dict[str, Any]
    visualizations: List[VisualizationData]
    insights: List[str]

class UserPreferenceUpdate(BaseModel):
    visualization_preferences: Dict[str, Any]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str 