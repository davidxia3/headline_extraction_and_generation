import pdfplumber
from pathlib import Path


def process_pdf_to_text(pdf_path: Path, output_path: Path):
    """
    Extracts text from all pages of a PDF file and writes it to a text file.

    Parameters:
    - pdf_path (Path): Path to the input PDF file.
    - output_path (Path): Path where the extracted text will be saved as a .txt file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n\n"

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the extracted text to file
    output_path.write_text(all_text, encoding="utf-8")


def process_agendas(input_folder: Path, output_folder: Path):
    """
    Processes all agenda PDF files under a given input folder, extracting text and saving
    each as a corresponding .txt file in the output folder.

    Parameters:
    - input_folder (Path): Root folder containing PDF files (recursively).
    - output_folder (Path): Root folder to save the processed .txt files.
    """
    for pdf_path in input_folder.rglob("*.pdf"):
        file_stem = pdf_path.stem  
        
        output_txt_path = output_folder / f"{file_stem}.txt"

        print(f"Processing: {pdf_path}")
        process_pdf_to_text(pdf_path, output_txt_path)


if __name__ == "__main__":
    ##################################################### Define input/output folders
    input_agenda_folder = Path("_input_agendas")
    processed_agenda_folder = Path("processed_agendas")
    #####################################################

    # Process all agendas
    process_agendas(input_agenda_folder, processed_agenda_folder)