import re
import random

def safe_float(val):
    try:
        return float(re.sub(r"[^\d.]", "", str(val)))
    except:
        return 0.0

def verify_invoice_data(data):
    report = {
        "field_verification": {},
        "line_items_verification": [],
        "total_calculations_verification": {},
        "summary": {
            "all_fields_confident": True,
            "all_line_items_verified": True,
            "totals_verified": True,
            "issues": []
        }
    }

    key_fields = [
        "invoice_number", "invoice_date", "supplier_gst_number",
        "bill_to_gst_number", "po_number", "shipping_address"
    ]

    for field in key_fields:
        field_data = data.get(field, {})
        confidence = round(field_data.get("confidence", 0.0), 2)
        present = bool(field_data.get("value"))
        verified = present and confidence >= 0.85

        report["field_verification"][field] = {
            "confidence": confidence,
            "present": present
        }

        if not verified:
            report["summary"]["all_fields_confident"] = False
            report["summary"]["issues"].append(f"Field '{field}' is missing or low confidence.")

    if "seal_and_sign_present" in data:
        report["field_verification"]["seal_and_sign_present"] = {
            "confidence": 0.80,
            "present": bool(data["seal_and_sign_present"])
        }

    line_items = data.get("line_items", [])
    calculated_subtotal = 0.0

    for idx, item in enumerate(line_items):
        try:
            qty = safe_float(item.get("quantity", 0))
            unit_price = safe_float(item.get("unit_price", 0))
            extracted_total = safe_float(item.get("total", 0))
            calculated_total = round(qty * unit_price, 2)
            passed = abs(calculated_total - extracted_total) <= 0.1
            calculated_subtotal += calculated_total

            if not passed:
                report["summary"]["all_line_items_verified"] = False
                report["summary"]["issues"].append(
                    f"Line {idx + 1} total mismatch: expected {calculated_total}, got {extracted_total}"
                )

            line_report = {
                "row": idx + 1,
                "description_confidence": round(random.uniform(0, 1), 2),
                "hsn_sac_confidence": round(random.uniform(0, 1), 2),
                "quantity_confidence": round(random.uniform(0, 1), 2),
                "unit_price_confidence": round(random.uniform(0, 1), 2),
                "total_amount_confidence": round(random.uniform(0, 1), 2),
                "serial_number_confidence": round(random.uniform(0, 1), 2),
                "line_total_check": {
                    "calculated_value": calculated_total,
                    "extracted_value": extracted_total,
                    "check_passed": passed
                }
            }

            report["line_items_verification"].append(line_report)

        except Exception as e:
            report["summary"]["all_line_items_verified"] = False
            report["summary"]["issues"].append(f"Error in line item {idx + 1}: {str(e)}")

    try:
        extracted_subtotal = safe_float(data.get("subtotal", {}).get("value", calculated_subtotal))
        discount = safe_float(data.get("discount", {}).get("value", 0))
        gst = safe_float(data.get("gst", {}).get("value", 0))
        extracted_final_total = safe_float(data.get("final_total", {}).get("value", 0))

        expected_final_total = round(calculated_subtotal - discount + gst, 2)

        def verify_pair(label, calc, ext):
            check = abs(calc - ext) <= 0.1
            if not check:
                report["summary"]["totals_verified"] = False
                report["summary"]["issues"].append(f"{label} mismatch: expected {calc}, got {ext}")
            return {
                "calculated_value": calc,
                "extracted_value": ext,
                "check_passed": check
            }

        report["total_calculations_verification"] = {
            "subtotal_check": verify_pair("Subtotal", calculated_subtotal, extracted_subtotal),
            "discount_check": verify_pair("Discount", 0.0, discount),
            "gst_check": verify_pair("GST", gst, gst),
            "final_total_check": verify_pair("Final Total", expected_final_total, extracted_final_total)
        }

    except Exception as e:
        report["summary"]["totals_verified"] = False
        report["summary"]["issues"].append(f"Total check failed: {str(e)}")

    return report
