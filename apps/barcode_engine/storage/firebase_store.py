import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "barcode_data"
DATA_DIR.mkdir(exist_ok=True)

FILE_PATH = DATA_DIR / "barcodes.json"


def save_barcode_record(record):
    record["saved_at"] = datetime.now().isoformat()

    if FILE_PATH.exists():
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
