import csv
import re
import pandas as pd
from pathlib import Path
import whisper
import regex as regex  # for Unicode-aware regex
from deepmultilingualpunctuation import PunctuationModel

# Load models
asr_model = whisper.load_model("large")
punct_model = PunctuationModel()


def transcribe_audio(audio_path: Path) -> str:
    """Transcribe audio using Whisper."""
    print(f"Transcribing: {audio_path}")
    result = asr_model.transcribe(str(audio_path), language="en")
    return result["text"]


def clean_text(text: str) -> str:
    """Clean and normalize raw ASR output text."""
    # Remove tags like [music]
    text = re.sub(r"\[.*?\]", "", text)

    # Remove punctuation-based segment endings
    text = text.replace(". ", " ").replace("? ", " ").replace("! ", " ").replace(", ", " ")

    # Remove non-Latin characters
    text = regex.sub(r'[^\p{Latin}\d\p{P}\s]', '', text)

    # Normalize whitespace and remove filler words
    text = re.sub(r'\b(?:uh|um)+\b[,.]?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences based on punctuation."""
    sentences = re.findall(r'[^.!?]*[.!?]', text)
    return [s.strip() for s in sentences if s.strip()]


def punctuate_and_save(csv_output_path: Path, raw_text: str):
    """Clean, punctuate, and save sentence-level CSV."""
    cleaned_text = clean_text(raw_text)
    print(f"\nCleaned Transcript:\n{cleaned_text}\n")

    punctuated_text = punct_model.restore_punctuation(cleaned_text)
    print(f"\nPunctuated Transcript:\n{punctuated_text}\n")

    sentences = split_into_sentences(punctuated_text)

    with open(csv_output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sentence", "classification"])
        for sentence in sentences:
            writer.writerow([sentence, "x"])


def convert_sentences_to_transcript(sent_csv: Path, out_txt: Path):
    """Reconstruct full transcript from sentence-level CSV."""
    df = pd.read_csv(sent_csv)
    full_text = " ".join(df["sentence"].dropna().astype(str))
    
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(full_text)


def process_audio_folder(audio_dir: Path, output_sent_dir: Path, output_tran_dir: Path):
    """Main pipeline to transcribe and process all audio files in a directory."""
    for audio_file in audio_dir.rglob("*.wav"):
        print(f"\n=== Processing: {audio_file.name} ===")
        stem = audio_file.stem

        sentence_csv = output_sent_dir / f"{stem}.csv"
        transcript_txt = output_tran_dir / f"{stem}.txt"

        # Transcribe audio
        raw_text = transcribe_audio(audio_file)

        # Punctuate and save
        punctuate_and_save(sentence_csv, raw_text)

        # Reconstruct transcript text file
        convert_sentences_to_transcript(sentence_csv, transcript_txt)


# === Config & Execution ===
if __name__ == "__main__":
    AUDIO_INPUT_DIR = Path("_input_audios")
    SENTENCES_OUTPUT_DIR = Path("sentences_unlabeled")
    TRANSCRIPTS_OUTPUT_DIR = Path("transcripts")

    # Ensure output directories exist
    SENTENCES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    process_audio_folder(
        audio_dir=AUDIO_INPUT_DIR,
        output_sent_dir=SENTENCES_OUTPUT_DIR,
        output_tran_dir=TRANSCRIPTS_OUTPUT_DIR
    )
