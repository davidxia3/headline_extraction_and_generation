import matplotlib.pyplot as plt
import pandas as pd

# === Configuration ===
weeks = [
    ("20250331", "20250404"),
    ("20250407", "20250411"),
    ("20250414", "20250418"),
    ("20250421", "20250425")
]

llms = ["claude", "gemini", "openai"]
llm_abbrev = {"claude": "C", "gemini": "G", "openai": "O"}

# === Displacement Tracking ===
displacements = {llm: 0 for llm in llms}
counts = {llm: 0 for llm in llms}

# === Processing Each Week ===
for week in weeks:
    week_str = f"{week[0]}_{week[1]}"
    df = pd.read_csv(f"human_evaluation_prep/{week_str}_filtered_headlines.csv")
    manual_indices = [idx for idx, row in df.iterrows() if row["manual_headline"] != "NO_HEADLINE"]

    # Load rankings for each LLM
    rankings = {
        llm: pd.read_csv(f"human_evaluation_results/{week_str}_manual_{llm}.csv")
        for llm in llms
    }

    # Compare ranks for each manual headline
    for llm in llms:
        abbrev = llm_abbrev[llm]
        ranking = rankings[llm]

        for mi in manual_indices:
            manual_label = f"M{mi}"
            llm_label = f"{abbrev}{mi}"

            manual_rank = ranking.loc[ranking["label"] == manual_label, "rank"].values[0]
            llm_rank = ranking.loc[ranking["label"] == llm_label, "rank"].values[0]
            displacement = manual_rank - llm_rank

            displacements[llm] += displacement
            counts[llm] += 1

# === Average Displacement Calculation ===
avg_displacements = {
    llm: displacements[llm] / counts[llm] for llm in llms
}
overall_avg = sum(displacements.values()) / sum(counts.values())

# === Bar Plot Data ===
data = {
    'Claude Sonnet 4': avg_displacements["claude"],
    'Gemini 2.5 Pro': avg_displacements["gemini"],
    'GPT-4.1 Mini': avg_displacements["openai"],
    'LLM Average': overall_avg
}

# === Sort Data ===
sorted_items = sorted(data.items(), key=lambda x: x[1])
labels, values = zip(*sorted_items)

# === Custom Colors ===
color_map = {
    'Claude Sonnet 4': (100/255, 130/255, 180/255),   # muted blue
    'Gemini 2.5 Pro': (161/255, 77/255, 79/255),      # muted red
    'GPT-4.1 Mini': (220/255, 200/255, 120/255),      # muted yellow
    'LLM Average': (101/255, 67/255, 33/255)          # deep brown
}
colors = [color_map[label] for label in labels]

# === Plotting ===
fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.barh(labels, values, color=colors)

ax.axvline(0, color='black', linewidth=4)
ax.set_xlim(-1, 8)
ax.set_xlabel('Average Rank Difference (LLM Higher than Expert)', fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

# Annotate bars
for bar in bars:
    width = bar.get_width()
    ax.annotate(
        f'{width:.1f}',
        xy=(width, bar.get_y() + bar.get_height() / 2),
        xytext=(5 if width > 0 else -5, 0),
        textcoords='offset points',
        ha='left' if width > 0 else 'right',
        va='center',
        fontsize=20,
        color='white' if width < 0 else 'black'
    )

plt.tight_layout()
plt.savefig("ranking_metrics/headline_rank_difference.png")
