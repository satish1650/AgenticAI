from langgraph.graph import StateGraph, END
from langgraph.types import Command

# Define shared state
class MyState(dict):
    pass

# Agent 1
def agent_1(state: MyState) -> MyState:
    print("Agent 1: writing number 5")
    state["number"] = 5
    state["next"] = "agent_2"
    return state

# Agent 2
def agent_2(state: MyState) -> MyState:
    number = state.get("number", 0)
    state["doubled"] = number * 2
    print(f"Agent 2: doubled {number} to {state['doubled']}")
    state["next"] = "agent_3"
    return state

# Agent 3
def agent_3(state: MyState) -> MyState:
    print(f"Agent 3: final result = {state.get('doubled')}")
    state["next"] = "end"
    return state

# Router — as a real node, returning Command
def router_node(state: MyState) -> Command:
    next_node = state.get("next", "end")
    return Command(goto=next_node)

# Build the graph
builder = StateGraph(dict)

# Add all real nodes
builder.add_node("agent_1", agent_1)
builder.add_node("agent_2", agent_2)
builder.add_node("agent_3", agent_3)
builder.add_node("router", router_node)  # ✅ Router is a real node now

# Set entry point
builder.set_entry_point("router")

# Agents go back to the router
builder.add_edge("agent_1", "router")
builder.add_edge("agent_2", "router")
builder.add_edge("agent_3", "router")

# Compile
graph = builder.compile()

# Visualize Graph
print(graph.get_graph().draw_ascii())
# Initial state
initial_state = {"next": "agent_1"}

# Run
final_state = graph.invoke(initial_state)

print("\nFinal State:", final_state)

# Output
'''
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +--------+
  | router |
  +--------+
      *
      *
      *
 +---------+
 | __end__ |
 +---------+
Agent 1: writing number 5
Agent 2: doubled 5 to 10
Agent 3: final result = 10

Final State: {'next': 'end', 'number': 5, 'doubled': 10}
'''