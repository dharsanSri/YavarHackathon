import json
import pandas as pd
import os

def save_as_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Saved JSON to {path}")
    except Exception as e:
        print(f"[ERROR] Failed to save JSON: {e}")

def save_as_excel(data, path):
    try:
        line_items = data.get("line_items", [])
        print(f"[DEBUG] Preparing to write {len(line_items)} line items to Excel.")
        if len(line_items) > 0:
            print(json.dumps(line_items[:3], indent=2))

        df = pd.DataFrame(line_items)
        if df.empty:
            print(f"[WARNING] DataFrame is empty. No line items to write.")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            df.to_excel(path, index=False)
            print(f"[INFO] Saved Excel to {path}")
    except Exception as e:
        print(f"[ERROR] Failed to save Excel: {e}")
