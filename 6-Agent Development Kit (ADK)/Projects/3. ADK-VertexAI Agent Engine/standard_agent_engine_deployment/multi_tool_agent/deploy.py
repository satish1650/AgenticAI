import vertexai
import asyncio
from agent import root_agent # modify this if your agent is not in agent.py

# TODO: Fill in these values for your project
PROJECT_ID = "gen-lang-client-0634579487"
LOCATION = "us-central1"  # For other options, see https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview#supported-regions
STAGING_BUCKET = "gs://your-gcs-bucket-name"

# Initialize the Vertex AI SDK
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

### Prepare the agent for deployment
from vertexai import agent_engines

# Wrap the agent in an AdkApp object
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

### Deploy to agent engine
from vertexai import agent_engines
remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]"   
    ]
)

print(f"Deployment finished!")
print(f"Resource Name: {remote_app.resource_name}")
# Resource Name: "projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"
# Note: The PROJECT_NUMBER is different than the PROJECT_ID.

### Test agent locally (optional)
# Create a local session to maintain conversation history
async def main():
    session = await app.async_create_session(user_id="u_123")
    print("Session created:", session)

    ### Send a query to the agent. Copy-paste the following code to your "deploy.py" python script or a notebook.
    events = []
    async for event in app.async_stream_query(
        user_id="u_123",
        session_id=session.id,
        message="whats the weather in new york",
    ):
        events.append(event)

    # The full event stream shows the agent's thought process
    print("--- Full Event Stream ---")
    for event in events:
        print(event)

    # For quick tests, you can extract just the final text response
    final_text_responses = [
        e for e in events
        if e.get("content", {}).get("parts", [{}])[0].get("text")
        and not e.get("content", {}).get("parts", [{}])[0].get("function_call")
    ]
    if final_text_responses:
        print("\n--- Final Response ---")
        print(final_text_responses[0]["content"]["parts"][0]["text"])

# Run the async main using asyncio
if __name__ == "__main__":
    asyncio.run(main())