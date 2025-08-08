import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# === Config ===
manual_dir = Path("sentences_manual")
model_dirs = {
    "claude": Path("sentences_claude"),
    "gemini": Path("sentences_gemini"),
    "openai": Path("sentences_openai")
}
output_csv = Path("sentences_metrics/sentences_metrics.csv")

# === Helper to compute metrics ===
def compute_metrics(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "precision_macro": precision_score(y_true, y_pred, average="macro"),
        "recall_macro": recall_score(y_true, y_pred, average="macro")
    }

# === Main ===
results = []

for model_name, model_dir in model_dirs.items():
    y_true_all = []
    y_pred_all = []

    for manual_file in manual_dir.glob("*.csv"):
        model_file = model_dir / manual_file.name
        if not model_file.exists():
            raise FileNotFoundError(f"Missing {model_file}")

        df_true = pd.read_csv(manual_file)
        df_pred = pd.read_csv(model_file)

        y_true_all.extend(df_true["classification"].astype(str).str.strip())
        y_pred_all.extend(df_pred["classification"].astype(str).str.strip())

    metrics = compute_metrics(y_true_all, y_pred_all)
    metrics["model"] = model_name
    results.append(metrics)

# Create dataframe, sort by f1_macro, and save
results_df = pd.DataFrame(results)
results_df = results_df[["model", "accuracy", "f1_macro", "f1_weighted", "precision_macro", "recall_macro"]]
results_df = results_df.sort_values(by="f1_macro", ascending=False).reset_index(drop=True)

results_df.to_csv(output_csv, index=False)

print(f"Saved metrics to {output_csv}")
print(results_df)
