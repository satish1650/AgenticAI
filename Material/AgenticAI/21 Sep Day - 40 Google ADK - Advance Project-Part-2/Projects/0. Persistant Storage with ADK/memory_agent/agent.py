from typing import List, Optional

from google.adk.agents import LlmAgent,Agent
from google.adk.tools.tool_context import ToolContext

from dotenv import load_dotenv

# Ensure .env is loaded when running via CLI (python main.py)
load_dotenv()


# -----------------------------
# Helpers
# -----------------------------
def _ensure_state(tool_context: ToolContext) -> None:
    """Guarantee required keys exist in state."""
    st = tool_context.state
    if "user_name" not in st or st["user_name"] is None:
        st["user_name"] = ""
    if "reading_list" not in st or st["reading_list"] is None:
        st["reading_list"] = []


def _normalize_tags(tags: Optional[List[str]]) -> List[str]:
    """Return a clean list of tag strings."""
    if not tags:
        return []
    return [str(t).strip() for t in tags if str(t).strip()]


def _valid_status(status: Optional[str]) -> bool:
    return status in {None, "queued", "reading", "done"}


# -----------------------------
# Tools (CRUD for reading_list)
# -----------------------------
def set_user_name(name: str, tool_context: ToolContext) -> dict:
    """
    Set the user's display name in persistent state.
    """
    _ensure_state(tool_context)
    old = tool_context.state.get("user_name", "")
    tool_context.state["user_name"] = name or ""
    return {
        "action": "set_user_name",
        "old_name": old,
        "new_name": tool_context.state["user_name"],
        "message": f"Saved your name as '{tool_context.state['user_name'] or 'Unknown'}'.",
    }


def add_item(
    title: str,
    url: str,
    tags: Optional[List[str]],
    status: str,
    notes: str, 
    tool_context: ToolContext,
) -> dict:
    """
    Add a new entry to the reading list.

    Fields:
      - title  (required)
      - url    (optional)
      - tags   (optional list[str])
      - status (queued|reading|done; default 'queued')
      - notes  (optional)
    """
    _ensure_state(tool_context)
    if not _valid_status(status):
        status = "queued"

    item = {
        "title": title.strip() if title else "(untitled)",
        "url": (url or "").strip(),
        "tags": _normalize_tags(tags),
        "status": status,
        "notes": (notes or "").strip(),
    }
    rl = tool_context.state["reading_list"]
    rl.append(item)
    tool_context.state["reading_list"] = rl  # write-through

    return {
        "action": "add_item",
        "item": item,
        "index": len(rl),  # 1-based index for user clarity
        "message": f"Added '{item['title']}' to your reading list.",
    }


def list_items(
    filter_status: Optional[str] = None,
    filter_tag: Optional[str] = None,
    tool_context: ToolContext = None,
) -> dict:
    """
    Return the reading list, optionally filtered by status or tag.
    """
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    filtered = []
    for it in rl:
        if filter_status and it.get("status") != filter_status:
            continue
        if filter_tag and (filter_tag not in it.get("tags", [])):
            continue
        filtered.append(it)

    return {
        "action": "list_items",
        "count": len(filtered),
        "items": filtered,
        "filters": {"status": filter_status, "tag": filter_tag},
        "message": f"Found {len(filtered)} item(s).",
    }


def update_item(
    index: int,
    title: Optional[str] = None,
    url: Optional[str] = None,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    tags: Optional[List[str]] = None,
    tool_context: ToolContext = None,
) -> dict:
    """
    Update fields of an existing reading-list item (1-based index).

    Any field left as None will remain unchanged.
    """
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    if index < 1 or index > len(rl):
        return {
            "action": "update_item",
            "status": "error",
            "message": f"No item at position {index}. You currently have {len(rl)} item(s).",
        }

    item = rl[index - 1]
    before = item.copy()

    if title is not None:
        item["title"] = title.strip() or item["title"]
    if url is not None:
        item["url"] = (url or "").strip()
    if _valid_status(status):
        if status is not None:
            item["status"] = status
    if notes is not None:
        item["notes"] = (notes or "").strip()
    if tags is not None:
        item["tags"] = _normalize_tags(tags)

    rl[index - 1] = item
    tool_context.state["reading_list"] = rl

    return {
        "action": "update_item",
        "index": index,
        "before": before,
        "after": item,
        "message": f"Updated item {index} ('{before.get('title','')}').",
    }


def annotate_item(
    index: int,
    notes: str,
    tool_context: ToolContext,
) -> dict:
    """
    Append or set notes for an item (1-based index).
    """
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    if index < 1 or index > len(rl):
        return {
            "action": "annotate_item",
            "status": "error",
            "message": f"No item at position {index}. You currently have {len(rl)} item(s).",
        }

    item = rl[index - 1]
    before_notes = item.get("notes", "")
    item["notes"] = (notes or "").strip()
    rl[index - 1] = item
    tool_context.state["reading_list"] = rl

    return {
        "action": "annotate_item",
        "index": index,
        "old_notes": before_notes,
        "new_notes": item["notes"],
        "message": f"Noted item {index} ('{item.get('title','')}').",
    }


def remove_item(index: int, tool_context: ToolContext) -> dict:
    """
    Remove a reading-list item (1-based index).
    """
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]

    if index < 1 or index > len(rl):
        return {
            "action": "remove_item",
            "status": "error",
            "message": f"No item at position {index}. You currently have {len(rl)} item(s).",
        }

    removed = rl.pop(index - 1)
    tool_context.state["reading_list"] = rl

    return {
        "action": "remove_item",
        "index": index,
        "removed": removed,
        "message": f"Removed '{removed.get('title','')}' from your reading list.",
    }


# -----------------------------
# Agent definition
# -----------------------------
reading_agent = LlmAgent(
    name="reading_list_curator",
    model="gemini-2.0-flash",
    description="Curate a personal reading list with persistent memory.",
    instruction="""
You are a friendly 'Reading List Curator'. The session state contains:
  - user_name: the user's display name (string, may be empty)
  - reading_list: an array of items, each with {title, url, tags[], status, notes}

Your job:
  1) Greet the user (use their name if known).
  2) Understand natural-language requests and call the appropriate tools.
  3) Return a short, helpful summary after tool calls (the tools already return structured data).

Tool selection guidelines:
  - For "add" requests (e.g., "add 'Clean Code' to my list"), call add_item. Extract a concise title.
    If a URL or tags are mentioned, pass them through. Default status is "queued".
  - For "show/list" requests, call list_items. If they mention a status (queued/reading/done) or a tag,
    pass it via the filter arguments. Present results in a clean numbered list.
  - For updates, figure out which item is referenced (by number, 'first', 'last', or title phrase)
    and call update_item with the fields that changed (title/url/status/notes/tags).
  - For notes, use annotate_item.
  - For delete/remove, call remove_item.
  - If the user shares their name, call set_user_name.

Indexing:
  - Treat the user's "first/second/last" or "item 2" as 1-based indices.
  - If you infer an index from context, do not ask clarifying questions—pick the best match.

Formatting:
  - Always keep responses concise and scannable.
  - When listing items, use a numbered list with: Title [status]
    and show URL/tags/notes on subsequent lines only if present.

Be proactive but never fabricate URLs or tags. If something is missing, proceed with what you have.
    """,
    tools=[
        set_user_name,
        add_item,
        list_items,
        update_item,
        annotate_item,
        remove_item,
    ],
)

# Optional alias for ADK web auto-discovery conventions (if you run `adk web -v .`)
root_agent = reading_agent
