#!/usr/bin/env python
import sys
import warnings
import time
import json
from datetime import datetime

from agentic_rag.crew import AgenticRag

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    print("\n" + "="*50)
    print("Starting CrewAI RAG System...")
    print("="*50)

    query = 'Who is Elon musk and what is his net worth?'
    print(f"\nProcessing query: '{query}'")
    print("-"*50)

    inputs = {
        'query': query
    }

    try:
        print("\nInitializing crew and executing query...")
        result = AgenticRag().crew().kickoff(inputs=inputs)
        
        print("\nRESULTS:")
        print("-"*50)
        print(result)
        print("\n" + "="*50)
        print("Execution completed successfully!")
        print("="*50 + "\n")
        
        return result

    except Exception as e:
        print("\nERROR:")
        print("-"*50)
        print(f"An error occurred while running the crew: {e}")
        print("\n" + "="*50)
        raise





if __name__ == "__main__":
    run()
