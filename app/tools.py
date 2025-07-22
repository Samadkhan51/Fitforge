# app/tools.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from .models import Exercise, Food, User, WorkoutLog, WeightLog
import os
from datetime import datetime, timedelta
from typing import List
# import google.generativeai as genai # No longer needed
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
# This needs to be done before other modules that might use the variables are imported.
# Assumes the script is run from the project root.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Database Connection ---
DATABASE_URL = "postgresql://fitforge:fitforgepassword@postgres-db:5432/fitforgedb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================
# COMPLETE TOOLKIT (11 TOOLS)
# ============================================

# == 1. Health Calculation Tools ==

def calculate_tdee_and_macros(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str, goal: str) -> dict:
    """Calculates TDEE and macros based on a user's profile data."""
    if gender.lower() == 'male': bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else: bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    activity_multipliers = {"sedentary": 1.2, "lightly_active": 1.375, "moderately_active": 1.55, "very_active": 1.725}
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    if goal == 'lose_fat': target_calories = tdee - 500
    elif goal == 'build_muscle': target_calories = tdee + 500
    else: target_calories = tdee
    macros = {"calories": round(target_calories), "protein_g": round((target_calories * 0.30) / 4), "carbs_g": round((target_calories * 0.40) / 4), "fat_g": round((target_calories * 0.30) / 9)}
    return macros

def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """Calculates Body Mass Index (BMI) and provides a general category."""
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)
    category = "Unknown"
    if bmi < 18.5: category = "Underweight"
    elif 18.5 <= bmi < 24.9: category = "Normal weight"
    elif 25 <= bmi < 29.9: category = "Overweight"
    else: category = "Obese"
    return f"A weight of {weight_kg}kg and height of {height_cm}cm results in a BMI of {bmi}, which is in the '{category}' category."

def estimate_one_rep_max(weight_kg: float, reps: int) -> str:
    """Estimates the one-rep max (1RM) from a given weight and rep count using the Brzycki formula."""
    if reps == 1: return f"Your one-rep max is already {weight_kg}kg."
    if reps > 12: return "1RM estimation is most accurate for rep ranges of 12 or less."
    one_rep_max = round(weight_kg / (1.0278 - (0.0278 * reps)), 1)
    return f"Lifting {weight_kg}kg for {reps} reps gives an estimated one-rep max of {one_rep_max}kg."

# == 2. Knowledge Base Lookup Tools ==

def find_exercises_by_muscle(target_muscle: str, equipment: str) -> str:
    """Finds and lists exercises for a specific muscle group using available equipment."""
    db = SessionLocal()
    try:
        exercises = db.query(Exercise).filter(func.lower(Exercise.target_muscle) == func.lower(target_muscle), func.lower(Exercise.equipment).contains(func.lower(equipment))).limit(5).all()
        if not exercises: return f"No exercises found for {target_muscle} using {equipment}."
        exercise_names = [e.name for e in exercises]
        return f"Here are some {equipment} exercises for {target_muscle}: {', '.join(exercise_names)}."
    finally: db.close()

def get_macronutrients_for_food(food_name: str, weight_grams: float) -> str:
    """Calculates the calories and macronutrients for a specific weight of a given food."""
    db = SessionLocal()
    try:
        food = db.query(Food).filter(func.lower(Food.name).contains(func.lower(food_name))).first()
        if not food: return f"Food '{food_name}' not found in the database."
        multiplier = weight_grams / 100.0
        calories = round(food.calories_per_100g * multiplier)
        protein = round(food.protein_g_per_100g * multiplier, 1)
        carbs = round(food.carbs_g_per_100g * multiplier, 1)
        fat = round(food.fat_g_per_100g * multiplier, 1)
        return (f"{weight_grams}g of {food.name} has approximately: {calories} calories, {protein}g protein, {carbs}g carbs, and {fat}g fat.")
    finally: db.close()

# == 3. Data Logging Tools ==

