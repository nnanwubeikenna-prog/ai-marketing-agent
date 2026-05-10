import os
import asyncio
import json
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

from langchain_core.runnables import RunnableConfig
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

# Load environment variables (Notion Page IDs, etc.)
load_dotenv()

# Define State - Cleaned up, no manual auth needed
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    remaining_steps: int

# Initialize LLM and Memory
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
memory = MemorySaver()

def dynamic_system_prompt(state: dict | None = None, config: RunnableConfig | None = None) -> str:
    """Builds the system prompt. In an MCP environment, tools are injected dynamically."""
    merged = {}
    if config and isinstance(config, dict):
        merged.update(config.get("configurable", {}))
    if state and isinstance(state, dict):
        merged.update(state)

    # Securely fetch the target Notion Page ID from environment variables
    notion_page_id = os.getenv("TARGET_NOTION_PAGE_ID", "2edfbae5-17da-80a9-8cc2-f3dca65848d8")
    brand_style = merged.get("brand_style") or "Ikenna Brand Kit"

    return (
        f"### ROLE\n"
        f"You are a world-class Marketing Strategist and AI Designer.\n"
        f"Your goal is to converse with the user to brainstorm brand concepts. When explicitly asked, you will convert Notion content into final Canva images.\n\n"
        f"### TARGET DATA\n"
        f"- Notion Page ID: {notion_page_id}\n"
        f"- Brand Style: {brand_style}\n\n"
        f"### PROTOCOL\n"
        f"1. **EVALUATE INTENT**: Are they chatting/brainstorming, or asking for a design? If chatting, respond as a marketing expert. If designing, identify the date.\n"
        f"2. **FETCH CONTENT**: Use the Notion tool to find scheduled activities for the identified date.\n"
        f"3. **DESIGN**: Use the Canva 'generate-design' tool to create a post based on the activities found.\n"
        f"   - CRITICAL BRANDING RULE: You MUST include this exact instruction: 'Use my \"{brand_style}\" for the design.'\n"
        f"4. **EXPORT**: Once generated, use the Canva 'export-design' tool to export it as a high-resolution JPG or PNG and provide the DIRECT URL.\n"
    )

async def setup_agent():
    # 1. Load the MCP configurations from the JSON file
    with open("mcp_config.json", "r") as f:
        config = json.load(f)

    # 2. Initialize and connect the MCP client
    client = MultiServerMCPClient(config)
    await client.connect()

    # 3. Dynamically fetch the tools from the connected servers
    mcp_tools = client.get_tools()

    # 4. Create the agent with the fetched tools
    agent = create_agent(
        model=model,
        tools=mcp_tools,
        state_schema=AgentState,
        system_prompt=dynamic_system_prompt(),
        checkpointer=memory
    )
    return agent

_agent_cache = None

async def get_agent():
    global _agent_cache
    if _agent_cache is None:
        _agent_cache = await setup_agent()
    return _agent_cache

async def get_agent():
    global _agent_cache
    if _agent_cache is None:
        _agent_cache = await setup_agent()
    return _agent_cache
