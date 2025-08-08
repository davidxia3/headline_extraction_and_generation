import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import anthropic
import google.generativeai as genai
from openai import OpenAI

# === Load Environment Variables ===
load_dotenv()

claude_client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))
genai.configure(api_key=os.getenv("GEMINI_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# === Configuration ===
INPUT_DIR = Path("sentences_unlabeled")
OUTPUT_DIRS = {
    "claude": Path("sentences_claude"),
    "gemini": Path("sentences_gemini"),
    "openai": Path("sentences_openai")
}

LABEL_MAP = {
    "beginning of new topic": "b",
    "beginning of new public comment topic": "p",
    "inside a topic": "i",
    "b": "b",
    "p": "p",
    "i": "i",
    "f": "f"
}

# === Prompt Builder ===
def make_prompt_with_context(prev2, prev1, target, next1, next2):
    return f"""
You are an expert meeting analyst. Your task is to classify a target sentence from a meeting transcript using its surrounding context.

There are exactly three possible labels:
- "beginning of new topic": the sentence starts a new discussion topic.
- "beginning of new public comment topic": the sentence starts a public comment section from citizens.
- "inside a topic": the sentence continues the current topic of discussion.

The sentence to classify is clearly marked below within >>> <<<. Do not analyze or explain. Return **only** one of the three labels as your final output.

Context:
{prev2}
{prev1}
>>> {target} <<<
{next1}
{next2}

Classification:
"""

# === LLM Query Functions ===
def ask_with_context_claude(row):
    prompt = make_prompt_with_context(row.get("prev2", ""), row.get("prev1", ""),
                                      row["sentence"], row.get("next1", ""), row.get("next2", ""))
    resp = claude_client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=4096,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text.strip().replace('"', '')

def ask_with_context_gemini(row):
    prompt = make_prompt_with_context(row.get("prev2", ""), row.get("prev1", ""),
                                      row["sentence"], row.get("next1", ""), row.get("next2", ""))
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    return resp.text.strip().replace('"', '')

def ask_with_context_openai(row):
    prompt = make_prompt_with_context(row.get("prev2", ""), row.get("prev1", ""),
                                      row["sentence"], row.get("next1", ""), row.get("next2", ""))
    resp = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=16
    )
    return resp.choices[0].message.content.strip().replace('"', '')

# === Core Processing Function ===
def process_files(model_name, classify_func):
    output_dir = OUTPUT_DIRS[model_name]
    output_dir.mkdir(exist_ok=True)

    for in_file in INPUT_DIR.rglob("*.csv"):
        out_file = Path(str(in_file).replace(str(INPUT_DIR), str(output_dir)))
        out_file.parent.mkdir(parents=True, exist_ok=True)

        if out_file.exists():
            continue

        df = pd.read_csv(in_file)
        df["sentence"] = df["sentence"].fillna("").astype(str)
        df = df[df["sentence"].str.strip() != ""]

        df["prev2"] = df["sentence"].shift(2).fillna("")
        df["prev1"] = df["sentence"].shift(1).fillna("")
        df["next1"] = df["sentence"].shift(-1).fillna("")
        df["next2"] = df["sentence"].shift(-2).fillna("")

        df["classification"] = df.apply(classify_func, axis=1)
        df["classification"] = df["classification"].map(LABEL_MAP).fillna("f")

        df.to_csv(out_file, index=False)
        print(f"Saved: {out_file}")

# === Run for All Models ===
process_files("claude", ask_with_context_claude)
process_files("gemini", ask_with_context_gemini)
process_files("openai", ask_with_context_openai)
