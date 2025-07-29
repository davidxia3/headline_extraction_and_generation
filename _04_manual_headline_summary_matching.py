import pandas as pd
from pathlib import Path

# Define the directory containing agenda segment CSV files
SEGMENT_DIR = Path("agenda_segments")

# Initialize missing columns in all CSV files if not already present
for csv_file in SEGMENT_DIR.rglob("*.csv"):
    df = pd.read_csv(csv_file)

    # Add columns if they don't exist
    if "true_headline" not in df.columns:
        df["true_headline"] = "NO_HEADLINE"
    if "true_summary" not in df.columns:
        df["true_summary"] = "NO_SUMMARY"

    df.to_csv(csv_file, index=False)

# Manual matching data
file_names = [
    "PIT_20250401_REG.csv",
    "PIT_20250401_REG.csv",
    "PIT_20250402_STA.csv",
    "PIT_20250402_STA.csv",
]

row_indices = [
    23, 
    27, 
    12, 
    17
]

manual_headlines = [
    "Open-Ended Professional Services Contracts Add 27 Unspecified New Vendors",
    "Portable Restroom Back Payment Sparks Inquiries into the Prevalence of Closed Public Restrooms in City Parks",
    "Council to Approve Funding for Recruitment Video Aimed at Addressing Police Shortages",
    "14 Acre Bakery Square Expansion Moves Forward with Two Key Amendments Ready for Public Hearing",
]

manual_summaries = [
    "- Open-ended professional services contracts allow vendors to provide on-call professional services for work orders estimated to cost $100,000 or less.\n- The program’s goal is to enable City departments to contract services on a rolling basis without seeking Council approval for each request.\n- Services include architecture, interior design, and historic consulting, among others.\n- New vendors will be added to the program on a rolling basis, but any new additions will require Council approval.\n- Councilperson Charland expressed concern that the “fairly self-governing” system of distributing work could lead departments to overlook minority contractors.",
    "- A bill covering $35k in expenses for portable bathrooms led to a discussion about the number of broken permanent public restrooms in the city’s parks.\n- Director Hornstein of the Department of Public Works did not have an exact count of closed public restrooms to share with Council.\n- There are 20 open public restrooms in city parks.\n- To restore inoperable restrooms, Director Hornstein stated that public approval and tax funding would be needed for:\n  - An assessment of which restrooms are closed and what repairs and maintenance are required.\n  - The actual repairs and maintenance, which will likely be significant given how long some have been closed.\n  - A program to maintain the restrooms once they are reopened.\n- The city spent $219,000 on portable restrooms in parks that lack functioning permanent public restrooms.\n- Council members agreed that there should be a plan to begin addressing this long-standing issue.",
    "- The Police Department is requesting approval to spend $32K from a State grant on a new recruitment video to be developed by Kicker, Inc.\n- Videos are expected to include “exciting and proud images of Pittsburgh Police Officers at work in various positions, including Patrol, K-9 Unit, Investigators, SWAT, Motorcycle Unit, Mounted Patrol, River Patrol, Special Victims Unit, Narcotics/Vice, and Computer Crimes Unit” as well as iconic Pittsburgh imagery.\n- Council noted the need for new recruitment efforts and was pleased to hear that the number of people taking the civil service exam has begun to increase. They hope the videos are as successful as they have been in other cities.\n- The videos will primarily be used across social media platforms and YouTube.",
    "- The expansion will encompass 14 acres west along Penn Avenue in the Larimer and East Liberty neighborhoods.\n- The standout initiative is the Build 100 program, which calls for Walnut Capital to contribute $6 million and commit to raising another $19 million toward creating 100 affordable homes for purchase.\n- This work is the product of a Community Benefits Agreement between the Larimer Consensus Group, the Village Collaborative, and Walnut Capital.\n- Council sent the proposed amendments to the Planning Commission on July 6 and July 12, 2023, and received the Commission’s report and recommendation for both on January 24, 2025.\n- The 4/2 vote allows for two bills—one delineating new block and lot numbers and the other detailing building code and other requirements within the subdistrict—to proceed to a public hearing.",
]

# Update specified rows with manual headline and summary
for file_name, idx, headline, summary in zip(file_names, row_indices, manual_headlines, manual_summaries):
    file_path = SEGMENT_DIR / file_name

    if not file_path.exists():
        print(f"File not found: {file_path}")
        continue

    df = pd.read_csv(file_path)

    if idx < 0 or idx >= len(df):
        print(f"Invalid row index {idx} in {file_name}")
        continue

    df.loc[idx, "true_headline"] = headline
    df.loc[idx, "true_summary"] = summary

    df.to_csv(file_path, index=False)
    print(f"Updated row {idx} in {file_name}")
