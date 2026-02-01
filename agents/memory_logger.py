import csv
from datetime import datetime

MEMORY_FILE = "decision_memory_dataset.csv"

def log_decision(truck, load, decision, regret):
    row = {
        "load_weight_tons": load["load_weight_tons"],
        "additional_time_hours": load["additional_time_hours"],
        "profit_inr": load["profit_inr"],
        "fuel_percent": truck["fuel_percent"],
        "time_left_hours": truck["time_left_hours"],
        "capacity_left_tons": truck["capacity_left_tons"],
        "decision_taken": decision,
        "regret": regret,
        "timestamp": datetime.now().isoformat()
    }

    write_header = False
    try:
        open(MEMORY_FILE, "r").close()
    except FileNotFoundError:
        write_header = True

    with open(MEMORY_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)
