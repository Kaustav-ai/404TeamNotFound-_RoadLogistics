import pandas as pd
import os

CSV_PATH = "data/dynamic_supply_chain_logistics_dataset.csv"

def append_decision_to_csv(row: dict):
    df_new = pd.DataFrame([row])

    if os.path.exists(CSV_PATH):
        df_old = pd.read_csv(CSV_PATH)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(CSV_PATH, index=False)
