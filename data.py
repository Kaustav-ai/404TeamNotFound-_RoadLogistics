import csv
import random
from datetime import datetime

def generate_memory_sample(truck, load, decision, score):
    accepted = decision == "ACCEPT"

    actual_profit = load["profit_inr"] - random.randint(0, 300) if accepted else 0
    delay = random.uniform(0, 1.5) if accepted else 0
    fuel_used = random.randint(5, 15) if accepted else 0

    regret = 0
    if accepted and actual_profit < 800 and delay > 1:
        regret = 1

    return {
        "truck_state": truck,
        "load": load,
        "decision": decision,
        "decision_score": score,
        "outcome": {
            "actual_profit_inr": actual_profit,
            "delay_hours": round(delay, 2),
            "fuel_used_percent": fuel_used
        },
        "future_state": {
            "time_left_hours": truck["time_left_hours"] - load["additional_time_hours"],
            "capacity_left_tons": truck["capacity_left_tons"] - load["load_weight_tons"]
        },
        "regret": regret,
        "timestamp": datetime.now().isoformat()
    }

def write_memory_to_csv(filename, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

memory_data = []

for _ in range(1000):   # 300 rows = perfect hackathon size
    truck = {
        "fuel_percent": random.randint(20, 80),
        "time_left_hours": round(random.uniform(2, 6), 1),
        "capacity_left_tons": random.randint(2, 10)
    }

    load = {
        "load_weight_tons": random.randint(1, 4),
        "additional_time_hours": round(random.uniform(0.5, 2), 1),
        "profit_inr": random.randint(500, 3000)
    }

    decision = random.choice(["ACCEPT", "REJECT"])
    score = round(random.uniform(-20, 30), 2)

    row = generate_memory_sample(truck, load, decision, score)
    memory_data.append(row)

write_memory_to_csv("decision_memory_dataset.csv", memory_data)
print("CSV file created successfully!")







