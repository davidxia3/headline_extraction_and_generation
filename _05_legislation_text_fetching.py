import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pathlib import Path
import time

# ===== CONFIG =====
input_folder = Path("legislations")  # Folder containing CSV files
output_folder = input_folder          # Saving back to original folder (overwrite)
tab_xpath = '//li[contains(@class, "rtsLI") and contains(@class, "rtsLast")]//span[contains(@class, "rtsTxt") and text()="Text"]/ancestor::li'
div_id = "ctl00_ContentPlaceHolder1_pageText"

# ===== SETUP HEADLESS CHROME =====
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    csv_files = list(input_folder.glob("*.csv"))
    for csv_file in csv_files:
        print(f"\nProcessing file: {csv_file}")
        df = pd.read_csv(csv_file)

        if "link" not in df.columns:
            print(f"  No 'link' column found in {csv_file}, skipping.")
            continue

        texts = []

        for idx, url in enumerate(df["link"]):
            print(f"  Row {idx + 1}: Opening {url}")
            try:
                driver.get(url)
                wait = WebDriverWait(driver, 5)

                # Click the "Text" tab
                tab_element = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
                tab_element.click()

                # Wait for the content div
                content_div = wait.until(EC.visibility_of_element_located((By.ID, div_id)))
                text_content = content_div.text.strip()

                # Check for "Click here for full text" link inside the div
                try:
                    full_text_link = content_div.find_element(By.LINK_TEXT, "Click here for full text")
                    if full_text_link:
                        full_text_url = full_text_link.get_attribute("href")
                        print(f"    Found full text link, navigating to {full_text_url}")
                        driver.get(full_text_url)

                        # Wait again for the div on the new page
                        content_div = wait.until(EC.visibility_of_element_located((By.ID, div_id)))
                        text_content = content_div.text.strip()
                except (TimeoutException, NoSuchElementException):
                    # No such link found, ignore
                    pass

                print(f"    Retrieved text length: {len(text_content)}")
                texts.append(text_content)

            except Exception as e:
                print(f"    Error processing URL {url}: {e}")
                texts.append("NO_LEGISLATION")

            time.sleep(1)  # polite delay between requests

        df["text"] = texts
        df.to_csv(csv_file, index=False)
        print(f"  Saved updated CSV: {csv_file}")

finally:
    driver.quit()
