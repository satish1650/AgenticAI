# Travel Planning
'''
In this example, we’ll walk through the process of creating a sophisticated travel planning system using AgentChat. 
Our travel planner will utilize multiple AI agents, each with a specific role, to collaboratively create a comprehensive travel itinerary.
'''

# First, let us import the necessary modules.

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
# from agents.agents import *
from agents.agents import planner_agent, local_agent, language_agent, travel_summary_agent


termination = TextMentionTermination("TERMINATE")
group_chat = RoundRobinGroupChat(
    [planner_agent, local_agent, language_agent, travel_summary_agent], 
    termination_condition=termination
)

Console(group_chat.run_stream(task="Plan a 3 day trip to Nepal."))

# model_client.close()