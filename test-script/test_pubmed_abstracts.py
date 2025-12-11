#!/usr/bin/env python3
"""Test that PubMed now returns full abstracts."""

from src.tools.implementations import search_pubmed

def test_pubmed_abstracts():
    """Test PubMed abstract retrieval."""
    print("Testing PubMed abstract retrieval...\n")
    
    result = search_pubmed("T-cell exhaustion gene signature", max_results=3)
    
    if not result.success:
        print(f"ERROR: {result.error}")
        return False
    
    articles = result.output
    print(f"Found {len(articles)} articles\n")
    
    for i, article in enumerate(articles, 1):
        print(f"Article {i}:")
        print(f"  PMID: {article['pmid']}")
        print(f"  Title: {article['title'][:80]}...")
        print(f"  Authors: {', '.join(article['authors'])}")
        print(f"  Date: {article['pubdate']}")
        
        abstract = article['abstract']
        if abstract == "N/A":
            print(f"  Abstract: ❌ NOT AVAILABLE")
        else:
            print(f"  Abstract: ✅ Available ({len(abstract)} chars)")
            print(f"    Preview: {abstract[:200]}...")
        print()
    
    # Check if we got real abstracts
    real_abstracts = sum(1 for a in articles if a['abstract'] != "N/A" and len(a['abstract']) > 50)
    print(f"\n{'✅ SUCCESS' if real_abstracts > 0 else '❌ FAILED'}: {real_abstracts}/{len(articles)} articles have full abstracts")
    
    return real_abstracts > 0

if __name__ == "__main__":
    test_pubmed_abstracts()
