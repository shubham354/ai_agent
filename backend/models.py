from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    chats = relationship("Chat", back_populates="user")
    data_analyses = relationship("DataAnalysis", back_populates="user")

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    context = Column(JSON)  # Store any relevant context
    feedback_score = Column(Float)  # User feedback for response quality
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="chats")

class DataAnalysis(Base):
    __tablename__ = "data_analyses"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    analysis_results = Column(JSON)  # Store analysis results and visualizations
    insights = Column(JSON)  # AI-generated insights
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="data_analyses")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    visualization_preferences = Column(JSON)  # Preferred chart types, colors, etc.
    interaction_history = Column(JSON)  # Track patterns and preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 