import csv
from typing import List, Dict
import os


def save_to_csv(filename: str, data: List[Dict]):
    data_keys = None
    header_required = os.path.exists(filename) is False

    if len(data) > 0:
        data_keys = data[0].keys()

    with open(filename, 'a', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data_keys)
        if header_required:
            writer.writeheader()
        writer.writerows(data)

