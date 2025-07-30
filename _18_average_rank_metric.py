import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------
# Constants and Configuration
# ----------------------------
weeks = [
    ("20250331", "20250404"),
    ("20250407", "20250411"),
    ("20250414", "20250418"),
    ("20250421", "20250425")
]

llms = ["claude", "gemini", "openai"]
llm_abbrev = {
    "claude": "C",
    "gemini": "G",
    "openai": "O"
}

# ----------------------------
# Initialization
# ----------------------------
sum_manual_rank = sum_claude_rank = sum_gemini_rank = sum_openai_rank = 0
manual_count = claude_count = gemini_count = openai_count = 0

# ----------------------------
# Main Loop over Weeks
# ----------------------------
for week in weeks:
    week_str = f"{week[0]}_{week[1]}"
    df = pd.read_csv(f"human_evaluation_prep/{week_str}_filtered_headlines.csv")
    manual_indices = set(df[df["manual_headline"] != "NO_HEADLINE"].index)

    # Load human evaluation results
    true_df_dict = {
        "true_claude": pd.read_csv(f"human_evaluation_results/{week_str}_claude_only.csv"),
        "true_gemini": pd.read_csv(f"human_evaluation_results/{week_str}_gemini_only.csv"),
        "true_openai": pd.read_csv(f"human_evaluation_results/{week_str}_openai_only.csv")
    }

    # ------------------------
    # Manual (Expert) Ranking
    # ------------------------
    for gen_llm in llms:
        true = true_df_dict[f"true_{gen_llm}"]
        manual_labels = [f"{llm_abbrev[gen_llm]}{i}" for i in manual_indices]

        for _, row in true.iterrows():
            if row["label"] in manual_labels:
                sum_manual_rank += row["rank"]
                manual_count += 1

    # ------------------------
    # LLM Rankings
    # ------------------------
    for gen_llm in llms:
        for ranking_llm in llms:
            true = true_df_dict[f"true_{gen_llm}"]
            ranking_path = Path(f"llm_rankings/{week_str}_{gen_llm}_headlines_ranked_by_{ranking_llm}.csv")
            ranking = pd.read_csv(ranking_path)

            top_labels = ranking.loc[:len(manual_indices)-1, "label"]

            for _, row in true.iterrows():
                if row["label"] in top_labels.values:
                    if ranking_llm == "claude":
                        sum_claude_rank += row["rank"]
                        claude_count += 1
                    elif ranking_llm == "gemini":
                        sum_gemini_rank += row["rank"]
                        gemini_count += 1
                    elif ranking_llm == "openai":
                        sum_openai_rank += row["rank"]
                        openai_count += 1

# ----------------------------
# Compute Averages
# ----------------------------
avg_manual_rank = sum_manual_rank / manual_count
avg_claude_rank = sum_claude_rank / claude_count
avg_gemini_rank = sum_gemini_rank / gemini_count
avg_openai_rank = sum_openai_rank / openai_count

# Print results
print(f'avg rank of manually chosen topics: {avg_manual_rank:.2f}')
print(f'avg rank of claude chosen topics: {avg_claude_rank:.2f}')
print(f'avg rank of gemini chosen topics: {avg_gemini_rank:.2f}')
print(f'avg rank of openai chosen topics: {avg_openai_rank:.2f}')

# ----------------------------
# Visualization
# ----------------------------
rank_data = {
    'Claude Sonnet 4': avg_claude_rank,
    'GPT-4.1': avg_openai_rank,
    'Expert': avg_manual_rank,
    'Gemini 2.5 Pro': avg_gemini_rank
}

# Sort results by rank (ascending)
sorted_items = sorted(rank_data.items(), key=lambda x: x[1])
labels, ranks = zip(*sorted_items)

# Define custom color map
color_map = {
    'Claude Sonnet 4': (100/255, 130/255, 180/255),   # muted blue
    'GPT-4.1': (220/255, 200/255, 120/255),           # muted yellow
    'Gemini 2.5 Pro': (161/255, 77/255, 79/255),      # muted red
    'Expert': (0, 0, 0)                               # black
}
colors = [color_map[label] for label in labels]

# Plot
fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(labels, ranks, color=colors)

ax.set_ylim(0, 17)
ax.set_ylabel('Average Rank (Lower is Better)', fontsize=25)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)

# Annotate bars
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=30)

plt.tight_layout()
plt.savefig("ranking_metrics/average_rank.png")
