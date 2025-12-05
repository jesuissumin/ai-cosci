"""Command-line interface for the bioinformatics agent."""

import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.agent.agent import create_agent


def main():
    """Main CLI entry point."""
    # Load environment variables from .env file
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="CoScientist: AI Research Assistant for Biomedical Questions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ask a single question
  python -m src.cli --question "How can gene signatures guide drug repositioning?"

  # With critic feedback loop for quality validation
  python -m src.cli --question "..." --with-critic

  # Interactive mode
  python -m src.cli --interactive

  # Use a different model
  python -m src.cli --question "..." --model "openai/gpt-4"

  # Verbose output to see tool calls
  python -m src.cli --question "..." --verbose
        """,
    )

    parser.add_argument(
        "--question",
        "-q",
        type=str,
        help="Question to ask the agent",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="anthropic/claude-sonnet-4",
        help="Model to use (default: claude-sonnet-4)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print verbose output with tool calls",
    )
    parser.add_argument(
        "--with-critic",
        "-c",
        action="store_true",
        help="Enable critic feedback loop for quality validation",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenRouter API key (or set OPENROUTER_API_KEY env var)",
    )

    args = parser.parse_args()

    try:
        agent = create_agent(api_key=args.api_key, model=args.model)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.question:
        # Single question mode
        if args.with_critic:
            initial, critique, final = agent.run_with_critic(args.question, verbose=args.verbose)
            print("\n" + "=" * 60)
            print("INITIAL ANSWER:")
            print("=" * 60)
            print(initial)
            print("\n" + "=" * 60)
            print("CRITIC FEEDBACK:")
            print("=" * 60)
            print(critique)
            print("\n" + "=" * 60)
            print("FINAL REFINED ANSWER:")
            print("=" * 60)
            print(final)
        else:
            response = agent.run(args.question, verbose=args.verbose)
            print("\n" + "=" * 60)
            print("Final Answer:")
            print("=" * 60)
            print(response)

    elif args.interactive:
        # Interactive mode
        print("=" * 60)
        print("CoScientist: Interactive Mode")
        print("=" * 60)
        print("Ask biomedical research questions. Type 'exit' or 'quit' to exit.\n")

        while True:
            try:
                question = input("Question: ").strip()
            except EOFError:
                break

            if question.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not question:
                continue

            if args.with_critic:
                initial, critique, final = agent.run_with_critic(question, verbose=args.verbose)
                print("\n" + "=" * 60)
                print("INITIAL ANSWER:")
                print("=" * 60)
                print(initial)
                print("\n" + "=" * 60)
                print("CRITIC FEEDBACK:")
                print("=" * 60)
                print(critique)
                print("\n" + "=" * 60)
                print("FINAL REFINED ANSWER:")
                print("=" * 60)
                print(final)
                print()
            else:
                response = agent.run(question, verbose=args.verbose)
                print("\n" + "=" * 60)
                print("Answer:")
                print("=" * 60)
                print(response)
                print()

    else:
        # No input provided
        parser.print_help()


if __name__ == "__main__":
    main()
