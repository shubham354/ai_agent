# AI Agent Web Application

A full-stack AI agent web application powered by Google's Gemini API that provides intelligent chat assistance, data analysis, and visualization capabilities.

## Features

- Interactive AI chat interface
- Data analysis and visualization
- Multiple chart types (bar, line, pie, heatmap)
- User authentication and session management
- Adaptive AI responses based on user interaction history
- Modern, responsive UI with dark mode support
- PostgreSQL database for data persistence
- Docker containerization for easy deployment

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- Google Gemini API (LLM)
- Pandas & NumPy (Data analysis)
- Plotly & Matplotlib (Visualization)
- PostgreSQL (Database)
- JWT Authentication

### Frontend
- React with TypeScript
- Chakra UI (Component library)
- Chart.js (Interactive charts)
- Axios (HTTP client)
- React Router (Navigation)

## Prerequisites

- Node.js 16+
- Python 3.9+
- PostgreSQL 14+
- Docker & Docker Compose (optional)
- Google Gemini API key

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. Set up the backend:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the development servers:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## Docker Deployment

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Railway Deployment

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize the project:
   ```bash
   railway init
   ```

4. Add environment variables:
   ```bash
   railway variables set GEMINI_API_KEY=your_api_key
   railway variables set DATABASE_URL=your_database_url
   railway variables set SECRET_KEY=your_secret_key
   ```

5. Deploy:
   ```bash
   railway up
   ```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY`: Google Gemini API key
- `SECRET_KEY`: JWT secret key
- `CORS_ORIGINS`: Allowed CORS origins

### Frontend
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_WS_URL`: WebSocket URL (if using real-time features)

## Project Structure

```
.
├── backend/
│   ├── models/         # Database models
│   ├── services/       # Business logic
│   ├── routes/         # API endpoints
│   └── main.py         # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── contexts/   # React contexts
│   │   ├── services/   # API services
│   │   └── App.tsx     # Root component
│   └── public/         # Static assets
└── docker-compose.yml  # Docker configuration
```

## API Documentation

The API documentation is available at `/docs` when running the backend server. It includes:
- Authentication endpoints
- Chat endpoints
- Data analysis endpoints
- User preference endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 