import pandas as pd
import numpy as np
import json
import csv
from pathlib import Path
from trueskill import Rating, rate_1vs1

# ========== CONFIGURATION ==========

WEEK = ("20250331", "20250404")
WEEK_STR = f"{WEEK[0]}_{WEEK[1]}"
INPUT_DIR = Path("human_evaluation_prep")
OUTPUT_DIR = Path("human_evaluation_results")
OUTPUT_DIR.mkdir(exist_ok=True)

# Maps
WEEK_TO_TOTAL_HEADLINES = {
    "20250331_20250404": 31,
}
WEEK_TO_MANUAL_INDICES = {
    "20250331_20250404": [10, 12, 22, 26],
}

TOTAL_HEADLINES = WEEK_TO_TOTAL_HEADLINES[WEEK_STR]
MANUAL_INDICES = WEEK_TO_MANUAL_INDICES[WEEK_STR]

# ========== GENERATE LABEL GROUPS ==========

def generate_labels(base: str, total: int) -> list[str]:
    return [f"{base}{i}" for i in range(total)]

# Basic LLM-only labels
claude_labels = generate_labels("C", TOTAL_HEADLINES)
gemini_labels = generate_labels("G", TOTAL_HEADLINES)
openai_labels = generate_labels("O", TOTAL_HEADLINES)

# Mixed labels (LLM + Manual)
manual_claude_labels = claude_labels + [f"M{i}" for i in MANUAL_INDICES]
manual_gemini_labels = gemini_labels + [f"M{i}" for i in MANUAL_INDICES]
manual_openai_labels = openai_labels + [f"M{i}" for i in MANUAL_INDICES]

# ========== LOAD LABELS & RESPONSES ==========

with open(INPUT_DIR / f"{WEEK_STR}_labels.json", "r") as f:
    label_data = json.load(f)

labels_to_headlines = label_data["labels_to_headlines"]
headlines_to_labels = label_data["headlines_to_labels"]

responses_df = pd.read_csv(Path("human_evaluation_responses") / f"{WEEK_STR}_responses.csv")

# ========== PARSE COMPARISONS ==========

comparisons = []

for _, row in responses_df.iterrows():
    hl1 = row["Headline 1"]
    hl2 = row["Headline 2"]
    winner = row["Annotator1_Response"]

    id1 = headlines_to_labels[hl1]
    id2 = headlines_to_labels[hl2]

    comparisons.append((id1, id2) if winner == "Headline 1" else (id2, id1))

# ========== RANKING FUNCTION ==========

def trueskill_ranking(item_labels, comparisons, label_to_headline):
    ratings = {item: Rating() for item in item_labels}

    for winner, loser in comparisons:
        if winner in ratings and loser in ratings:
            ratings[winner], ratings[loser] = rate_1vs1(ratings[winner], ratings[loser])

    ranked_items = sorted(ratings.items(), key=lambda x: x[1].mu, reverse=True)

    z = 1.96  # 95% confidence
    results = []

    for rank, (label, rating) in enumerate(ranked_items, start=1):
        results.append({
            "rank": rank,
            "label": label,
            "headline": label_to_headline.get(label, "UNKNOWN"),
            "score_mu": round(rating.mu, 2),
            "score_sigma": round(rating.sigma, 2),
            "score_95ci": round(z * rating.sigma, 2),
        })

    return results

# ========== WRITE RESULTS ==========

def save_ranking_results(filename: str, results: list[dict]):
    filepath = OUTPUT_DIR / f"{WEEK_STR}_{filename}.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

# ========== RUN ALL RANKINGS ==========

ranking_tasks = [
    ("manual_claude", manual_claude_labels),
    ("manual_gemini", manual_gemini_labels),
    ("manual_openai", manual_openai_labels),
    ("claude_only", claude_labels),
    ("gemini_only", gemini_labels),
    ("openai_only", openai_labels),
]

for name, label_group in ranking_tasks:
    results = trueskill_ranking(label_group, comparisons, labels_to_headlines)
    save_ranking_results(name, results)

print("All rankings complete. Results saved to:", OUTPUT_DIR)
