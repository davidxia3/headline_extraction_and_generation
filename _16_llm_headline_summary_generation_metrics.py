from rouge_score import rouge_scorer
from bert_score import score as bert_score
from pathlib import Path
import pandas as pd

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)


def avg_rouge(true_list, gen_list):
        agg = {'rouge1': {'precision': [], 'recall': [], 'f1': []},
               'rouge2': {'precision': [], 'recall': [], 'f1': []},
               'rougeL': {'precision': [], 'recall': [], 'f1': []}}
        for t, g in zip(true_list, gen_list):
            scores = scorer.score(t, g)
            for rouge_type in agg:
                for k in ['precision', 'recall', 'fmeasure']:
                    score_val = getattr(scores[rouge_type], k)
                    agg[rouge_type][k if k != 'fmeasure' else 'f1'].append(score_val)
        # Average each score
        return {f'{r}_{k}': sum(v)/len(v) for r in agg for k, v in agg[r].items()}

# --- BERTScore ---
def avg_bert(true_list, gen_list):
    P, R, F1 = bert_score(gen_list, true_list, lang="en", verbose=False)
    return {
        'bert_precision': P.mean().item(),
        'bert_recall': R.mean().item(),
        'bert_f1': F1.mean().item()
    }


def compute_metrics_row(true_headlines, true_summaries, gen_headlines, gen_summaries):
    # Compute all scores
    metrics = {}

    # ROUGE for headlines
    rouge_headline = avg_rouge(true_headlines, gen_headlines)
    metrics.update({f'headline_{k}': v for k, v in rouge_headline.items()})

    # ROUGE for summaries
    rouge_summary = avg_rouge(true_summaries, gen_summaries)
    metrics.update({f'summary_{k}': v for k, v in rouge_summary.items()})

    # BERT for headlines
    bert_headline = avg_bert(true_headlines, gen_headlines)
    metrics.update({f'headline_{k}': v for k, v in bert_headline.items()})

    # BERT for summaries
    bert_summary = avg_bert(true_summaries, gen_summaries)
    metrics.update({f'summary_{k}': v for k, v in bert_summary.items()})

    return metrics




llms = ["claude", "gemini", "openai"]


columns = [
    "pipeline",
    "headline_rouge1_precision", "headline_rouge1_recall", "headline_rouge1_f1",
    "headline_rouge2_precision", "headline_rouge2_recall", "headline_rouge2_f1",
    "headline_rougeL_precision", "headline_rougeL_recall", "headline_rougeL_f1",
    "headline_bert_precision", "headline_bert_recall", "headline_bert_f1",
    "summary_rouge1_precision", "summary_rouge1_recall", "summary_rouge1_f1",
    "summary_rouge2_precision", "summary_rouge2_recall", "summary_rouge2_f1",
    "summary_rougeL_precision", "summary_rougeL_recall", "summary_rougeL_f1",
    "summary_bert_precision", "summary_bert_recall", "summary_bert_f1"
]

metrics_df = pd.DataFrame(columns=columns)


for llm in llms:
    folder = Path(f"reports_{llm}")

    true_headlines = []
    true_summaries = []
    generated_headlines = []
    generated_summaries = []
    for in_file in folder.rglob("*.csv"):
        df = pd.read_csv(in_file)

        for idx, row in df.iterrows():
            if row["true_headline"] == "NO_HEADLINE" or row["true_summary"] == "NO_SUMMARY":
                continue

            true_headlines.append(row["true_headline"])
            true_summaries.append(row["true_summary"])
            generated_headlines.append(row[f"{llm}_headline"])
            generated_summaries.append(row[f"{llm}_summary"])


    if len(true_headlines) > 0:
        metrics_df_row = compute_metrics_row(true_headlines, true_summaries, generated_headlines, generated_summaries)

        metrics_df_row["pipeline"] = f"{llm}_modular"


        metrics_df.loc[len(metrics_df)] = metrics_df_row
    else:
        print("skip (empty)")


metrics_df.to_csv("_reports_metrics/reports_metrics.csv", index=False)
