import re

def extract_invoice_fields(full_text, all_ocr_data):
    keywords = {
        "invoice_number": ["invoice no", "invoice number"],
        "invoice_date": ["invoice date", "date"],
        "supplier_gst_number": ["supplier gst", "supplier gstin", "supplier gst number"],
        "bill_to_gst_number": ["bill to gst", "bill to gstin", "bill to gst number"],
        "po_number": ["po number", "purchase order"],
        "shipping_address": ["shipping address"],
    }

    extracted_fields = {}
    flat_texts = []
    for page_data in all_ocr_data:
        flat_texts.extend(zip(page_data['text'], page_data['conf']))

    for field, labels in keywords.items():
        found = False
        for idx, (ocr_text, conf) in enumerate(flat_texts):
            text_lower = ocr_text.lower()
            for keyword in labels:
                if keyword in text_lower:
                    match = re.search(rf"{keyword}[:\-]?\s*(.+)", ocr_text, re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                    elif idx + 1 < len(flat_texts):
                        value = flat_texts[idx + 1][0].strip()
                    else:
                        value = ""

                    if field == "shipping_address":
                        value_lines = [value]
                        for offset in range(1, 3):
                            if idx + offset < len(flat_texts):
                                next_line = flat_texts[idx + offset][0].strip()
                                if len(next_line.split()) > 1:
                                    value_lines.append(next_line)
                        value = ", ".join(value_lines)

                    extracted_fields[field] = {
                        "value": value,
                        "confidence": round(conf, 2)
                    }
                    found = True
                    break
            if found:
                break

        if not found:
            extracted_fields[field] = {"value": None, "confidence": 0.0}

    return extracted_fields

def extract_table(all_ocr_data):
    table = []
    flat_lines = []

    for page_data in all_ocr_data:
        flat_lines.extend(page_data['text'])

    expected_headers = [
        "no_items",
        "description",
        "hsn_sac",
        "quantity",
        "unit_price",
        "total_amount",
        "serial_number"
    ]

    start_index = -1
    for i in range(len(flat_lines) - len(expected_headers) + 1):
        segment = [flat_lines[i + j].strip().lower() for j in range(len(expected_headers))]
        if segment == expected_headers:
            start_index = i
            break

    if start_index == -1:
        return []

    current_row = []
    for line in flat_lines[start_index + len(expected_headers):]:
        line_clean = line.strip()
        if not line_clean:
            continue
        current_row.append(line_clean)
        if len(current_row) == 7:
            row = {
                "serial_number": current_row[0],
                "description": current_row[1],
                "hsn_sac": current_row[2],
                "quantity": current_row[3],
                "unit_price": current_row[4],
                "total": current_row[5],
                "extra_serial_number": current_row[6]
            }
            table.append(row)
            current_row = []

    return table
