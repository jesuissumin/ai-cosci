"""Verbose test of the search implementation to see what's failing."""

import os
import sys
import requests
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paperqa import Docs, Settings
from paperqa.settings import AnswerSettings
from dotenv import load_dotenv

load_dotenv()

# Create settings
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

question = "PD-1 checkpoint inhibitor"
max_sources = 2

print("Starting Semantic Scholar search...")
print(f"Question: {question}\n")

try:
    s2_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": question,
        "limit": max_sources,
        "fields": "title,authors,year,abstract,openAccessPdf,externalIds,citationCount"
    }

    print(f"Calling S2 API: {s2_url}")
    response = requests.get(s2_url, params=params, timeout=30.0)
    print(f"Response status: {response.status_code}")
    response.raise_for_status()

    search_data = response.json()
    papers_data = search_data.get("data", [])
    print(f"Found {len(papers_data)} papers\n")

    s2_papers_added = 0

    for i, paper in enumerate(papers_data[:max_sources], 1):
        print(f"\n--- Paper {i} ---")
        title = paper.get("title", "Unknown")
        print(f"Title: {title}")

        # Check for PDF
        pdf_url = None
        pdf_info = paper.get("openAccessPdf")

        if pdf_info and pdf_info.get("url"):
            pdf_url = pdf_info["url"]
            print(f"OpenAccess PDF: {pdf_url}")
        else:
            print("No OpenAccess PDF")
            # Try arXiv
            external_ids = paper.get("externalIds", {})
            arxiv_id = external_ids.get("ArXiv")
            if arxiv_id:
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                print(f"ArXiv PDF: {pdf_url}")
            else:
                print("No ArXiv ID either, skipping")
                continue

        # Try to download
        try:
            print(f"Downloading PDF...")
            pdf_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            pdf_response = requests.get(pdf_url, headers=pdf_headers, timeout=60)
            print(f"Download status: {pdf_response.status_code}")
            pdf_response.raise_for_status()

            content_type = pdf_response.headers.get("Content-Type", "")
            print(f"Content-Type: {content_type}")
            print(f"Content size: {len(pdf_response.content)} bytes")

            # Verify it's actually a PDF
            if "pdf" not in content_type.lower() and not pdf_response.content.startswith(b"%PDF"):
                print("Not a valid PDF, skipping")
                continue

            # Save and add to docs
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as tmp_file:
                tmp_file.write(pdf_response.content)
                tmp_path = tmp_file.name
                print(f"Saved to temp file: {tmp_path}")

            try:
                year = paper.get("year", "")
                authors = paper.get("authors", [])
                author_names = ", ".join([a.get("name", "") for a in authors[:3]])
                if len(authors) > 3:
                    author_names += " et al."

                citation = f"{author_names}. {title}. {year}" if year else f"{author_names}. {title}"

                print(f"Adding to docs...")
                docs.add(tmp_path, citation=citation, settings=settings)
                s2_papers_added += 1
                print(f"✓ Successfully added!")

            finally:
                try:
                    os.unlink(tmp_path)
                    print(f"Cleaned up temp file")
                except Exception as e:
                    print(f"Warning: Failed to clean up temp file: {e}")

        except Exception as e:
            print(f"✗ Error: {type(e).__name__}: {e}")
            continue

    print(f"\n\nTotal papers added: {s2_papers_added}")
    print(f"Total docs in collection: {len(docs.docs)}")

except Exception as e:
    print(f"Fatal error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
