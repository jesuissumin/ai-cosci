#!/usr/bin/env python3
"""Test that search_literature prioritizes local PDFs before online search."""

from src.tools.implementations import search_literature
from src.config import get_default_config

def test_literature_priority():
    """Test literature search prioritization."""
    config = get_default_config()
    
    print("=" * 70)
    print("Testing search_literature - Local PDF Prioritization")
    print("=" * 70)
    print(f"Local PDF library: {config.paper_library_dir}")
    print()
    
    # Test question about T-cell exhaustion
    question = "What are the key transcription factors that drive T-cell exhaustion?"
    
    print(f"Question: {question}")
    print()
    print("Mode: 'auto' (default - prioritize local, supplement with online)")
    print("-" * 70)
    
    result = search_literature(
        question=question,
        mode="auto",
        max_sources=3
    )
    
    if result.success:
        output = result.output
        print(f"\n✅ Search completed!")
        print(f"\nSources used: {output['sources_used']}")
        print(f"Search mode: {output['mode']}")
        print(f"\nAnswer preview:")
        print(f"{output['answer'][:300]}...")
        print(f"\nNumber of contexts: {len(output['contexts'])}")
        
        if output['mode'] == 'local':
            print("\n🎯 SUCCESS: Local PDFs were sufficient - no online search needed!")
        elif output['mode'] in ['online', 'hybrid']:
            print("\n📡 Online search was used (local PDFs may not have covered this topic)")
            
    else:
        print(f"\n❌ Error: {result.error}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_literature_priority()
