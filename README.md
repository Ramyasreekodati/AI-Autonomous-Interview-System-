# AI Interview System

A comprehensive AI-driven interview platform designed to automate and enhance the candidate evaluation process.

## Project Structure
- **/backend**: FastAPI-based server handling session logic, questions, and AI model orchestration.
- **/frontend**: React-based candidate portal with real-time video monitoring and interview flow.
- **/ai_modules**: Specialized Python modules for CV (Computer Vision) and NLP (Natural Language Processing).

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js & npm

### Backend Setup
1. Navigate to `/backend`: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `python main.py`

### Frontend Setup
1. Navigate to `/frontend`: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

## Phase 1-5 Deliverables
- [x] Backend Core (FastAPI) & Database (SQLite/SQLAlchemy)
- [x] Frontend Boilerplate (React + Tailwind)
- [x] Candidate Session Flow & Persistence
- [x] Real-time Face Tracking (MediaPipe) & Low-Focus Alerts
- [x] WebSocket Communication for CV Frames
- [x] NLP Answer Relevance Scoring (Logic Layer)
- [x] Automated PDF Report Generation (fpdf2)
- [x] Admin Session Analytics Endpoint
