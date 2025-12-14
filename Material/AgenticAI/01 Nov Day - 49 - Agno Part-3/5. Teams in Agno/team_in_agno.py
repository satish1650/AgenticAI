from agno.team import Team
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from typing import Iterator
from agno.team import Team
from agno.agent import Agent
from agno.run.team import TeamRunOutputEvent
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

import os

# Set your API key (replace YOUR_API_KEY with your actual key)
os.environ["GOOGLE_API_KEY"] = "your-api-key-here"

# Verify it’s set
print("GOOGLE_API_KEY set successfully!")

# Create specialized agents
news_agent = Agent(
    id="news-agent", # Important
    name="News Agent", # Important
    role="Get the latest news and provide summaries", # Important
    tools=[DuckDuckGoTools()]
)

weather_agent = Agent(
    id="weather-agent", # Important
    name="Weather Agent", # Important
    role="Get weather information and forecasts",# Important
    tools=[DuckDuckGoTools()]
)

# Create the team
team = Team(
    name="News and Weather Team",
    members=[news_agent, weather_agent],
    model=OpenAIChat(id="gpt-4o"),
    instructions="Coordinate with team members to provide comprehensive information. " \
    "Delegate tasks based on the user's request."
)

# team.print_response("What's the latest news and weather in Tokyo?", stream=True)



# # Run team and return the response as a variable
# response = team.run("What is the weather in Tokyo?")
# # Print the response
# print(response)

# ################ STREAM RESPONSE #################
# stream: Iterator[TeamRunOutputEvent] = team.run("What is the weather in Tokyo?", stream=True)
# for chunk in stream:
#     if chunk.event == "TeamRunContent":
#         print(chunk.content)

# # ################ STREAM AND PRETTY PRINT #################
# stream: Iterator[TeamRunOutputEvent] = team.run("What is the weather in Tokyo?", stream=True)
# pprint_run_response(stream, markdown=True)