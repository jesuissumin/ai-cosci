"""Debug test for internet search."""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Test Semantic Scholar directly
print("Testing Semantic Scholar API...")
s2_url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": "PD-1 checkpoint inhibitor",
    "limit": 2,
    "fields": "title,authors,year,abstract,openAccessPdf,externalIds,citationCount"
}

headers = {}
if s2_api_key := os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
    headers["x-api-key"] = s2_api_key

try:
    response = requests.get(s2_url, params=params, headers=headers, timeout=30.0)
    print(f"Status code: {response.status_code}")
    response.raise_for_status()
    search_data = response.json()

    papers_data = search_data.get("data", [])
    print(f"\nFound {len(papers_data)} papers from Semantic Scholar")

    for i, paper in enumerate(papers_data, 1):
        print(f"\nPaper {i}:")
        print(f"  Title: {paper.get('title', 'N/A')}")
        print(f"  Year: {paper.get('year', 'N/A')}")

        pdf_info = paper.get("openAccessPdf")
        if pdf_info:
            print(f"  PDF available: {pdf_info.get('url', 'No URL')}")
        else:
            print(f"  PDF available: No")

except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)

# Test PubMed
print("\nTesting PubMed API...")
import urllib.parse

search_term = urllib.parse.quote("PD-1 checkpoint inhibitor")
search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={search_term}&retmode=json&retmax=2"

try:
    search_response = requests.get(search_url, timeout=30)
    print(f"Status code: {search_response.status_code}")
    search_response.raise_for_status()
    search_data = search_response.json()

    pmids = search_data.get("esearchresult", {}).get("idlist", [])
    print(f"\nFound {len(pmids)} papers from PubMed")

    for i, pmid in enumerate(pmids, 1):
        print(f"\nPaper {i} (PMID: {pmid}):")

        # Check PMC availability
        pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=json"
        pmc_response = requests.get(pmc_url, timeout=30)
        pmc_data = pmc_response.json()

        records = pmc_data.get("records", [])
        if records and records[0].get("pmcid"):
            pmcid = records[0]["pmcid"]
            print(f"  PMC ID: {pmcid}")
            print(f"  PDF URL: https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/")
        else:
            print(f"  PMC: Not available (not open access)")

except Exception as e:
    print(f"Error: {e}")
