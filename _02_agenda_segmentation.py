from dotenv import load_dotenv
import anthropic
import json
import csv
from pathlib import Path
import os



def main():
    ###################################################################
    load_dotenv()
    client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_KEY'))

    # Folder containing processed agenda .txt files
    input_agenda_folder = Path("processed_agendas")
    output_agenda_segment_folder = Path("agenda_segments")
    ###################################################################

    segment_all_agendas(input_agenda_folder, output_agenda_segment_folder, client)


# ============================ #
# Claude Prompt Generator      #
# ============================ #

def agenda_segmentation_prompt(agenda_text: str) -> str:
    return f"""
You are a professional city council meeting assistant.

Given the full raw text of a meeting agenda, segment it into distinct agenda items. For each item:

1. Include the full agenda item title (e.g., "Bill 2023-114: Amending the zoning regulations").
2. Each **bill, paper, resolution, or ordinance** (e.g., "ORD. 2023-114", "RES. 2023-R016", "PAPER #412") counts as a **separate agenda item**, even if multiple items fall under the same section.
3. If a bill number or ordinance number appears, include it as part of the agenda item title.
4. Under each agenda item, include **all the text** that falls under it until the next agenda item begins.
5. Keep the original wording and formatting. Do not summarize or shorten the text.
6. Do not skip or omit any part of the agenda. This includes routine items such as “Roll Call,” “Public Comment," and other procedural sections.

Return the segmented agenda as a JSON array of strings. Each string is one agenda item with its full text.

**Important:** Return **only** the JSON array of strings with no additional text, explanation, or commentary. The output must be a valid JSON array.

[
  "[Agenda item title]\\n   [Full text under the item]",
  "[Next agenda item]\\n   [Full text under the item]",
  ...
]

Agenda:
\"\"\"{agenda_text}\"\"\"
"""


# ============================ #
# Claude API Wrapper           #
# ============================ #

def claude_segment(agenda_text: str, client) -> str:
    prompt = agenda_segmentation_prompt(agenda_text)
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=8192,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


# ============================ #
# File I/O Helpers             #
# ============================ #

def save_json_segments_to_csv(json_string: str, output_path: Path):
    try:
        segments = json.loads(json_string)
        with output_path.open("w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["agenda_segment"])
            for segment in segments:
                writer.writerow([segment])
        print(f"Saved {len(segments)} segments to {output_path}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from Claude:\n{e}")


# ============================ #
# Main Pipeline                #
# ============================ #

def segment_all_agendas(input_folder: Path, output_folder: Path, client):
    for file_path in input_folder.rglob("*.txt"):
        print(f"Segmenting {file_path}")
        file_stem = file_path.stem
        output_path = output_folder / f"{file_stem}.csv"

        text = file_path.read_text(encoding='utf-8')
        segments_json = claude_segment(text, client)
        save_json_segments_to_csv(segments_json, output_path)


# Run the script
if __name__ == "__main__":
    main()
