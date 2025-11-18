import pandas as pd
import json
import os

def load_symptom_data(path="data/symptom_guidelines.json"):
    with open(path, "r") as f:
        return json.load(f)

def load_clinical_faq():
    path = os.path.join(os.path.dirname(__file__), "../data/clinical_faq.csv")
    return pd.read_csv(path)
