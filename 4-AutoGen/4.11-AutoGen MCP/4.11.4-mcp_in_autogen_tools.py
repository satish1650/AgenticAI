import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key= os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.") 

async def main():   
    params= StdioServerParams(
        command="uvx",
        args=['mcp-server-time','--local-timezone=America/New_York']
    )

    model= OpenAIChatCompletionClient(
        api_key=api_key,
        model="gpt-4o",
    )
    
    async with McpWorkbench(server_params=params) as workbench:
        tools = await workbench.list_tools()
        print(tools)

        # agent= AssistantAgent(
        #     name="Agent",
        #     system_message="You are a helpful assistant.",
        #     model_client=model,
        #     workbench=workbench,
        #     reflect_on_tool_use=True,
        # ) 

        # task= 'What is the time right now in New Delhi ?'
        # task= 'What is the time right now in London ?'
    
        # async for message in agent.run_stream(task=task):
        #     print("-"*100)
        #     print(message)
        #     print("-"*100)
            
if (__name__ == "__main__"):
    asyncio.run(main())