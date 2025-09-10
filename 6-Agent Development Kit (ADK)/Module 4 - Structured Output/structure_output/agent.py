from google.adk.agents.llm_agent import LlmAgent
from pydantic import BaseModel, Field

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='"""You are a Capital Information Agent. Given a country, ' \
    'respond ONLY with a JSON object containing the capital. ' \
    'Format: {"capital": "capital_name"}"""',
    output_key="Capital",
    output_schema=CapitalOutput
)
