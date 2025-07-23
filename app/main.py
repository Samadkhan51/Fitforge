# app/main.py
import logging
import os
from contextlib import asynccontextmanager # <-- Import this

logging.getLogger("google.adk").setLevel(logging.ERROR)

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from .models import ActivityLevel, Goal
from .agent import fitforge_agent
from ..seed_db import seed_db # <-- Import the seeder script
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

# --- NEW: Lifespan function to run seeder on startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs once when the application starts up.
    print("Application startup: Checking and seeding database...")
    try:
        # We call the seed_database function directly.
        seed_db.seed_database()
        print("✅ Database seeding check complete.")
    except Exception as e:
        print(f"❌ Database seeding failed on startup: {e}")
    yield
    # Code below yield would run on shutdown.

app = FastAPI(title="FitForge Agent API", lifespan=lifespan) # <-- Add lifespan here

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
session_service = InMemorySessionService()
runner = Runner(
    agent=fitforge_agent,
    app_name="fitforge_agent_app",
    session_service=session_service,
)

class PlanRequest(BaseModel):
    age: int
    weight_kg: float
    height_cm: float
    gender: str
    activity_level: ActivityLevel
    goal: Goal
    available_equipment: List[str]
    days_per_week: int

@app.post("/generate-plan")
async def generate_plan(request: PlanRequest):
    prompt = f"""
    Please act as an expert fitness and nutrition coach.
    A new client has provided the following profile and needs a comprehensive fitness and meal plan.

    **Client Profile:**
    - **Goal:** {request.goal.value}
    - **Experience / Activity Level:** {request.activity_level.value}
    - **Workouts Per Week:** {request.days_per_week}
    - **Available Equipment:** {', '.join(request.available_equipment) if request.available_equipment else 'Bodyweight only'}
    - **Age:** {request.age}
    - **Gender:** {request.gender}
    - **Weight:** {request.weight_kg} kg
    - **Height:** {request.height_cm} cm

    Your Task:
    1.  First, calculate the user's daily energy and macronutrient needs.
    2.  Based on those needs, create a detailed, sample one-day meal plan.
    3.  Create a detailed, {request.days_per_week}-day workout plan tailored to their goal and equipment.
    4.  Combine everything into a single, encouraging, and easy-to-read report.
    """
    try:
        session = await session_service.create_session(
            app_name="fitforge_agent_app", user_id="api_user"
        )
        user_message = genai_types.Content(
            role="user", parts=[genai_types.Part(text=prompt)]
        )
        final_response = "[Agent did not produce a final response]"
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=user_message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break
        return {"plan": final_response}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    mode: Optional[str] = 'both'

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if request.session_id:
            session = await session_service.get_session(app_name="fitforge_agent_app", user_id="api_user", session_id=request.session_id)
            if not session:
                session = await session_service.create_session(app_name="fitforge_agent_app", user_id="api_user")
        else:
            session = await session_service.create_session(app_name="fitforge_agent_app", user_id="api_user")

        # --- UPDATED: Stricter System Prompts ---
        if request.mode == 'diet':
            system_prompt = (
                "You are FitForge, an expert diet and nutrition AI coach. "
                "Your sole purpose is to answer questions about diet, nutrition, food, calories, macros, and healthy eating. "
                "You MUST politely refuse to answer any question that is not related to these topics, including exercise. "
                "If you do not know the user's dietary preferences (e.g., vegetarian, allergies) or calorie goals, you must ask for this information before providing a plan."
            )
        elif request.mode == 'exercise':
            system_prompt = (
                "You are FitForge, an expert exercise and fitness AI coach. "
                "Your sole purpose is to answer questions about exercise, workouts, routines, sets, reps, and exercise form. "
                "You MUST politely refuse to answer any question that is not related to these topics, including diet and nutrition. "
                "If you do not know the user's experience level (beginner, intermediate, advanced) or how often they work out, you must ask for this information before providing a plan."
            )
        else: # 'both' mode
            system_prompt = (
                "You are FitForge, an expert fitness and nutrition AI coach. "
                "Your purpose is to assist with fitness AND nutrition. "
                "You MUST politely refuse to answer any question that is not related to fitness, diet, or health. "
                "If you need details like age, weight, height, goal, etc., to provide a personalized plan, you must ask for them."
            )
        
        full_prompt = f"{system_prompt}\n\nAlways be creative, engaging, and motivational! Use emojis and well-structured markdown.\n\nUser: {request.message}"

        user_message = genai_types.Content(role="user", parts=[genai_types.Part(text=full_prompt)])
        final_response = "[Agent did not produce a final response]"
        async for event in runner.run_async(user_id=session.user_id, session_id=session.id, new_message=user_message):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break
        return ChatResponse(response=final_response, session_id=session.id)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    return FileResponse('app/frontend/index.html')

@app.get("/{page_name}.html")
async def serve_html(page_name: str):
    file_path = f"app/frontend/{page_name}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Page not found")
