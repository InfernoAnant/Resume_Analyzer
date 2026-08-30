import pdfplumber

class PDFExtractionError(Exception):
    pass

def extract_text_from_pdf(pdf_path):

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted
    except Exception as e:
        raise PDFExtractionError(f"We couldn't read this PDF — it may be corrupted or password-protected.")

    if len(text.strip()) < 50:
        raise PDFExtractionError("This looks like a scanned PDF with no selectable text. Please upload a text-based PDF.")

    return text