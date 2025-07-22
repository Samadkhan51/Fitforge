# app/mcp_server.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the project root
# This needs to be done before other modules that might use the variables are imported.
# Assumes the script is run from the project root.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

from fastmcp import FastMCP
from app import tools as fitforge_tools

mcp = FastMCP(name="FitForge Tool Service")

# Register ALL the tools from your toolkit
mcp.tool()(fitforge_tools.calculate_tdee_and_macros)
mcp.tool()(fitforge_tools.calculate_bmi)
mcp.tool()(fitforge_tools.estimate_one_rep_max)
mcp.tool()(fitforge_tools.find_exercises_by_muscle)
mcp.tool()(fitforge_tools.get_macronutrients_for_food)
mcp.tool()(fitforge_tools.log_workout)
mcp.tool()(fitforge_tools.log_daily_weight)
mcp.tool()(fitforge_tools.get_strength_progress)
# mcp.tool()(fitforge_tools.generate_meal_plan) # Handled by the LlmAgent directly
# mcp.tool()(fitforge_tools.generate_workout_plan) # Handled by the LlmAgent directly
mcp.tool()(fitforge_tools.suggest_exercise_substitutions)

if __name__ == "__main__":
    print("🚀 Starting FitForge FastMCP Tool Server...")
    mcp.run()