"""Test downloading PDF with proper headers."""

import requests
import tempfile

pdf_url = "https://jamanetwork.com/journals/jamanetworkopen/articlepdf/2760661/schmidt_2020_oi_190782.pdf"

print(f"Downloading PDF from: {pdf_url}")

try:
    # Download with proper headers
    pdf_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    pdf_response = requests.get(pdf_url, headers=pdf_headers, timeout=60)
    print(f"Status code: {pdf_response.status_code}")
    pdf_response.raise_for_status()

    print(f"Content-Type: {pdf_response.headers.get('Content-Type')}")
    print(f"Content-Length: {len(pdf_response.content)} bytes")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as tmp_file:
        tmp_file.write(pdf_response.content)
        tmp_path = tmp_file.name
        print(f"Saved to: {tmp_path}")

    print("✓ Successfully downloaded PDF!")

except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
