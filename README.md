# 🧾 Invoice OCR and Verification Pipeline

This project is an end-to-end pipeline to extract, verify, and export structured data from invoice PDFs using OCR and rule-based validation. It includes a modular architecture for image preprocessing, OCR, data extraction, verification, and export.

## 📁 Project Structure
```bash
project-root/
│
├── input/ # Folder to drop input invoice PDFs
├── output/invoice_with_metadata/ # Contains extracted results and reports
│ ├── extracted_data.json
│ ├── extracted_data.xlsx
│ ├── invoice_with_metadata.pdf
│ └── verifiability_report.json
│
├── main.py # Entry point of the pipeline
├── ocr_utils.py # OCR setup and inference (e.g. PaddleOCR)
├── extract_fields.py # Logic to extract fields and line items
├── verify_data.py # Field validation and verification logic
├── export_utils.py # Save outputs to JSON, Excel, and annotated PDF
├── seal_cropper.py # Tool to crop and embed seal images
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore file (exclude venv, etc.)
└── venv/ # Python virtual environment (excluded from Git)

```


## 🚀 Features

- Optical Character Recognition using PaddleOCR
- Field and table extraction (Invoice No, Date, Items, Serial Numbers, etc.)
- Data verifiability checks (GSTIN, totals, HSN/SAC code rules, etc.)
- Export to:
  - Annotated PDF with metadata
  - JSON and Excel formats
  - Verification report
- Seal/image stamping on PDF outputs

## ⚙️ Setup

1. **Clone the repo:**

   ```bash
   git clone https://github.com/your-username/invoice-ocr-pipeline.git
   cd invoice-ocr-pipeline
   ```
2. **Create a virtual environment and activate it:**

    ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   ```

3.**Install dependencies:**
   ```bash
  pip install -r requirements.txt
  ```

4.**Run the pipeline::**
```bash
python main.py
```




   
