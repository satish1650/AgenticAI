import os, asyncio
from dotenv import load_dotenv
# from codecs import StreamReader
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

# Set API Key
load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')

# Define Model Cli
model_client= OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

# Define Assistant Agent
assistant= AssistantAgent(
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who help on the task given.'
)

# Define User Proxy Agent --> Human in Loop
user_proxy_agent= UserProxyAgent(
    name="UserProxy",
    description='you are a user proxy agent',
    input_func=input # Getting feedback from user
)

# Termination Condition
termination_condition= TextMentionTermination(text="APPROVE")

# Define Team by using Round Robin Group Chat
team= RoundRobinGroupChat(
    participants=[assistant, user_proxy_agent],
    termination_condition=termination_condition,
    max_turns=10
)

stream= team.run_stream(task='Write a great poem about india?')

async def main():
    await Console(stream)

if (__name__=="__main__"):
    asyncio.run(main())