"""Test adding a URL directly to see if there's an issue."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paperqa import Docs, Settings
from paperqa.settings import AnswerSettings
from dotenv import load_dotenv

load_dotenv()

# Create settings (use environment variables)
settings = Settings(
    llm=os.getenv("PAPERQA_LLM", "openrouter/openai/gpt-4.1-mini"),
    embedding=os.getenv("PAPERQA_EMBEDDING", "openai/text-embedding-3-small"),
    answer=AnswerSettings(
        answer_max_sources=2,
        evidence_k=5
    )
)

# Create docs
docs = Docs()

# Try to add a URL from Semantic Scholar result
pdf_url = "https://jamanetwork.com/journals/jamanetworkopen/articlepdf/2760661/schmidt_2020_oi_190782.pdf"
citation = "Schmidt et al. Assessment of Clinical Activity of PD-1 Checkpoint Inhibitor Combination Therapies. 2020"

print(f"Attempting to add PDF from URL: {pdf_url}")
print(f"Citation: {citation}\n")

try:
    docs.add_url(pdf_url, citation=citation, settings=settings)
    print("✓ Successfully added URL!")
    print(f"Number of docs: {len(docs.docs)}")

    # Try to query
    if len(docs.docs) > 0:
        print("\nQuerying...")
        result = docs.query("What is PD-1?", settings=settings)
        print(f"Answer: {result.answer[:200]}...")

except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
