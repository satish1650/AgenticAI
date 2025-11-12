import os
from dotenv import load_dotenv

load_dotenv()

# Set your API key (replace YOUR_API_KEY with your actual key)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Verify it’s set
print("GOOGLE_API_KEY set successfully!")

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

agent.print_response(input="Trending startups and products and stories from hackernews")