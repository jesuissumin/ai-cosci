#!/usr/bin/env python3
"""Test script for database query tools."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.implementations import query_database, ToolResult


def test_database(db_name: str, query: str):
    """Test a database query."""
    print(f"\n{'='*60}")
    print(f"Testing {db_name.upper()} database")
    print(f"Query: {query}")
    print(f"{'='*60}")

    result = query_database(db_name, query, limit=5)

    if result.success:
        print("✓ Query successful!")
        print(f"\nResult:")
        import json
        print(json.dumps(result.output, indent=2, default=str)[:2000])  # Limit output
        if len(json.dumps(result.output, default=str)) > 2000:
            print("\n... (truncated)")
    else:
        print(f"✗ Query failed: {result.error}")


def main():
    """Run database tests."""
    print("\n" + "="*60)
    print("CoScientist Database Tool Test")
    print("="*60)

    # Test 1: Get info from each database
    print("\n\nPhase 1: Testing database info queries")
    print("-" * 60)

    for db in ["bindingdb", "drugbank", "pharos", "gwas", "string"]:
        test_database(db, "info")

    # Test 2: Query specific data
    print("\n\nPhase 2: Testing specific data queries")
    print("-" * 60)

    # Test DrugBank interactions
    test_database("drugbank", "file:interactions")

    # Test Pharos drugs
    test_database("pharos", "file:pharos_drugs")

    # Test STRING protein info
    test_database("string", "file:sapiens.9606.protein.info.v12.0")

    print("\n\n" + "="*60)
    print("Database tool tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
