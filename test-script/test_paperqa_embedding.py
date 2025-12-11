import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from paperqa import Docs, Settings
from paperqa.settings import AnswerSettings

def test_embedding():
    print("Testing PaperQA embedding with OpenRouter...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"OPENROUTER_API_KEY present: {bool(api_key)}")
    
    # Explicitly set for LiteLLM
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
        
        # TRICK: Configure OpenAI provider to point to OpenRouter for embeddings
        # This bypasses "Unmapped LLM provider" error for openrouter embeddings
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
        
    llm_model = os.getenv("PAPERQA_LLM", "openrouter/openai/gpt-5-mini")
    # Use openai/ prefix but point to OpenRouter via env vars
    embedding_model = "openai/text-embedding-3-small"
    
    print(f"LLM: {llm_model}")
    print(f"Embedding: {embedding_model}")
    
    settings = Settings(
        llm=llm_model,
        embedding=embedding_model,
        answer=AnswerSettings(evidence_k=1)
    )
    
    docs = Docs()
    
    # Create a dummy file to embed
    dummy_path = "test_doc.txt"
    with open(dummy_path, "w") as f:
        f.write("T-cell exhaustion is characterized by high expression of PD-1 and TOX.")
        
    try:
        print("Adding document (this triggers embedding)...")
        docs.add(dummy_path, settings=settings)
        print("SUCCESS: Document added and embedded.")
    except Exception as e:
        print("\nFAILURE")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if os.path.exists(dummy_path):
            os.remove(dummy_path)

if __name__ == "__main__":
    test_embedding()
