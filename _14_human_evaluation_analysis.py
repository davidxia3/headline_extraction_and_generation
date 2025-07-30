import pandas as pd
import json
import csv
from pathlib import Path
from trueskill import Rating, rate_1vs1

# ========== CONFIGURATION ==========
WEEKS = [
    ("20250331", "20250404"),
    ("20250407", "20250411"),
    ("20250414", "20250418"),
    ("20250421", "20250425")
]

INPUT_DIR = Path("human_evaluation_prep")
OUTPUT_DIR = Path("human_evaluation_results")
OUTPUT_DIR.mkdir(exist_ok=True)

# ========== UTILITY FUNCTIONS ==========

def generate_labels(base: str, total: int) -> list[str]:
    return [f"{base}{i}" for i in range(total)]

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

def save_ranking_results(week_str: str, filename: str, results: list[dict]):
    filepath = OUTPUT_DIR / f"{week_str}_{filename}.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

# ========== MAIN PROCESSING FUNCTION ==========

def process_week(week: tuple[str, str]):
    week_str = f"{week[0]}_{week[1]}"
    print(f"Processing week: {week_str}")

    df = pd.read_csv(INPUT_DIR / f"{week_str}_filtered_headlines.csv")
    manual_indices = [idx for idx, row in df.iterrows() if row["manual_headline"] != "NO_HEADLINE"]
    total_headlines = len(df)

    # Labels
    claude_labels = generate_labels("C", total_headlines)
    gemini_labels = generate_labels("G", total_headlines)
    openai_labels = generate_labels("O", total_headlines)

    manual_claude_labels = claude_labels + [f"M{i}" for i in manual_indices]
    manual_gemini_labels = gemini_labels + [f"M{i}" for i in manual_indices]
    manual_openai_labels = openai_labels + [f"M{i}" for i in manual_indices]

    with open(INPUT_DIR / f"{week_str}_labels.json", "r") as f:
        label_data = json.load(f)

    labels_to_headlines = label_data["labels_to_headlines"]
    headlines_to_labels = label_data["headlines_to_labels"]

    responses_df = pd.read_csv(Path("human_evaluation_responses") / f"{week_str}_responses.csv")

    comparisons = []
    for _, row in responses_df.iterrows():
        hl1 = row["Headline 1"]
        hl2 = row["Headline 2"]
        winner = row["Annotator1_Response"]

        id1 = headlines_to_labels[hl1]
        id2 = headlines_to_labels[hl2]

        comparisons.append((id1, id2) if winner == "Headline 1" else (id2, id1))

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
        save_ranking_results(week_str, name, results)

    print(f"Finished: {week_str}")

# ========== RUN FOR ALL WEEKS ==========

for week in WEEKS:
    process_week(week)

print("All weeks processed.")
