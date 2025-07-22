# app/agent.py
import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams

load_dotenv()

# Set up the connection to the local tool server
mcp_connection_params = StdioConnectionParams(
    server_params={
        "command": "python",
        "args": ["-m", "app.mcp_server"],
    },
    timeout=60.0,
)

# Use LiteLlm to connect to the Ollama model specified in the .env file
model_name = os.getenv("OLLAMA_MODEL", "ollama_chat/qwen2.5:32b")
model = LiteLlm(model=model_name)

# Define the master agent that will orchestrate the tasks
fitforge_agent = LlmAgent(
    model=model,
    name="fitforge_agent",
    description=(
        "A comprehensive AI fitness and nutrition coach. It can create workout and meal plans, "
        "log workouts and daily weight, calculate health metrics like BMI, look up exercises "
        "and food nutrition, track strength progress, and suggest exercise substitutions."
    ),
    tools=[
        MCPToolset(connection_params=mcp_connection_params)
    ],
)