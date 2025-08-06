# AI-Powered L1 Automation E-commerce Assitant

This project is an AI-powered chatbot for an e-commerce store , using FastAPI for the backend and a simple HTML/CSS/JS frontend served by Node.js.

## Setup

### Backend (Python/FastAPI)
1.  Navigate to the `backend` directory: `cd backend`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate it: `source venv/bin/activate` (on Mac/Linux) or `.\venv\Scripts\activate` (on Windows)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file and add your `OPENROUTER_API_KEY`.

### Frontend (Node.js/Express)
1.  Navigate to the `frontend` directory: `cd frontend`
2.  Install dependencies: `npm install`

## Running the Application
1.  **Start the Backend:** In the `/backend` directory, run `uvicorn app.main:app --reload`
2.  **Start the Frontend:** In the `/frontend` directory, run `npm start`
3.  Open your browser to `http://localhost:3000`