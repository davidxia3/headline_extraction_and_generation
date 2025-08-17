import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =======================
# CONFIGURATION
# =======================
weeks = [
    ("20250331", "20250404"),
    ("20250407", "20250411"),
    ("20250414", "20250418"),
    ("20250421", "20250425")
]

llms = ["claude", "gemini", "openai"]
llm_abbrev = {"claude": "C", "gemini": "G", "openai": "O"}

# =======================
# HELPER FUNCTIONS
# =======================

def parse_label_ids(labels):
    return set(int(label[1:]) for label in labels)

def load_top_n_labels(week_str, model, n):
    df = pd.read_csv(f"human_evaluation_results/{week_str}_{model}_only.csv")
    return parse_label_ids(df.iloc[:n]["label"])

def load_llm_ranking_indices(week_str, llm, judge, num_manual):
    df = pd.read_csv(f"rankings_by_llm/{week_str}_{llm}_headlines_ranked_by_{judge}.csv")
    return parse_label_ids(df.iloc[:num_manual]["label"])

# =======================
# RECALL COUNTERS
# =======================

recall = {
    "manual_top3": 0,
    "manual_top5": 0,
    "claude_top3": 0,
    "claude_top5": 0,
    "gemini_top3": 0,
    "gemini_top5": 0,
    "openai_top3": 0,
    "openai_top5": 0
}

# =======================
# PROCESS EACH WEEK
# =======================

for week_start, week_end in weeks:
    week_str = f"{week_start}_{week_end}"
    df = pd.read_csv(f"ranking_prep/{week_str}_filtered_headlines.csv")
    manual_indices = set(df[df["manual_headline"] != "NO_HEADLINE"].index)

    # Load top-3 and top-5 for each LLM
    top3 = {llm: load_top_n_labels(week_str, llm, 3) for llm in llms}
    top5 = {llm: load_top_n_labels(week_str, llm, 5) for llm in llms}

    # Count overlap with manual
    recall["manual_top3"] += sum(len(top3[llm] & manual_indices) for llm in llms)
    recall["manual_top5"] += sum(len(top5[llm] & manual_indices) for llm in llms)

    # Load LLM rankings judged by each LLM
    num_manual = len(manual_indices)
    for judge in llms:
        judge_key_top3 = f"{judge}_top3"
        judge_key_top5 = f"{judge}_top5"
        for llm in llms:
            pred_indices = load_llm_ranking_indices(week_str, llm, judge, num_manual)
            recall[judge_key_top3] += len(top3[llm] & pred_indices)
            recall[judge_key_top5] += len(top5[llm] & pred_indices)

# =======================
# NORMALIZE RECALL VALUES
# =======================

num_weeks = len(weeks)
for key in recall:
    if "top3" in key:
        recall[key] /= (num_weeks * 3)
    elif "top5" in key:
        recall[key] /= (num_weeks * 5)

# =======================
# PRINT RESULTS
# =======================

for key, value in recall.items():
    print(f"{key.replace('_', ' ').capitalize()}: {value:.3f}")

# =======================
# PLOTTING
# =======================

group_labels = ['Gemini 2.5 Pro', 'Claude Sonnet 4', 'Expert', 'GPT-4.1']
values_top3 = [
    100 * recall["gemini_top3"] / 3,
    100 * recall["claude_top3"] / 3,
    100 * recall["manual_top3"] / 3,
    100 * recall["openai_top3"] / 3
]
values_top5 = [
    100 * recall["gemini_top5"] / 3,
    100 * recall["claude_top5"] / 3,
    100 * recall["manual_top5"] / 3,
    100 * recall["openai_top5"] / 3
]

x = np.arange(len(group_labels))
width = 0.35

# Color themes
color_top3 = {
    'Claude Sonnet 4': (100/255, 130/255, 180/255),
    'GPT-4.1': (220/255, 200/255, 120/255),
    'Gemini 2.5 Pro': (161/255, 77/255, 79/255),
    'Expert': (130/255, 130/255, 130/255)
}
color_top5 = {
    'Claude Sonnet 4': (50/255, 80/255, 130/255),
    'GPT-4.1': (140/255, 120/255, 50/255),
    'Gemini 2.5 Pro': (90/255, 40/255, 40/255),
    'Expert': (0, 0, 0)
}

fig, ax = plt.subplots(figsize=(13, 6))
bars_top3 = ax.bar(x - width/2, values_top3, width, color=[color_top3[g] for g in group_labels])
bars_top5 = ax.bar(x + width/2, values_top5, width, color=[color_top5[g] for g in group_labels])

ax.set_ylim(0, 70)
ax.set_ylabel('Percentage', fontsize=25)
ax.set_xticks(x)
ax.set_xticklabels(group_labels, fontsize=25)
ax.tick_params(axis='y', labelsize=20)

# Bar annotations
def annotate_bars(bars, label):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=20)
        ax.text(bar.get_x() + bar.get_width() / 2, height + 5, label,
                ha='center', va='bottom', fontsize=20)

annotate_bars(bars_top3, "Top 3")
annotate_bars(bars_top5, "Top 5")

plt.tight_layout()
os.makedirs("_ranking_metrics", exist_ok=True)
plt.savefig("_ranking_metrics/recall_rate.png")
