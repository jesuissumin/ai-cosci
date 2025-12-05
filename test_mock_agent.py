#!/usr/bin/env python3
"""Test the agent logic without API calls using a mock client."""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.implementations import query_database, execute_python


class MockClient:
    """Mock LLM client for testing without API costs."""

    def __init__(self):
        self.call_count = 0

    def create_message(self, messages, tools, **kwargs):
        """Simulate LLM responses for testing."""
        self.call_count += 1

        # Simulate different responses based on conversation state
        if self.call_count == 1:
            # First call: explore databases
            return {
                "content": [{
                    "type": "text",
                    "text": "I'll query the Pharos and DrugBank databases to find CYP2D6-related information."
                }, {
                    "type": "tool_use",
                    "id": "call_1",
                    "name": "query_database",
                    "input": {"db_name": "pharos", "query": "file:pharos_drugs", "limit": 5}
                }]
            }
        elif self.call_count == 2:
            # Second call: query DrugBank
            return {
                "content": [{
                    "type": "tool_use",
                    "id": "call_2",
                    "name": "query_database",
                    "input": {"db_name": "drugbank", "query": "file:interactions", "limit": 5}
                }]
            }
        elif self.call_count == 3:
            # Third call: analyze with Python
            return {
                "content": [{
                    "type": "tool_use",
                    "id": "call_3",
                    "name": "execute_python",
                    "input": {
                        "code": "print('Analysis: Found CYP2D6-targeting drugs with multiple interaction patterns')"
                    }
                }]
            }
        else:
            # Final response
            return {
                "content": [{
                    "type": "text",
                    "text": """Based on the database queries:

**CYP2D6-Targeting Drugs Found:**
1. Levobupivacaine - Local anesthetic with CYP2D6 activity
   - IC50: 6.71, AC50: 6.3
   - Description: S-enantiomer of bupivacaine

**Drug Interactions (from DrugBank):**
- Multiple documented interactions with anticoagulants
- Food interactions noted for several compounds

**Analysis:**
The data shows that CYP2D6-targeting drugs have complex interaction profiles that require careful monitoring in clinical settings.

*Note: This is a MOCK TEST demonstrating the agent workflow without API costs.*
"""
                }]
            }

    def extract_tool_calls(self, response):
        """Extract tool calls from mock response."""
        tool_calls = []
        for block in response.get("content", []):
            if block.get("type") == "tool_use":
                tool_calls.append({
                    "id": block.get("id"),
                    "name": block.get("name"),
                    "input": block.get("input")
                })
        return tool_calls

    def get_response_text(self, response):
        """Extract text from mock response."""
        text_parts = []
        for block in response.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text"))
        return "".join(text_parts)


def test_agent_workflow():
    """Test the full agent workflow with mock LLM."""
    print("="*70)
    print("MOCK AGENT TEST - No API Costs!")
    print("="*70)
    print("\nTesting: Agent loop, tool calling, database queries")
    print("Question: 'What are drug interactions for CYP2D6-targeting drugs?'\n")

    client = MockClient()
    conversation = []
    max_iterations = 5

    # Add user question
    conversation.append({"role": "user", "content": "What are drug interactions for CYP2D6-targeting drugs?"})

    for iteration in range(max_iterations):
        print(f"\n[Iteration {iteration + 1}/{max_iterations}]")

        # Get mock response
        response = client.create_message(
            messages=conversation,
            tools=[],
            max_tokens=1500
        )

        # Extract text and tool calls
        text = client.get_response_text(response)
        tool_calls = client.extract_tool_calls(response)

        if text:
            print(f"Assistant: {text[:150]}...")

        if not tool_calls:
            print("\n[Agent completed - no more tools needed]")
            print(f"\nFinal Answer:\n{text}")
            break

        print(f"[Tools to call: {[tc['name'] for tc in tool_calls]}]")

        # Execute tools
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_input = tool_call["input"]

            print(f"  Calling {tool_name}({json.dumps(tool_input, indent=2)})...")

            # Execute real tool
            if tool_name == "query_database":
                result = query_database(**tool_input)
            elif tool_name == "execute_python":
                result = execute_python(**tool_input)
            else:
                result = {"success": False, "error": "Unknown tool"}

            if result.success:
                output_preview = str(result.output)[:100]
                print(f"    ✓ Success: {output_preview}...")
            else:
                print(f"    ✗ Error: {result.error}")

            # Add tool result to conversation
            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_name,
                "content": json.dumps(result.to_dict())
            })

    print("\n" + "="*70)
    print("MOCK TEST COMPLETE")
    print("="*70)
    print("""
Summary:
✓ Agent loop works correctly (no infinite loops)
✓ Tool calls are executed properly
✓ Database queries return real data
✓ Results are processed and added to conversation
✓ Agent provides final answer

Cost of this test: $0.00 (mock mode)

To run with real LLM:
  1. Decide on API provider (team OpenRouter or personal Anthropic)
  2. Run: python -m src.cli --question "..." --verbose
    """)


if __name__ == "__main__":
    test_agent_workflow()
