import os
import sys
import argparse

from dotenv import load_dotenv

import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from multi_tool_bot.agent import root_agent


def create_remote_agent():
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

    print(f'✅ Created remote agent with ID: {remote_app.resource_name}')


def create_remote_session(resource_id: str, user_id: str):
    remote_app = agent_engines.get(
        resource_name=f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/{os.getenv("GOOGLE_CLOUD_LOCATION")}/reasoningEngines/{resource_id}'
    )
    remote_session = remote_app.create_session(user_id=user_id)
    print(f'✅ Created remote session with ID: {remote_session}')


def list_deployments():
    deployments = agent_engines.list()
    for deployment in deployments:
        print(f'Deployment ID: {deployment.resource_name}')


def send_message(resource_id: str, session_id: str, message: str, user_id: str):
    
    remote_app = agent_engines.get(
        resource_name=f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/{os.getenv("GOOGLE_CLOUD_LOCATION")}/reasoningEngines/{resource_id}'
    )
    for event in remote_app.stream_query(
        user_id=user_id,
        session_id=session_id,
        message=message,
    ):
        print(event)


def delete_agent(resource_id: str):
    remote_app = agent_engines.get(
        resource_name=f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/{os.getenv("GOOGLE_CLOUD_LOCATION")}/reasoningEngines/{resource_id}'
    )
    remote_app.delete()
    print(f'🗑️ Deleted agent: {resource_id}')


def main():
    load_dotenv()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    bucket_name = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")

    if not project_id or not location or not bucket_name:
        print("❌ Missing required environment variables. Please check your .env file.")
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket_name,
    )

    parser = argparse.ArgumentParser(description="Vertex AI Remote Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create-agent
    subparsers.add_parser("create-agent", help="Create a new remote agent")

    # create-session
    parser_create_session = subparsers.add_parser("create-session", help="Create a session for a remote agent")
    parser_create_session.add_argument("--resource-id", required=True, help="Remote agent resource ID")
    parser_create_session.add_argument("--user-id", default="test_user_123", help="User ID")

    # send-message
    parser_send = subparsers.add_parser("send-message", help="Send a message to the remote agent session")
    parser_send.add_argument("--resource-id", required=True, help="Remote agent resource ID")
    parser_send.add_argument("--session-id", required=True, help="Session ID")
    parser_send.add_argument("--message", required=True, help="Message to send")
    parser_send.add_argument("--user-id", default="test_user_123", help="User ID")

    # list-deployments
    subparsers.add_parser("list-deployments", help="List all remote agent deployments")

    # delete-agent
    parser_delete = subparsers.add_parser("delete-agent", help="Delete a remote agent")
    parser_delete.add_argument("--resource-id", required=True, help="Remote agent resource ID to delete")

    args = parser.parse_args()

    if args.command == "create-agent":
        create_remote_agent()

    elif args.command == "create-session":
        create_remote_session(args.resource_id, args.user_id)

    elif args.command == "send-message":
        send_message(args.resource_id, args.session_id, args.message, args.user_id)

    elif args.command == "list-deployments":
        list_deployments()

    elif args.command == "delete-agent":
        delete_agent(args.resource_id)


if __name__ == "__main__":
    main()
