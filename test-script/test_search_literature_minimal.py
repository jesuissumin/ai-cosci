"""Minimal test for search_literature tool with both local and internet modes."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.implementations import search_literature
from dotenv import load_dotenv

# Load environment
load_dotenv()


def test_local_search():
    """Test local PDF search with minimal query."""
    print("\n" + "="*60)
    print("TEST 1: Local PDF Search (tcell paper)")
    print("="*60)

    result = search_literature(
        question="What is T-cell exhaustion?",
        mode="local",
        max_sources=2  # Limit sources to minimize processing
    )

    print(f"\nSuccess: {result.success}")
    if result.success:
        print(f"Answer: {result.output['answer'][:200]}...")  # First 200 chars
        print(f"Sources used: {result.output['sources_used']}")
        print(f"Number of contexts: {len(result.output['contexts'])}")
    else:
        print(f"Error: {result.error}")

    return result.success


def test_internet_search():
    """Test internet search with minimal query."""
    print("\n" + "="*60)
    print("TEST 2: Internet Search (PubMed)")
    print("="*60)
    print("Note: This will use API credits but with minimal sources")

    result = search_literature(
        question="What is PD-1?",  # Very simple question
        mode="online",
        max_sources=1  # Minimal sources to save credits
    )

    print(f"\nSuccess: {result.success}")
    if result.success:
        print(f"Answer: {result.output['answer'][:200]}...")  # First 200 chars
        print(f"Sources used: {result.output['sources_used']}")
        print(f"Number of contexts: {len(result.output['contexts'])}")
    else:
        print(f"Error: {result.error}")

    return result.success


if __name__ == "__main__":
    print("Testing search_literature with minimal credit usage")
    print(f"PAPERQA_LLM: {os.getenv('PAPERQA_LLM')}")
    print(f"PAPERQA_EMBEDDING: {os.getenv('PAPERQA_EMBEDDING')}")

    # Test local first (no API credits used for processing local PDFs)
    local_ok = test_local_search()

    # Ask before testing internet
    if local_ok:
        print("\n" + "="*60)
        response = input("Local search worked! Test internet search? (y/n): ")
        if response.lower() == 'y':
            test_internet_search()
        else:
            print("Skipping internet search test.")
    else:
        print("\nLocal search failed. Fix the issue before testing internet search.")
