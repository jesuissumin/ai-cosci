"""Test internet search functionality for search_literature tool."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.implementations import search_literature
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_internet_search():
    """Test internet search with minimal query."""
    print("\n" + "="*60)
    print("Testing Internet Search (Semantic Scholar + PubMed)")
    print("="*60)
    print(f"PAPERQA_LLM: {os.getenv('PAPERQA_LLM')}")
    print(f"PAPERQA_EMBEDDING: {os.getenv('PAPERQA_EMBEDDING')}")
    print("Note: This will use API credits but with minimal sources\n")

    result = search_literature(
        question="What is PD-1 checkpoint inhibitor?",
        mode="online",
        max_sources=2  # Minimal sources to save credits
    )

    print(f"\nSuccess: {result.success}")
    if result.success:
        print(f"\nAnswer preview: {result.output['answer'][:300]}...")
        print(f"\nSources used: {result.output['sources_used']}")
        print(f"Number of contexts: {len(result.output['contexts'])}")

        # Show which papers were found
        if result.output['contexts']:
            print("\nPapers found:")
            seen_citations = set()
            for ctx in result.output['contexts'][:5]:
                citation = ctx.get('citation', 'Unknown')
                if citation not in seen_citations:
                    print(f"  - {citation}")
                    seen_citations.add(citation)
    else:
        print(f"Error: {result.error}")

    return result.success

if __name__ == "__main__":
    success = test_internet_search()
    sys.exit(0 if success else 1)
