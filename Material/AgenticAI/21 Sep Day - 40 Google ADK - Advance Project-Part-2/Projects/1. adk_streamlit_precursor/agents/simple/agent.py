import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


# This agent can answer general questions and will use Tavily MCP to search when needed.
# It is intentionally simple for teaching: one agent, one toolset.

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY is None:
    raise ValueError("TAVILY_API_KEY is not set")


tavily_tools =   MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y", "tavily-mcp"],
                env={
                    'TAVILY_API_KEY':TAVILY_API_KEY
                },
            )
        )

root_agent = Agent(
    model="gemini-2.0-flash",
    name="simple",
    instruction="""
You are a helpful Q&A assistant.

RULES:
1) For any factual, time-sensitive, or non-trivial question, you MUST first call an MCP web-search tool
   (from the available Tavily tools) using the user’s question as the query (or a focused reformulation).
2) After the tool returns results, synthesize a clear 3–6 sentence answer grounded in those results.
3) Briefly cite sources inline (domain or title is fine). Do NOT answer without using the tool unless the
   user explicitly says "no search".
""".strip(),
    tools=[tavily_tools],
)
