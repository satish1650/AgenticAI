import os
import sys


import vertexai

from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from dotenv import load_dotenv

from multi_tool_bot.agent import root_agent


def create_remote_agent() -> None:
    
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True
    )

    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
        ],
        extra_packages=["./multi_tool_bot"],
    )

    print(f'Created remote agent with ID: {remote_app.resource_name}')

# https://us-central1-aiplatform.googleapis.com/v1/projects/geminikeyn8n/locations/us-central1/reasoningEngines/566771855839461376:query

def create_remote_session(resource_id:str,user_id:str):
    remote_app = agent_engines.get(resource_name='projects/479047999858/locations/us-central1/reasoningEngines/566771855839461376')

    remote_sessions=remote_app.create_session(user_id=user_id)
    print(f'Created remote session with ID: {remote_sessions}')


def list_deployments():
    deployments = agent_engines.list()
    for deployment in deployments:
        print(f'Deployment ID: {deployment.resource_name}')
    


def send_message(resource_id:str,session_id:str,message:str):
    remote_app = agent_engines.get(resource_name='projects/479047999858/locations/us-central1/reasoningEngines/566771855839461376')

    for event in remote_app.stream_query(
        user_id="test_user_123",
        session_id="3732740271473950720",
        message="What is the weather in New York?",
    ):
        print(event)


def delete_agent(resource_id:str):
    remote_app = agent_engines.

def main(argv=None):
   
    # if (args) is None:
    #     args=flags.FLAGS(sys.argv)
    # else:
    #     argv=flags.FLAGS(argv)

    load_dotenv()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    bucket_name = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket_name:
        print("Missing required environment variable: GOOGLE_CLOUD_STAGING_BUCKET")
        return

    print("Using the following configuration:")
    print(f"Project ID: {project_id}")
    print(f"Location: {location}")
    print(f"Staging Bucket: {bucket_name}")

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket_name,
    )

    # print("Creating remote agent...")
    # create_remote_agent()
    # print("Remote agent created successfully.")

    # list_deployments()
    # create_remote_session("566771855839461376","test_user_123")


    send_message("566771855839461376","3732740271473950720","Hi how are you, what all can you do for me?")

if __name__ == "__main__":
    main(sys.argv)