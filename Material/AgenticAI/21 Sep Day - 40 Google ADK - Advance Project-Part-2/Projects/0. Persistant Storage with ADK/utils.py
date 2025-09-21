from google.genai import types

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"

    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"


async def display_state_async(session_service, app_name, user_id, session_id, label="State"):
    """
    Pretty-print current session state (ASYNC):
      - user_name
      - reading_list (index, title, status, tags, url, notes)
    """
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        st = session.state or {}
        print(f"\n{'-' * 12} {label} {'-' * 12}")

        user_name = st.get("user_name", "") or "Unknown"
        print(f"👤 User: {user_name}")

        items = st.get("reading_list", [])
        if not items:
            print("📚 Reading List: [empty]")
        else:
            print("📚 Reading List:")
            for i, it in enumerate(items, 1):
                title = it.get("title", "(untitled)")
                status = it.get("status", "queued")
                tags = ", ".join(it.get("tags", []) or [])
                url = it.get("url", "")
                notes = it.get("notes", "")
                print(f"  {i}. {title}  [{status}]")
                if url:
                    print(f"     URL: {url}")
                if tags:
                    print(f"     Tags: {tags}")
                if notes:
                    print(f"     Notes: {notes}")

        print("-" * (26 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """
    Stream and log events from the runner.
    Returns the final response text if the event is the final response.
    """
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Show helpful parts for debugging (tool outputs, text, code, etc.)
    if event.content and event.content.parts:
        for part in event.content.parts:
            if getattr(part, "text", None):
                txt = (part.text or "").strip()
                if txt:
                    print(f"  Text: '{txt}'")
            if getattr(part, "tool_response", None):
                print(f"  Tool Response: {part.tool_response.output}")
            if getattr(part, "executable_code", None):
                print("  Executable Code:\n", part.executable_code.code)
            if getattr(part, "code_execution_result", None):
                cer = part.code_execution_result
                print(f"  Code Result: {cer.outcome}\n{cer.output}")

    # Final response banner
    if event.is_final_response():
        final_text = ""
        if event.content and event.content.parts and getattr(event.content.parts[0], "text", None):
            final_text = (event.content.parts[0].text or "").strip()

        if final_text:
            print(
                f"\n{Colors.BG_BLUE}{Colors.BLACK}{Colors.BOLD}╔══ AGENT RESPONSE ════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_text}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.BLACK}{Colors.BOLD}╚═══════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.BLACK}{Colors.BOLD}==> Final Agent Response: [No text in final event]{Colors.RESET}\n"
            )
        return final_text

    return None


async def call_agent_async(runner, user_id, session_id, query: str):
    """
    Convenience helper to send a query to the agent.
    NOTE: State printing moved to the caller so we can await both sides cleanly.
    """
    content = types.Content(role="user", parts=[types.Part(text=query)])

    print(f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}")

    final_response_text = None
    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            maybe_text = await process_agent_response(event)
            if maybe_text:
                final_response_text = maybe_text
    except Exception as e:
        print(f"Error during agent call: {e}")

    return final_response_text
