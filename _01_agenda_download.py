import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

# ===== CONFIG =====
input_folder = Path("__input_urls")      # Folder containing .txt files with URLs
output_folder = Path("agendas_raw")      # Where PDFs will be saved
link_id = "ctl00_ContentPlaceHolder1_hypMinutes"

# Create output folder if it doesn't exist
output_folder.mkdir(parents=True, exist_ok=True)

# Iterate through all .txt files in the input folder
for txt_file in input_folder.glob("*.txt"):
    with open(txt_file, "r", encoding="utf-8") as f:
        page_url = f.read().strip()

    if not page_url:
        print(f"Skipping empty file: {txt_file}")
        continue

    print(f"Processing: {page_url}")

    # Step 1: Get HTML content
    try:
        response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch page {page_url}: {e}")
        continue

    # Step 2: Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 3: Find the link with the given ID
    link_tag = soup.find("a", id=link_id)
    if not link_tag or not link_tag.get("href"):
        print(f"No PDF link found on page: {page_url}")
        continue

    # Step 4: Build full URL for the PDF
    pdf_url = urljoin(page_url, link_tag["href"])
    print(f"Found PDF link: {pdf_url}")

    # Step 5: Download PDF
    try:
        pdf_response = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
        pdf_response.raise_for_status()
    except Exception as e:
        print(f"Failed to download PDF from {pdf_url}: {e}")
        continue

    # Save PDF using the txt filename but with .pdf extension
    output_filename = output_folder / (txt_file.stem + ".pdf")
    with open(output_filename, "wb") as f:
        f.write(pdf_response.content)

    print(f"PDF saved as '{output_filename}'\n")

print("Done.")
