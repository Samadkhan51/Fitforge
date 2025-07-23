# app/mcp_server.py
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

from fastmcp import FastMCP
from app import tools as fitforge_tools

mcp = FastMCP(name="FitForge Tool Service")

mcp.tool()(fitforge_tools.calculate_tdee_and_macros)
mcp.tool()(fitforge_tools.calculate_bmi)
mcp.tool()(fitforge_tools.estimate_one_rep_max)
mcp.tool()(fitforge_tools.find_exercises_by_muscle)
mcp.tool()(fitforge_tools.get_macronutrients_for_food)
mcp.tool()(fitforge_tools.log_workout)
mcp.tool()(fitforge_tools.log_daily_weight)
mcp.tool()(fitforge_tools.get_strength_progress)
mcp.tool()(fitforge_tools.suggest_exercise_substitutions)

if __name__ == "__main__":
    print("🚀 Starting FitForge FastMCP Tool Server...")
    mcp.run()