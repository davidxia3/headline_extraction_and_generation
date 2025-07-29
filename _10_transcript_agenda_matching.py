import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from sentence_transformers import SentenceTransformer, util

# ============================ #
# Setup and Initialization     #
# ============================ #

load_dotenv()
CLAUDE_API_KEY = os.getenv('CLAUDE_KEY')
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

TRANSCRIPTS_DIR = Path("transcript_segments")
AGENDAS_DIR = Path("agenda_segments")


# ============================ #
# Semantic Matching Helpers    #
# ============================ #

def compute_top_k_matches(query: str, corpus: list[str], top_k: int = 3):
    """Compute top_k cosine similarity matches from corpus to the query string."""
    if query == "NO_SUMMARY":
        return [("NO_SUMMARY", 0.0)] * top_k

    query_emb = embedding_model.encode(query, convert_to_tensor=True)
    corpus_emb = embedding_model.encode(corpus, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, corpus_emb)[0]

    actual_k = min(top_k, len(corpus))
    top_indices = scores.topk(k=actual_k).indices.tolist()

    results = [(corpus[i], scores[i].item()) for i in top_indices]
    while len(results) < top_k:
        results.append(("NO_SUMMARY", 0.0))

    return results


def add_semantic_matches(transcript_path: Path, agenda_path: Path):
    """Adds top 3 semantic matches from agenda summaries to each transcript segment."""
    transcript_df = pd.read_csv(transcript_path)
    agenda_df = pd.read_csv(agenda_path)

    transcript_summaries = transcript_df["matching_summary"].fillna("").tolist()
    agenda_summaries = agenda_df["matching_summary"].fillna("").tolist()

    top_matches = [compute_top_k_matches(ts, agenda_summaries) for ts in transcript_summaries]

    for i in range(3):
        transcript_df[f"match{i+1}_summary"] = [matches[i][0] for matches in top_matches]
        transcript_df[f"match{i+1}_score"] = [matches[i][1] for matches in top_matches]

    transcript_df.to_csv(transcript_path, index=False)


# ============================ #
# LLM Prompting Utilities      #
# ============================ #

def build_llm_prompt(summary: str, candidates: list[str]) -> str:
    """Creates a prompt to select the best agenda summary matching the transcript summary."""
    candidate_lines = "\n".join(f"{i+1}. {c}" for i, c in enumerate(candidates))
    return f"""
You are a professional analyst assisting in matching a segment of a **city council meeting transcript** to the correct **agenda item summary**.

Below is a **summary of the transcript**, followed by the candidate agenda summaries. Your task is to select the best match based on:
- Named entities (e.g., **people**, **departments**, **projects**, **locations**)
- **Bill, ordinance, or resolution numbers**
- Procedural or organizational details
- Matching intent or decision

IMPORTANT:
- If none of the agenda summaries match clearly and specifically, return **0**
- Do NOT guess or return a weak/partial match
- Only respond with the number 1, 2, or 3 — or 0 if there is no good match

Transcript Summary:
\"\"\"{summary}\"\"\"

Candidate Agenda Summaries:
{candidate_lines}

Your response: (just 0, 1, 2, or 3)
""".strip()


def call_llm_matcher(summary: str, candidates: list[str]) -> int:
    """Queries Claude to choose the best candidate agenda match."""
    prompt = build_llm_prompt(summary, candidates)
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        temperature=0,
        max_tokens=32,
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        return int(response.content[0].text.strip())
    except ValueError:
        return 0


# ============================ #
# LLM Match Application        #
# ============================ #

def assign_llm_matches(transcript_path: Path):
    """Use Claude to assign best agenda match for each transcript segment."""
    df = pd.read_csv(transcript_path)

    if "llm_match" in df.columns:
        print(f"Skipping (already matched): {transcript_path.name}")
        return

    print(f"Matching: {transcript_path.name}")
    df["llm_match"] = 0

    for idx, row in df.iterrows():
        summary = row.get("matching_summary", "NO_SUMMARY")
        if summary == "NO_SUMMARY":
            continue

        candidates = []
        for i in range(1, 4):
            match_summary = row.get(f"match{i}_summary", "NO_SUMMARY")
            if match_summary != "NO_SUMMARY":
                candidates.append(match_summary)

        if not candidates:
            continue

        df.at[idx, "llm_match"] = call_llm_matcher(summary, candidates)

    df.to_csv(transcript_path, index=False)


# ============================ #
# Main Pipeline                #
# ============================ #

def run_matching_pipeline():
    for transcript_file in TRANSCRIPTS_DIR.rglob("*.csv"):
        agenda_file = AGENDAS_DIR / f"{transcript_file.stem}.csv"

        if not agenda_file.exists():
            print(f"Missing agenda for: {transcript_file.stem}")
            continue

        # Step 1: Add top-3 matches
        df = pd.read_csv(transcript_file)
        if "match1_summary" not in df.columns:
            add_semantic_matches(transcript_file, agenda_file)

        # Step 2: Use Claude to choose best match
        assign_llm_matches(transcript_file)


if __name__ == "__main__":
    run_matching_pipeline()
