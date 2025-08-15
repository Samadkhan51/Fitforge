# app/agent.py
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from google.adk.models import Gemini

# Try to load .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("DEBUG: dotenv loaded successfully")
except ImportError:
    # dotenv not available, which is fine for production deployments
    print("DEBUG: dotenv not available, using system environment variables")

mcp_connection_params = StdioConnectionParams(
    server_params={
        "command": "python",
        "args": ["-m", "app.mcp_server"],
    },
    timeout=60.0,
)

# Debug: Print environment variables to see what's available
print("DEBUG: Available environment variables:")
for key in sorted(os.environ.keys()):
    if 'GOOGLE' in key or 'API' in key or 'RAILWAY' in key:
        print(f"  {key}: {'***' if 'KEY' in key else os.environ[key]}")

api_key = os.getenv("GOOGLE_API_KEY")
print(f"DEBUG: GOOGLE_API_KEY found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"DEBUG: API key starts with: {api_key[:10]}...")

if not api_key:
    print("DEBUG: All environment variables:")
    for key, value in sorted(os.environ.items()):
        print(f"  {key}: {'***' if 'KEY' in key or 'PASSWORD' in key or 'SECRET' in key else value}")
    raise ValueError("LLM configuration error: Please set GOOGLE_API_KEY environment variable.")

# --- Define the FitForge Agent ---
fitforge_agent = LlmAgent(
    name="fitforge_agent",
    description="A comprehensive AI fitness and nutrition coach.",
    # --- ADDED: Strict instructions for the agent's persona and scope ---
    instruction=(
        "You are FitForge, an expert AI fitness and nutrition coach. "
        "Your sole purpose is to assist users with their fitness and nutrition goals. "
        "This includes creating workout/meal plans, answering questions about exercises, food, nutrition, and logging progress. "
        "You MUST politely refuse to answer any question that is not related to fitness, diet, or health. "
        "Do not answer questions about any other topic, no matter how simple it seems. "
        "For example, if asked about history, programming, or the weather, you must say something like, "
        "'As a fitness and nutrition coach, I can only answer questions related to those topics.'"
    ),
    model=Gemini(
        model_name="gemini-1.5-flash-latest",
        api_key=api_key
    ),
    tools=[
        MCPToolset(connection_params=mcp_connection_params)
    ],
)
