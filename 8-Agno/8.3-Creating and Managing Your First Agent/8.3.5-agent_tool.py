from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

import os
from agno.models.google import Gemini

# Set your API key (replace YOUR_API_KEY with your actual key)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

agent = Agent(tools=[DuckDuckGoTools()], markdown=True,debug_mode=True,  model=Gemini(id="gemini-2.0-flash"),
)
agent.print_response("Whats happening in world of AI?", stream=True)