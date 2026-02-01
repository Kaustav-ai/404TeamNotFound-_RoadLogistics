# =========================
# FINAL: data/truck_state.py
# =========================
import random

def get_truck_state(prev=None):
    """
    Returns a dynamic truck state.
    If prev is given, updates it realistically.
    """
    if not prev:
        return {
            "latitude": 18.5204 + random.uniform(-0.02, 0.02),
            "longitude": 73.8567 + random.uniform(-0.02, 0.02),
            "fuel_percent": random.randint(40, 80),
            "speed_kmph": random.randint(30, 70),
            "time_left_hours": round(random.uniform(3, 6), 1),
            "capacity_left_tons": random.randint(3, 10),
            "current_load": {
                "weight_tons": random.randint(1, 3),
                "destination": random.choice(["Mumbai", "Pune", "Nashik"])
            }
        }

    # realistic drift
    return {
        "latitude": prev["latitude"] + random.uniform(-0.005, 0.005),
        "longitude": prev["longitude"] + random.uniform(-0.005, 0.005),
        "fuel_percent": max(prev["fuel_percent"] - random.randint(1, 3), 0),
        "speed_kmph": max(0, prev["speed_kmph"] + random.randint(-5, 5)),
        "time_left_hours": max(round(prev["time_left_hours"] - 0.2, 1), 0),
        "capacity_left_tons": prev["capacity_left_tons"],
        "current_load": prev["current_load"]
    }
