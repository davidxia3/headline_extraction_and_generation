import pandas as pd
import csv
from pathlib import Path

def convert_sentences_to_segments(input_csv_path, output_csv_path):
    """
    Converts a CSV of classified sentences into text segments, 
    excluding segments that begin with public comments ("p").
    """
    df = pd.read_csv(input_csv_path)

    # Remove irrelevant rows
    df = df[df["classification"] != "f"].reset_index(drop=True)

    # Skip any initial content before the first 'b' or 'p'
    start_index = df[df["classification"].isin(["b", "p"])].index.min()
    df = df.iloc[start_index:].reset_index(drop=True)

    segments = []
    current_segment = ""
    is_public_comment = False
    in_segment = False

    for _, row in df.iterrows():
        label = row["classification"]
        sentence = row["sentence"]

        if label == "i":
            current_segment += sentence + " "
        else:
            # If we're finishing a segment, and it's not a public comment, store it
            if in_segment and not is_public_comment:
                segments.append(current_segment.strip())

            current_segment = sentence + " "
            in_segment = True
            is_public_comment = (label == "p")

    # Handle final segment
    if in_segment and not is_public_comment:
        segments.append(current_segment.strip())

    # Save segments to CSV
    with open(output_csv_path, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["segment"])
        for segment in segments:
            writer.writerow([segment])


if __name__ == "__main__":
    input_folder = Path("sentences_manual") # or sentences_claude, sentences_gemini, sentences_openai
    output_folder = Path("transcript_segments")
    output_folder.mkdir(parents=True, exist_ok=True)

    for input_file in input_folder.rglob("*.csv"):
        output_file = output_folder / f"{input_file.stem}.csv"
        print(f"Segmenting: {input_file}")
        convert_sentences_to_segments(input_file, output_file)
