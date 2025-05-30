import os
from pdf2image import convert_from_path
from ocr_utils import preprocess_image, extract_text
from extract_fields import extract_invoice_fields, extract_table
from verify_data import verify_invoice_data
from export_utils import save_as_json, save_as_excel
from seal_cropper import detect_and_crop_seal

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(OUTPUT_DIR)

for file in os.listdir(os.path.join('..', INPUT_DIR)):
    if file.lower().endswith('.pdf'):
        pdf_path = os.path.join('..', INPUT_DIR, file)
        pdf_name = os.path.splitext(file)[0]

        invoice_output_dir = pdf_name
        os.makedirs(invoice_output_dir, exist_ok=True)

        pages = convert_from_path(pdf_path)

        all_text, all_data = [], []
        for page_idx, page in enumerate(pages):
            processed_img = preprocess_image(page)
            text, data = extract_text(processed_img)

            print(f"--- Page {page_idx + 1} extracted text (first 100 chars) ---")
            print(text[:100])
            print(f"Detected {len(data['text'])} text segments on page {page_idx + 1}")

            all_text.append(text)
            all_data.append(data)

        invoice_text = "\n".join(all_text)
        invoice_data = extract_invoice_fields(invoice_text, all_data)
        invoice_data["line_items"] = extract_table(all_data)

        seal_present, seal_path = detect_and_crop_seal(pages[0], pdf_name, invoice_output_dir)
        invoice_data["seal_and_sign_present"] = seal_present
        invoice_data["seal_image_path"] = seal_path

        verification_report = verify_invoice_data(invoice_data)

        save_as_json(invoice_data, os.path.join(invoice_output_dir, 'extracted_data.json'))
        save_as_excel(invoice_data, os.path.join(invoice_output_dir, 'extracted_data.xlsx'))
        save_as_json(verification_report, os.path.join(invoice_output_dir, 'verifiability_report.json'))

        print(f"Processed {file}, output saved to {invoice_output_dir}\n")
