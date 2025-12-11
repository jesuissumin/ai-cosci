#!/usr/bin/env python3
"""Test the new find_files tool for efficient file discovery."""

from src.tools.implementations import find_files
from src.config import get_default_config
import os

def test_find_files():
    """Test file discovery tool."""
    # Get configuration from .env
    config = get_default_config()
    
    print("=" * 60)
    print("Testing find_files tool")
    print("=" * 60)
    print(f"Workspace: {os.getcwd()}")
    print(f"Database Dir: {config.database_dir}")
    print(f"Input Dir: {config.input_dir}")
    
    # Test 1: Find CSV files related to T-cell exhaustion question
    print("\n1. Smart search based on question context:")
    print("-" * 60)
    result = find_files(
        question_context="T-cell exhaustion gene signature differential expression",
        workspace_root=".",
        data_dir=config.database_dir
    )
    
    if result.success:
        output = result.output
        print(f"✅ Found {output['total_files']} relevant files")
        print("\nTop files:")
        for i, file in enumerate(output['files'][:10], 1):
            print(f"  {i}. {file['name']}")
            print(f"     Path: {file['path']}")
            print(f"     Type: {file['type']}, Size: {file['size_mb']} MB")
    else:
        print(f"❌ Error: {result.error}")
    
    # Test 2: Find all CSV files
    print("\n\n2. Find all CSV files:")
    print("-" * 60)
    result = find_files(
        extension="csv",
        workspace_root=".",
        data_dir=config.database_dir
    )
    
    if result.success:
        print(f"✅ Found {result.output['total_files']} CSV files")
    else:
        print(f"❌ Error: {result.error}")
    
    # Test 3: Find files with 'DEG' in the name
    print("\n\n3. Find files with 'DEG' in name:")
    print("-" * 60)
    result = find_files(
        name_contains="DEG",
        workspace_root=".",
        data_dir=config.database_dir
    )
    
    if result.success:
        output = result.output
        print(f"✅ Found {output['total_files']} files with 'DEG'")
        for file in output['files']:
            print(f"  - {file['name']}")
    else:
        print(f"❌ Error: {result.error}")
    
    # Test 4: Pattern matching
    print("\n\n4. Pattern match: **/Q5/*.csv")
    print("-" * 60)
    result = find_files(
        pattern="**/Q5/*.csv",
        workspace_root=".",
        data_dir=config.database_dir
    )
    
    if result.success:
        output = result.output
        print(f"✅ Found {output['total_files']} files matching pattern")
        for file in output['files']:
            print(f"  - {file['name']}")
    else:
        print(f"❌ Error: {result.error}")
    
    print("\n" + "=" * 60)
    print("File discovery test complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_find_files()
