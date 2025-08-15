import pdfplumber
from pathlib import Path


def main():
    ######## CONFIGURATION ########
    input_agenda_folder = Path("agendas_raw")
    processed_agenda_folder = Path("agendas_processed")
    ###############################

    process_agendas(input_agenda_folder, processed_agenda_folder)


def process_pdf_to_text(pdf_path: Path, output_path: Path):
    """
    Extracts text from all pages of a PDF file and writes it to a TXT file.

    Parameters:
    - pdf_path (Path): Path object of the input PDF file.
    - output_path (Path): Path object of where the extracted text will be saved as a TXT file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(all_text, encoding="utf-8")


def process_agendas(input_folder: Path, output_folder: Path):
    """
    Processes all agenda PDF files under a given input folder, extracting text and saving
    each as a corresponding TXT file in the output folder.

    Parameters:
    - input_folder (Path): Path object of folder containing PDF files.
    - output_folder (Path): Path object of folder to save the processed TXT files.
    """
    for pdf_path in input_folder.rglob("*.pdf"):
        file_stem = pdf_path.stem  
        output_txt_path = output_folder / f"{file_stem}.txt"

        print(f"processing: {pdf_path}")

        # process individual file
        process_pdf_to_text(pdf_path, output_txt_path)


if __name__ == "__main__":
    main()
