from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='search_agent',
    tools=[google_search],  # Using a custom tool
    description='An assistant that helps with Query and search internet when needed.',
    # change instruction to reflect google_search tool
    instruction='''
        You are a helpful Search assistant.
        When the user asks about current events or factual information, use the google_search tool.
        Always return a clear, short explanation.
    '''
)
