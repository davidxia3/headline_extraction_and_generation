import pandas as pd
from pathlib import Path

# Map for human-readable or shorthand label inputs
LABEL_MAP = {
    "beginning of new topic": "b",
    "beginning of new public comment topic": "p",
    "inside a topic": "i",
    "b": "b",
    "p": "p",
    "i": "i",
    "f": "f"
}

# === Configuration ===
FILE_STEM = "PIT_20250401_REG"
INPUT_DIR = Path("sentences_unlabeled")
OUTPUT_DIR = Path("sentences_manual")

INPUT_FILE = INPUT_DIR / f"{FILE_STEM}.csv"
OUTPUT_FILE = OUTPUT_DIR / f"{FILE_STEM}.csv"
# ======================

# Load input CSV
df = pd.read_csv(INPUT_FILE)

# Ensure classification column exists
if "classification" not in df.columns:
    df["classification"] = ""

# === Instructions ===
print("Label each sentence as:")
print("  b - beginning of new topic")
print("  p - beginning of new public comment topic")
print("  i - inside a topic")
print("Type 'back' to go to the previous sentence.")
print("Type 'quit' to stop early and save your progress.\n")

# === Labeling Loop ===
idx = 0
while idx < len(df):
    sentence = df.loc[idx, "sentence"]
    current_label = df.loc[idx, "classification"]

    print(f"\n{idx + 1}/{len(df)}: {sentence}")
    if current_label:
        print(f"Current label: {current_label}")

    user_input = input("Label (b/p/i, or 'back', 'quit'): ").strip().lower()

    if user_input in {"b", "p", "i"}:
        df.at[idx, "classification"] = LABEL_MAP[user_input]
        idx += 1
    elif user_input == "back":
        if idx > 0:
            idx -= 1
        else:
            print("Already at the beginning.")
    elif user_input == "quit":
        break
    else:
        print("Invalid input. Please enter 'b', 'p', 'i', 'back', or 'quit'.")

# === Save Results ===
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nProgress saved to: {OUTPUT_FILE}")
