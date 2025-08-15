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

# Try multiple ways to get the API key
api_key = os.getenv("GOOGLE_API_KEY")

# If not found, try alternative environment variable names that Railway might use
if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY_")  # With trailing underscore
if not api_key:
    api_key = os.getenv("google_api_key")   # Lowercase
if not api_key:
    api_key = os.getenv("GoogleApiKey")     # CamelCase

# Debug: Check what we found
print(f"Environment variable check: GOOGLE_API_KEY = {'Found' if api_key else 'Not Found'}")

if not api_key:
    # Print available environment variables for debugging
    print("Available environment variables:")
    env_vars = list(os.environ.keys())
    print(f"Total variables: {len(env_vars)}")
    
    # Look for any variable that might contain our API key
    potential_keys = [k for k in env_vars if 'GOOGLE' in k.upper() or 'API' in k.upper()]
    if potential_keys:
        print(f"Potential API key variables: {potential_keys}")
    else:
        print("No variables containing 'GOOGLE' or 'API' found")
    
    raise ValueError(f"LLM configuration error: GOOGLE_API_KEY environment variable not found. Available vars: {len(env_vars)}")

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
