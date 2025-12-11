#!/usr/bin/env python3
"""
Test script for PaperQA integration.

This script tests:
1. Configuration system
2. Tool registration
3. search_literature tool (without actual API calls)
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all necessary modules can be imported."""
    print("Testing imports...")

    try:
        from src.config import get_default_config, create_custom_config
        print("✓ Config module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False

    try:
        from src.tools.implementations import search_literature, get_tool_definitions
        print("✓ search_literature function imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import search_literature: {e}")
        return False

    try:
        from src.agent.agent import BioinformaticsAgent
        print("✓ Agent module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import agent: {e}")
        return False

    return True


def test_configuration():
    """Test configuration system."""
    print("\nTesting configuration system...")

    from src.config import get_default_config, create_custom_config, DataConfig

    # Test default config
    try:
        config = get_default_config()
        print(f"✓ Default config loaded")
        print(f"  - Database dir: {config.database_dir}")
        print(f"  - Input dir: {config.input_dir}")
        print(f"  - Paper library dir: {config.paper_library_dir}")
        print(f"  - PaperQA LLM: {config.paperqa_llm}")
        print(f"  - PaperQA embedding: {config.paperqa_embedding}")
    except Exception as e:
        print(f"✗ Failed to load default config: {e}")
        return False

    # Test custom config
    try:
        custom_config = create_custom_config(
            paper_library_dir="./test_papers",
            paperqa_max_sources=10
        )
        print(f"✓ Custom config created")
        print(f"  - Paper library dir: {custom_config.paper_library_dir}")
        print(f"  - Max sources: {custom_config.paperqa_max_sources}")
    except Exception as e:
        print(f"✗ Failed to create custom config: {e}")
        return False

    return True


def test_tool_definitions():
    """Test that search_literature is in tool definitions."""
    print("\nTesting tool definitions...")

    from src.tools.implementations import get_tool_definitions

    tool_defs = get_tool_definitions()
    tool_names = [tool["function"]["name"] for tool in tool_defs]

    print(f"Available tools: {', '.join(tool_names)}")

    if "search_literature" in tool_names:
        print("✓ search_literature found in tool definitions")

        # Find and display the definition
        lit_tool = next(t for t in tool_defs if t["function"]["name"] == "search_literature")
        print(f"  - Description: {lit_tool['function']['description'][:100]}...")
        print(f"  - Parameters: {list(lit_tool['function']['parameters']['properties'].keys())}")
        return True
    else:
        print("✗ search_literature NOT found in tool definitions")
        return False


def test_agent_integration():
    """Test that agent has access to search_literature."""
    print("\nTesting agent integration...")

    try:
        from src.agent.agent import BioinformaticsAgent

        # Create agent (without API key, just to test tool registration)
        # This will fail when making actual API calls, but that's ok for this test
        agent = BioinformaticsAgent(
            api_key="test_key",
            provider="anthropic"
        )

        if "search_literature" in agent.tools:
            print("✓ search_literature registered in agent.tools")
            print(f"  - Total tools: {len(agent.tools)}")
            print(f"  - Tools: {', '.join(agent.tools.keys())}")
            return True
        else:
            print("✗ search_literature NOT in agent.tools")
            print(f"  - Available tools: {', '.join(agent.tools.keys())}")
            return False

    except Exception as e:
        print(f"✗ Failed to create agent: {e}")
        return False


def test_search_literature_signature():
    """Test search_literature function signature."""
    print("\nTesting search_literature function signature...")

    from src.tools.implementations import search_literature
    import inspect

    sig = inspect.signature(search_literature)
    params = list(sig.parameters.keys())

    print(f"✓ Function signature: search_literature({', '.join(params)})")

    expected_params = ["question", "mode", "paper_dir", "max_sources"]
    missing = set(expected_params) - set(params)

    if missing:
        print(f"✗ Missing expected parameters: {missing}")
        return False
    else:
        print("✓ All expected parameters present")
        return True


def test_paperqa_import():
    """Test that PaperQA can be imported."""
    print("\nTesting PaperQA installation...")

    try:
        import paperqa
        print(f"✓ PaperQA imported successfully")
        print(f"  - Version: {paperqa.__version__}")
        return True
    except ImportError as e:
        print(f"✗ PaperQA not installed: {e}")
        print("  Run: pip install paper-qa")
        return False


def test_mock_search():
    """Test search_literature with no PDFs (should handle gracefully)."""
    print("\nTesting search_literature error handling...")

    from src.tools.implementations import search_literature

    # Test with non-existent directory (should fail gracefully)
    result = search_literature(
        question="Test question",
        mode="local",
        paper_dir="/nonexistent/directory"
    )

    if not result.success:
        print(f"✓ Correctly handles missing directory")
        print(f"  - Error message: {result.error[:100]}...")
        return True
    else:
        print(f"✗ Should have failed with missing directory")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("PaperQA Integration Test Suite")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Tool Definitions Test", test_tool_definitions),
        ("Agent Integration Test", test_agent_integration),
        ("Function Signature Test", test_search_literature_signature),
        ("PaperQA Installation Test", test_paperqa_import),
        ("Error Handling Test", test_mock_search),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
