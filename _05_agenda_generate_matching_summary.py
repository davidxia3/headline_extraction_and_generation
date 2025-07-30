from dotenv import load_dotenv
import anthropic
import pandas as pd
from pathlib import Path
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_KEY'))


def main():
    ########################################################
    folder = Path("agenda_segments")
    ########################################################
    for file_path in folder.rglob("*.csv"):
        df = pd.read_csv(file_path)
        if "matching_summary" in df.columns:
            continue

        print(f"Generating matching summaries for {file_path}")
        df["matching_summary"] = df["agenda_segment"].apply(ask_summary)
        df.to_csv(file_path, index=False)



# ============================ #
# Claude Prompt Generator      #
# ============================ #

def make_summary_prompt(agenda_segment):
    return f"""
You are a professional city council meeting analyst.

Given a segment from a city council meeting agenda, write a **factual, one-sentence summary** that:
  - Extracts the **agenda item identifier** — this could be a bill number, ordinance, resolution number (e.g., ORD. 2023-114, RES. 2025-1802, 2025-1799), or a procedural label like "Roll Call" or "Public Comment"
  - Includes the main purpose or action (e.g., approval, authorization, recommendation)
  - Includes relevant named entities like people, organizations, and locations

If the content is too vague or procedural to summarize meaningfully, **return `"NO_SUMMARY"` exactly** — no explanation or extra words.

Segment:
\"\"\"{agenda_segment}\"\"\"

Summary:
"""


# ============================ #
# Claude API Wrapper           #
# ============================ #

def ask_summary(agenda_segment):
    prompt = make_summary_prompt(agenda_segment)
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=8192,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text.strip()


if __name__ == "__main__":
    main()