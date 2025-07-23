# FitForge: Your Personal AI Fitness & Nutrition Coach

FitForge is a complete, full-stack web application that acts as a personal AI coach. It leverages a sophisticated, multi-tool AI agent to create highly personalized workout and meal plans based on user-specific data and goals.

This project is designed to showcase a professional, scalable, and modern AI application architecture, suitable for a high-level portfolio. It moves beyond simple API calls to a true, decision-making agentic system.

## Key Features

* **Advanced Agentic Architecture:** Built with the Google ADK framework, the agent has a strict expert persona and connects to a separate `FastMCP` server that hosts a rich toolkit of fitness and nutrition functions.
* **Multi-Tool Execution:** The agent can use multiple tools in a single turn to perform complex, multi-step tasks like calculating a user's caloric needs and then generating a meal plan based on the results.
* **Fully Containerized:** The entire backend stack (PostgreSQL Database, FastAPI Server, ADK Agent, MCP Tool Server) is orchestrated with Docker and Docker Compose for a seamless, one-command setup.
* **Automated Database Seeding:** On the first run, a dedicated Docker service automatically populates the PostgreSQL database with a comprehensive knowledge base of exercises and food nutrition data.
* **Modern API:** A clean FastAPI backend serves the AI agent and provides a simple, powerful endpoint for interaction.
* **Interactive Frontend:** A user-friendly HTML/CSS/JS frontend provides a polished chat interface for users to interact with the agent.

## Tech Stack

* **Backend:** Python, FastAPI
* **AI Agent Framework:** Google ADK (Agent Development Kit)
* **Tool Server:** FastMCP
* **LLM:** Google Gemini (via API)
* **Database:** PostgreSQL
* **Containerization:** Docker & Docker Compose
* **Frontend:** HTML, CSS, JavaScript

## Architecture

FitForge uses a decoupled, microservice-style architecture. The main `agent-api` container runs a FastAPI server which hosts the ADK Agent. When the agent needs to perform an action, it starts and communicates with its `mcp_server` as a subprocess. This tool server then executes the required functions, which can include making calculations or querying the PostgreSQL database. This entire process is orchestrated by Docker Compose.

## Getting Started

### Prerequisites
* Git
* Docker Desktop (must be running)

### 1. Clone the Repository
```bash
git clone https://github.com/SyedShahmeerAli12/FitForge-Agent
cd fitforge
```

### 2. Configure Your Environment
Create a secret `.env` file to hold your API key by copying the provided template.

* **On Windows:**
    ```bash
    copy .env.example .env
    ```
* **On Mac/Linux:**
    ```bash
    cp .env.example .env
    ```
Now, open the new `.env` file and paste your secret **Google API Key** into it.

### 3. Build and Run the Application
This single command will build the Docker images, start the database, automatically seed it with the knowledge base, and start your agent's API server.
```bash
docker compose up --build -d
```
After a minute, the entire system will be online.

## How to Use the Application

### 1. Open the Web App
Navigate to **`http://localhost:8000`** in your web browser. You will see the FitForge landing page.

### 2. Start a Conversation
Click on one of the coaching modes to start a chat session with the AI.

### 3. Use the API (with Postman)
You can also interact with the agent directly through its API endpoint.

* **Endpoint:** `POST http://localhost:8000/generate-plan`
* **Body:** (raw, JSON)
    ```json
    {
      "age": 30,
      "weight_kg": 80,
      "height_cm": 180,
      "gender": "male",
      "activity_level": "moderately_active",
      "goal": "build_muscle",
      "available_equipment": ["Barbell", "Dumbbells", "Bench"],
      "days_per_week": 3
    }
    ```

## How to Stop
To stop all the running containers, run the following command in your terminal:
```bash
docker compose down
