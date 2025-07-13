import asyncio
import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ['SERPER_API_KEY']=os.getenv("SERPER_API_KEY")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

model_client= OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

search_tool_wrapper= GoogleSerperAPIWrapper(type="search")

def search_web(query: str) -> str:
    """Search the web for the given query and return the results."""
    try:
        response= search_tool_wrapper.run(query)
        return response
    except Exception as ex:
        print(f"Error occurred while searching the web: {ex}")
        return "No results found."
    
search_agent= AssistantAgent(
    name="SearchAgent",
    model_client=model_client,
    description="An agent that can search the web for information.",
    system_message="You are a helpful assistant that can search the web for information using the search_web tool.",
    # "Please make sure that you use the search_web tool to find information before you return the answer.",
    tools=[search_web],
    reflect_on_tool_use=True
)

async def run_serper_search():
    """Run the search agent with a sample query."""
    task= "who won the IPL in 2025"
    print(f"Querying: {task}")

    response= await search_agent.run(task=task)
    print(response.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(run_serper_search())