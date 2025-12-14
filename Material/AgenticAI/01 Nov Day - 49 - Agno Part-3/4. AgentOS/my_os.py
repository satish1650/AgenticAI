from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb

import os

# Set your API key (replace YOUR_API_KEY with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBQ_pZ37jQiQG1tFGiyfViNrWXOZXjew5U"

db = SqliteDb(db_file="tmp/data.db")

assistant = Agent(
    name="Assistant",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=["You are a helpful AI assistant."],
    markdown=True,
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    session_state={"name":"Mayank"}
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)