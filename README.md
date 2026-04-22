# AI Resume Generator

An advanced, AI-powered tool designed to transform existing resumes into high-quality, ATS-compliant documents. Built with a modern React frontend and a robust Python FastAPI backend, this application leverages Artificial Intelligence to optimize content, formatting, and industry-specific keywords.

## 🚀 Key Features

*   **ATS Optimization**: Automatically formats resumes to pass Applicant Tracking Systems.
*   **AI-Powered Content Enhancement**: Improves bullet points, summaries, and skills using GenAI.
*   **Real-time Analysis**: Provides instant feedback on resume strength and missing keywords.
*   **Modern UI**: Sleek, responsive interface built with Tailwind CSS and Framer Motion.
*   **PDF & DOCX Support**: Input and output in standard recruitment formats.
*   **Secure Authentication**: User accounts and secure file handling.

## 🛠️ Tech Stack

### Frontend
*   **Framework**: React (Vite)
*   **Styling**: Tailwind CSS, Framer Motion
*   **State Management**: React Context / Hooks
*   **HTTP Client**: Axios

### Backend
*   **Framework**: FastAPI (Python)
*   **AI/ML**: Groq API (or configurable LLM provider)
*   **Database**: SQLite (SQLAlchemy ORM)
*   **Authentication**: JWT (JSON Web Tokens)

## 📦 Project Structure

```bash
Resume-AI-Generator/
├── src/                # React Frontend Source
├── server/             # Python FastAPI Backend
├── public/             
├── docker-compose.yml 
└── ...config files
```

## 🏁 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python (3.9+)
*   Groq API Key (for AI features)

### 1. Setup Frontend
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### 2. Setup Backend
Open a new terminal:
```bash
cd server

# Create virtual environment
python -m venv venv
# Windows
.\venv\Scripts\Activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Server
uvicorn main:app --reload --port 8000
```

### 3. Environment Variables
Create a `.env` file in the root for frontend config:
```env
VITE_API_URL=http://localhost:8000
```
Create a `.env` file in `server/` for backend config:
```env
GROQ_API_KEY=your_api_key_here
```

## ☁️ Deployment (Lovable / Production)

This project is optimized for a **Split Deployment** strategy:

1.  **Backend**: Deploy the `server/` folder to a Python hosting service like **Render**, **Railway**, or **Fly.io**.
2.  **Frontend**: Deploy the root directory to **Lovable.dev**, **Vercel**, or **Netlify**.
3.  **Link**: Update the Frontend's `VITE_API_URL` environment variable to point to your live backend URL (e.g., `https://my-api.onrender.com`).

