"""Test PubMed/PMC search specifically."""

import os
import requests
import urllib.parse
import tempfile

question = "T-cell exhaustion 2020"  # Add year to get older papers
max_sources = 10  # Try more to find open access ones

print(f"Searching PubMed for: {question}\n")

search_term = urllib.parse.quote(question)
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={search_term}&retmode=json&retmax={max_sources}"

search_response = requests.get(search_url, timeout=30)
search_data = search_response.json()

pmids = search_data.get("esearchresult", {}).get("idlist", [])
print(f"Found {len(pmids)} PubMed IDs\n")

pmc_papers_found = 0

for i, pmid in enumerate(pmids, 1):
    print(f"--- PMID {pmid} (Paper {i}/{len(pmids)}) ---")

    try:
        # Check if available in PMC
        pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=json"
        pmc_response = requests.get(pmc_url, timeout=30)
        pmc_data = pmc_response.json()

        records = pmc_data.get("records", [])
        if not records or not records[0].get("pmcid"):
            print("Not available in PMC (not open access)")
            continue

        pmcid = records[0]["pmcid"]
        print(f"PMC ID: {pmcid}")

        # Get paper details
        details_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
        details_response = requests.get(details_url, timeout=30)
        details_data = details_response.json()

        paper_info = details_data.get("result", {}).get(pmid, {})
        title = paper_info.get("title", "Unknown")
        print(f"Title: {title[:80]}...")

        # Try to download PDF
        pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
        print(f"PDF URL: {pdf_url}")

        pdf_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        pdf_response = requests.get(pdf_url, headers=pdf_headers, timeout=60)
        print(f"Download status: {pdf_response.status_code}")

        if pdf_response.status_code == 200:
            content_type = pdf_response.headers.get("Content-Type", "")
            size = len(pdf_response.content)
            print(f"Content-Type: {content_type}")
            print(f"Size: {size} bytes")

            if "pdf" in content_type.lower() or pdf_response.content.startswith(b"%PDF"):
                print("✓ Valid PDF downloaded!")
                pmc_papers_found += 1
            else:
                print("✗ Not a valid PDF")
        else:
            print(f"✗ Failed to download")

    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")

    print()

print(f"\n{'='*60}")
print(f"Total PMC papers found: {pmc_papers_found}/{len(pmids)}")
