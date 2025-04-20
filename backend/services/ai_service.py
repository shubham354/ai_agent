import google.generativeai as genai
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

class AIService:
    def __init__(self):
        self.model = model
    
    async def generate_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Generate AI response based on user message and context"""
        prompt = self._build_prompt(message, context)
        response = self.model.generate_content(prompt)
        return response.text
    
    async def analyze_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data and generate insights"""
        analysis = self._perform_data_analysis(df)
        visualizations = self._generate_visualizations(df)
        insights = await self._generate_insights(analysis)
        
        return {
            "analysis": analysis,
            "visualizations": visualizations,
            "insights": insights
        }
    
    def _build_prompt(self, message: str, context: Optional[Dict] = None) -> str:
        """Build prompt with context for better responses"""
        if context:
            return f"Context:\n{json.dumps(context)}\n\nUser: {message}\nAssistant:"
        return f"User: {message}\nAssistant:"
    
    def _perform_data_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform statistical analysis on dataframe"""
        analysis = {
            "basic_info": {
                "rows": len(df),
                "columns": list(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "data_types": df.dtypes.astype(str).to_dict()
            },
            "statistics": df.describe().to_dict(),
            "correlations": df.corr().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 1 else None
        }
        return analysis
    
    def _generate_visualizations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate various visualizations based on data types"""
        visualizations = []
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Line charts for time series if date column exists
            date_cols = df.select_dtypes(include=['datetime64']).columns
            if len(date_cols) > 0:
                for date_col in date_cols:
                    for num_col in numeric_cols:
                        fig = px.line(df, x=date_col, y=num_col, 
                                    title=f"{num_col} over time")
                        visualizations.append({
                            "type": "line",
                            "title": f"{num_col} over time",
                            "data": fig.to_json()
                        })
            
            # Bar charts for numeric columns
            for col in numeric_cols:
                fig = px.bar(df[col].value_counts(), 
                            title=f"Distribution of {col}")
                visualizations.append({
                    "type": "bar",
                    "title": f"Distribution of {col}",
                    "data": fig.to_json()
                })
            
            # Correlation heatmap
            if len(numeric_cols) > 1:
                corr = df[numeric_cols].corr()
                fig = px.imshow(corr, title="Correlation Heatmap")
                visualizations.append({
                    "type": "heatmap",
                    "title": "Correlation Heatmap",
                    "data": fig.to_json()
                })
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].nunique() < 10:  # Only for columns with reasonable number of categories
                # Pie chart
                fig = px.pie(df, names=col, title=f"Distribution of {col}")
                visualizations.append({
                    "type": "pie",
                    "title": f"Distribution of {col}",
                    "data": fig.to_json()
                })
        
        return visualizations
    
    async def _generate_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate insights using Gemini API"""
        prompt = f"""
        Based on this data analysis, provide key insights and actionable recommendations:
        {json.dumps(analysis, indent=2)}
        
        Focus on:
        1. Key patterns and trends
        2. Potential areas for improvement
        3. Actionable recommendations
        4. Unusual findings or anomalies
        """
        
        response = self.model.generate_content(prompt)
        insights = response.text.split('\n')
        return [insight.strip() for insight in insights if insight.strip()]

ai_service = AIService() 