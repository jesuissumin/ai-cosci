import os
import sys
from dotenv import load_dotenv

# Load env vars first
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.tools.implementations import search_literature

def test_search():
    print("Testing search_literature with PaperQA...")
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"OPENROUTER_API_KEY present: {bool(api_key)}")
    
    # Check config
    try:
        from src.config import get_global_config
        config = get_global_config()
        print(f"PaperQA LLM: {config.paperqa_llm}")
    except Exception as e:
        print(f"Could not load config: {e}")

    question = "What are the key markers of T-cell exhaustion?"
    print(f"Question: {question}")
    
    try:
        # Use 'online' mode to force using the LLM/Search instead of just local files
        # This tests the OpenRouter integration
        result = search_literature(
            question=question,
            mode="online", 
            max_sources=2
        )
        
        if result.success:
            print("\nSUCCESS!")
            # result.output is likely a dictionary or object with 'answer', 'contexts', etc.
            # based on the docstring: "ToolResult with: - answer: ..."
            print(f"Result type: {type(result.output)}")
            print(f"Output: {str(result.output)[:500]}...")
        else:
            print("\nFAILURE")
            print(f"Error: {result.error}")
            
    except Exception as e:
        print(f"\nEXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search()
