import math
from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool

def calculate_area(shape: str, value: float) -> dict:
    """Calculate the area of a simple shape.

    Args:
        shape (str): The type of shape ("circle" or "square").
        value (float): The radius (circle) or side length (square).

    Returns:
        dict: status and result or error msg.
    """
    if shape.lower() == "circle":
        area = math.pi * value * value
        return {"status": "success", "report": f"The area of the circle is {area:.2f}"} # make sure return is well defined.
    elif shape.lower() == "square":
        area = value * value
        return {"status": "success", "report": f"The area of the square is {area:.2f}"}
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I can only calculate areas for circles and squares, not {shape}.",
        }
    
root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    tools=[calculate_area],  # Using a custom tool
    description='An assistant that helps with simple math problems.',
    instruction='''You are a helpful math assistant.
        When the user asks about the area of a shape, use the calculate_area tool.
        Always return a clear, short explanation.
    '''
)
