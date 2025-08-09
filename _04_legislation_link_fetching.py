import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import csv
import re


# ===== CONFIG =====
input_folder = Path("__input_urls")  # Folder containing .txt files with URLs
output_folder = Path("legislations")  # Folder to save CSV files
table_id = "ctl00_ContentPlaceHolder1_gridMain_ctl00"

output_folder.mkdir(exist_ok=True, parents=True)

# Iterate through each .txt file
for txt_file in input_folder.glob("*.txt"):
    with open(txt_file, "r", encoding="utf-8") as f:
        page_url = f.read().strip()

    if not page_url:
        print(f"Skipping empty file: {txt_file}")
        continue

    print(f"\nProcessing: {page_url}")

    try:
        response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch page {page_url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", id=table_id)
    if not table:
        print(f"No table with id '{table_id}' found on page.")
        continue

    output_csv_path = output_folder / f"{txt_file.stem}.csv"

    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["item", "link"])  # header row

        # Iterate table rows
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue

            first_col = cells[0]
            text = re.sub(r"[a-zA-Z\s]", "", first_col.get_text(strip=True))
            links = first_col.find_all("a", href=True)

            for a in links:
                href = urljoin(page_url, a["href"])
                if text and href:
                    writer.writerow([text, href])

    print(f"Saved CSV: {output_csv_path}")

print("All done.")
