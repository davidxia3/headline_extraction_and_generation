import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
import anthropic

# ============================ #
# Setup                        #
# ============================ #

# Load environment variables (for CLAUDE_KEY)
load_dotenv()
CLAUDE_API_KEY = os.getenv('CLAUDE_KEY')
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# ============================ #
# Prompt Builder               #
# ============================ #

def build_summary_prompt(transcript_segment: str) -> str:
    """
    Returns a prompt string for summarizing a city council meeting transcript segment.
    """
    return f"""
You are a professional city council meeting analyst.

Given a segment from a city council meeting transcript, write a **factual, one-sentence summary** that:
  - Extracts the **agenda item identifier** — such as a bill number, ordinance, resolution (e.g., ORD. 2023-114, RES. 2025-1802), or procedural label like "Roll Call"
  - Describes the main purpose or action (e.g., approval, authorization, discussion)
  - Names relevant people, organizations, or locations

If the content is too vague or procedural to summarize meaningfully, return **"NO_SUMMARY"** exactly (no explanations or extra words).

Segment:
\"\"\"{transcript_segment}\"\"\"

Summary:
""".strip()

# ============================ #
# Claude API Query Function   #
# ============================ #

def summarize_segment_with_claude(segment: str) -> str:
    """
    Sends the segment to Claude and returns its summary.
    """
    prompt = build_summary_prompt(segment)
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=64,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text.strip()

# ============================ #
# Main Loop: Process CSVs     #
# ============================ #

def summarize_transcript_folder(folder_path: str):
    folder = Path(folder_path)
    for csv_file in folder.rglob("*.csv"):

        df = pd.read_csv(csv_file)

        if "matching_summary" in df.columns:
            print(f"Skipping (already processed): {csv_file.name}")
            continue

        print(f"Processing: {csv_file}")
        
        # Apply Claude summarization
        df["matching_summary"] = df["segment"].apply(summarize_segment_with_claude)

        # Save the updated DataFrame
        df.to_csv(csv_file, index=False)

# ============================ #
# Entry Point                 #
# ============================ #

if __name__ == "__main__":
    summarize_transcript_folder("transcript_segments")
