# Tours Thambi: Multi-Agentic AI Trip Planner 🌍✈️

Tours Thambi is an advanced, AI-powered travel planning application that utilizes a multi-agent LangGraph architecture to dynamically generate highly personalized, constraint-aware itineraries. 

By leveraging native browser Voice APIs and a beautiful, premium glassmorphism frontend (styled with Tailwind CSS), Tours Thambi offers a seamless and futuristic trip-planning experience.

## ✨ Key Features
- **🧠 Multi-Agent Architecture**: Uses `LangGraph` to orchestrate specialized AI agents (Destination, Logistics, Budget, and Review) to cross-verify and compile itineraries.
- **🎤 Native Voice Integration**: Speak your constraints directly into the app using the Web Speech API (STT), and listen to your generated itinerary read aloud via SpeechSynthesis (TTS).
- **🎨 Premium UI/UX**: An aesthetic dark-mode frontend featuring glassmorphism, responsive Tailwind CSS layouts, and micro-animations, originally designed via Google Stitch.
- **🌐 100% Free Live Data**: Scrapes Wikivoyage for destination info, DuckDuckGo for live logistics, and Frankfurter for real-time currency exchange rates.
- **⚡ Decoupled Stack**: A high-performance Python FastAPI backend and a lightning-fast React + Vite frontend.

## 🛠️ Technology Stack
- **Backend**: Python, FastAPI, Uvicorn, LangChain, LangGraph, Groq (Llama-3).
- **Frontend**: React (Vite), Tailwind CSS v3, React Markdown.
- **APIs**: DuckDuckGo Search, Frankfurter Exchange Rates, Web Speech API.

## 🚀 Getting Started Locally

### 1. Clone the Repository
```bash
git clone https://github.com/Santhosh-A-Git/Tours-Thambi-Multi-Agentic-AI-trip-planner.git
cd Tours-Thambi-Multi-Agentic-AI-trip-planner
```

### 2. Backend Setup (FastAPI)
Set up a Python virtual environment and install the dependencies:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_api_key_here
```

Start the backend server:
```bash
uvicorn api:app --reload
```
*The API will be live at `http://localhost:8000`*

### 3. Frontend Setup (React/Vite)
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
```

Start the Vite development server:
```bash
npm run dev
```
*The web app will be live at `http://localhost:5173`*

## ☁️ Deployment

- **Backend (Railway)**: The root directory includes a `Procfile` ready for seamless deployment on Railway. Ensure you set your `GROQ_API_KEY` in the Railway dashboard variables.
- **Frontend (Vercel)**: The `frontend` directory is ready to be imported into Vercel as a Vite project. Make sure to set the `VITE_API_URL` environment variable to your deployed Railway backend URL.

## 📄 License
This project is open-source and available under the MIT License.