def log_workout(user_id: int, exercise_name: str, sets: int, reps: int, weight_kg: float) -> str:
    """Logs a completed workout for a user in the database."""
    db = SessionLocal()
    try:
        exercise = db.query(Exercise).filter(func.lower(Exercise.name) == func.lower(exercise_name)).first()
        if not exercise: return f"Exercise '{exercise_name}' not found."
        new_log = WorkoutLog(user_id=user_id, exercise_id=exercise.id, sets=sets, reps=reps, weight_kg=weight_kg)
        db.add(new_log)
        db.commit()
        return f"Successfully logged workout: {sets} sets of {reps} reps of {exercise_name} at {weight_kg}kg."
    finally: db.close()

def log_daily_weight(user_id: int, weight_kg: float) -> str:
    """Logs the user's body weight for the current day."""
    db = SessionLocal()
    try:
        new_log = WeightLog(user_id=user_id, weight_kg=weight_kg)
        db.add(new_log)
        db.commit()
        return f"Successfully logged today's weight as {weight_kg}kg."
    finally: db.close()

# == 4. Progress Monitoring Tools ==

def get_strength_progress(user_id: int, exercise_name: str) -> str:
    """Retrieves and summarizes a user's strength progress for a specific exercise over time."""
    db = SessionLocal()
    try:
        exercise = db.query(Exercise).filter(func.lower(Exercise.name) == func.lower(exercise_name)).first()
        if not exercise: return f"Exercise '{exercise_name}' not found."
        logs = db.query(WorkoutLog).filter_by(user_id=user_id, exercise_id=exercise.id).order_by(WorkoutLog.date.asc()).all()
        if len(logs) < 2: return f"Not enough data to show progress for {exercise_name}. Keep logging your workouts!"
        first_log = logs[0]
        latest_log = logs[-1]
        return (f"Strength progress for {exercise_name}: You started at {first_log.weight_kg}kg for {first_log.reps} reps on {first_log.date.date()}. Your latest lift was {latest_log.weight_kg}kg for {latest_log.reps} reps on {latest_log.date.date()}.")
    finally: db.close()

# == 5. LLM-Powered Generative Tools ==
# These tools are no longer needed as the new LlmAgent will handle generation directly.

# def generate_meal_plan(calories: int, protein_g: int, carbs_g: int, fat_g: int) -> str:
#     """Generates a sample one-day meal plan using an LLM."""
#     genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#     model = genai.GenerativeModel('gemini-1.5-flash-latest')
#     prompt = f"Create a sample one-day meal plan for these targets: ~{calories} kcal, ~{protein_g}g protein, ~{carbs_g}g carbs, ~{fat_g}g fat. Structure as a markdown list."
#     response = model.generate_content(prompt)
#     return response.text

# def generate_workout_plan(goal: str, equipment: List[str], days_per_week: int) -> str:
#     """Generates a sample weekly workout plan using an LLM."""
#     genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#     model = genai.GenerativeModel('gemini-1.5-flash-latest')
#     prompt = f"Create a {days_per_week}-day workout plan for the goal '{goal}' using only this equipment: {', '.join(equipment)}. Structure as a markdown plan. Suggest 3-4 sets of 8-12 reps."
#     response = model.generate_content(prompt)
#     return response.text

def suggest_exercise_substitutions(exercise_to_replace: str, available_equipment: List[str]) -> str:
    """Suggests alternative exercises for a given exercise, using only available equipment."""
    db = SessionLocal()
    try:
        original_exercise = db.query(Exercise).filter(func.lower(Exercise.name) == func.lower(exercise_to_replace)).first()
        if not original_exercise: return f"Exercise '{exercise_to_replace}' not found."
        target_muscle = original_exercise.target_muscle
        substitutes = db.query(Exercise).filter(func.lower(Exercise.target_muscle) == func.lower(target_muscle), Exercise.equipment.in_(available_equipment), func.lower(Exercise.name) != func.lower(exercise_to_replace)).all()
        if not substitutes: return f"No substitutes found for {target_muscle} with your equipment."
        substitute_names = [e.name for e in substitutes]
        # The new LlmAgent will handle the generative part.
        # This tool's responsibility is now to find and list suitable substitutes.
        return f"Here are some suitable substitutes for {exercise_to_replace} using your equipment: {', '.join(substitute_names)}. The user should choose one."

    finally: db.close()