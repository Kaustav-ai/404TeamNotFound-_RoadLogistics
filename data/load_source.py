import random

def fetch_live_load():
    return {
        "weight": random.randint(1, 4),
        "extra_time": round(random.uniform(0.5, 2.0), 1),
        "profit": random.randint(800, 3000),
        "destination": random.choice(["Mumbai", "Pune", "Nashik"])
    }
