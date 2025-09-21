import asyncio
import os

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService,InMemorySessionService

from memory_agent.agent import root_agent
from utils import call_agent_async, display_state_async

load_dotenv()

reading_agent = root_agent

# ===== PART 1: Initialize Persistent Session Service =====
DB_URL = os.getenv("ADK_DB_URL", "sqlite:///./reading_list.db")
session_service = DatabaseSessionService(db_url=DB_URL)

# ===== PART 2: Initial State (first run) =====
INITIAL_STATE = {
    "user_name": "",
    "reading_list": [],
}

# ===== PART 3: App/User identifiers =====
APP_NAME = os.getenv("ADK_APP_NAME", "Reading List Curator")
USER_ID = os.getenv("ADK_USER_ID", "demo_user")


async def main_async():
    # ===== PART 4: Find-or-create session (AWAIT these calls) =====
    existing = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
    if getattr(existing, "sessions", None):
        SESSION_ID = existing.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=INITIAL_STATE,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # ===== PART 5: Build a Runner =====
    runner = Runner(
        agent=reading_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 6: Simple terminal loop =====
    print("\nWelcome to the Reading List Curator!")
    print("I remember your reading list across sessions. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye! Your reading list has been saved.")
            break

        # (Optional) show state before each turn
        await display_state_async(session_service, APP_NAME, USER_ID, SESSION_ID, "State BEFORE")

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

        # (Optional) show state after each turn
        await display_state_async(session_service, APP_NAME, USER_ID, SESSION_ID, "State AFTER")


if __name__ == "__main__":
    asyncio.run(main_async())
