import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

# ----------------------------
# Configuration
# ----------------------------
weeks = [
    ("20250331", "20250404"),
    ("20250407", "20250411"),
    ("20250414", "20250418"),
    ("20250421", "20250425")
]

# ----------------------------
# Helper Function
# ----------------------------
def list_to_rank_array(ordering):
    """Convert a list of topic indices into a rank array."""
    n = len(ordering)
    ranks = [0] * n
    for rank, topic_idx in enumerate(ordering):
        ranks[topic_idx] = rank
    return ranks

# ----------------------------
# Initialize Accumulators
# ----------------------------
total_co, total_cg, total_go = 0, 0, 0
valid_weeks = 0

# ----------------------------
# Main Loop over Weeks
# ----------------------------
for week in weeks:
    week_str = f"{week[0]}_{week[1]}"

    # Load label rankings
    claude_labels = pd.read_csv(f"human_evaluation_results/{week_str}_claude_only.csv")["label"]
    gemini_labels = pd.read_csv(f"human_evaluation_results/{week_str}_gemini_only.csv")["label"]
    openai_labels = pd.read_csv(f"human_evaluation_results/{week_str}_openai_only.csv")["label"]

    # Convert labels like "C23" to integers (23)
    claude_ranking = [int(x[1:]) for x in claude_labels]
    gemini_ranking = [int(x[1:]) for x in gemini_labels]
    openai_ranking = [int(x[1:]) for x in openai_labels]

    # Convert to rank arrays
    r_claude = list_to_rank_array(claude_ranking)
    r_gemini = list_to_rank_array(gemini_ranking)
    r_openai = list_to_rank_array(openai_ranking)

    # Compute Kendall's Tau
    tau_cg, _ = kendalltau(r_claude, r_gemini)
    tau_co, _ = kendalltau(r_claude, r_openai)
    tau_go, _ = kendalltau(r_gemini, r_openai)

    # Accumulate scores
    if None not in (tau_cg, tau_co, tau_go):
        total_cg += tau_cg
        total_co += tau_co
        total_go += tau_go
        valid_weeks += 1

# ----------------------------
# Compute Averages
# ----------------------------
avg_co = total_co / valid_weeks
avg_cg = total_cg / valid_weeks
avg_go = total_go / valid_weeks

print("Claude-Gemini:", avg_cg)
print("Claude-GPT:", avg_co)
print("Gemini-GPT:", avg_go)

# ----------------------------
# Bar Chart
# ----------------------------
labels = [
    'Gemini 2.5 Pro\nand GPT-4.1 Mini',
    'Claude Sonnet 4\nand Gemini 2.5 Pro',
    'GPT-4.1 Mini and\nClaude Sonnet 4'
]
scores = [avg_go, avg_cg, avg_co]
colors = [
    (191/255, 121/255, 74/255),   # Gemini-GPT
    (125/255, 107/255, 157/255),  # Claude-Gemini
    (107/255, 142/255, 107/255)   # Claude-GPT
]

# Sort by score
data = list(zip(labels, scores, colors))
data.sort(key=lambda x: x[1], reverse=True)
labels, scores, colors = zip(*data)

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(labels, scores, color=colors)

# Annotate values
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=30)

# Axis formatting
ax.set_ylim(0, 0.6)
ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
ax.set_ylabel("Kendall's Tau", fontsize=25)
# ax.set_title("LLM Generated Headlines Ranking Agreement", fontsize=30)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)

plt.tight_layout()
plt.savefig("_ranking_metrics/llm_ranking_agreement.png")
