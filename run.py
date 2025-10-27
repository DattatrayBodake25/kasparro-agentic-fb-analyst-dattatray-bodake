"""
Main entry point for the Agentic Facebook Performance Analyst system.

Usage:
    python run.py "Analyze ROAS drop"

This script serves as a CLI wrapper for the orchestrator module.
It loads configuration, initializes the orchestrator, and executes the full agentic workflow.
"""

import sys
import traceback
from src.orchestrator import main


def run():
    """Execute the full pipeline with the provided query."""
    try:
        if len(sys.argv) < 2:
            print("Usage: python run.py \"<query>\"")
            print("Example: python run.py \"Analyze ROAS drop\"")
            sys.exit(1)

        query = " ".join(sys.argv[1:])
        print("\n=== Starting Agentic Facebook Analyst System ===\n")
        main(query)
        print("\n=== Execution Completed Successfully ===\n")

    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        sys.exit(1)

    except Exception as exc:
        print("\nError: An unexpected exception occurred during execution.")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run()
