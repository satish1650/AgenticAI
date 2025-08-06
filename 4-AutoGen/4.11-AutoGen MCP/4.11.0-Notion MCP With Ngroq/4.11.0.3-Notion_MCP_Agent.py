import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import FunctionCallTermination, TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key= os.getenv("OPENAI_API_KEY")
notion_secret= os.getenv("NOTION_TOKEN")