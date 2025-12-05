"""Example usage of the CoScientist agent."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.agent import create_agent


def main():
    """Run example queries with the agent."""
    load_dotenv()

    agent = create_agent()

    # Example questions
    questions = [
        "What databases would be most useful for drug repositioning based on gene signatures?",
        "How would you design a Python pipeline to analyze protein-ligand binding data from BindingDB?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*70}")
        print(f"Question {i}: {question}")
        print(f"{'='*70}\n")

        response = agent.run(question, verbose=True)

        print(f"\n{'='*70}")
        print("FINAL ANSWER:")
        print(f"{'='*70}")
        print(response)
        print()


if __name__ == "__main__":
    main()
