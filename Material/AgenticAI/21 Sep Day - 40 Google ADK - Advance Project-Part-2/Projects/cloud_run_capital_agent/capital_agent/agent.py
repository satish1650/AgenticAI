""" 
Capital Agent -- minimal ADK agent for Cloud Run demos.

Exposes `root_agent` and relies only on a Gemini model.
The instruction steers toward short, factual answers.
"""
from google.adk.agents.llm_agent import Agent

# Exported variable: root_agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="capital_agent",
    instruction=(
        "You answer concisely. If asked for a country's capital, reply with just the capital name "
        "and a short confirmation (one sentence). If the question is unrelated, answer helpfully in 2-4 sentences."
    ),
)
