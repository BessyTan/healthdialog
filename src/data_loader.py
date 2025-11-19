# src/data_loader.py
import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_symptom_data(path: str | Path = None):
    if path is None:
        path = BASE_DIR / "data" / "symptom_guidelines.json"
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_clinical_faq(path: str | Path = None) -> pd.DataFrame:
    if path is None:
        path = BASE_DIR / "data" / "clinical_faq.csv"
    path = Path(path)
    return pd.read_csv(path)
