def time_tick(truck, journey, minutes=5):
    """
    Simulates real time passing (no buttons).
    """
    truck["fuel_percent"] = max(truck["fuel_percent"] - 0.5, 0)
    truck["time_left_hours"] = max(truck["time_left_hours"] - (minutes / 60), 0)

    journey["idle_hours"] += minutes / 60
    journey["urgency"] += 0.3

    return truck, journey
