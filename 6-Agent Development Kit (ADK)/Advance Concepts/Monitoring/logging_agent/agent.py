import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler("agent_logs.log", mode="a"),   # Log to file
        logging.StreamHandler()                  # Also log to console
    ],
    force=True
)

# Example: ADK agent usage

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

logging.info("Root agent initialized successfully")