def compute_risk(truck, journey):
    risk = 0

    if truck["fuel_percent"] < 30:
        risk += 20
    if truck["time_left_hours"] < 2:
        risk += 30
    if journey["rejected_loads"] >= 3:
        risk += 20
    if journey["urgency"] > 5:
        risk += 30

    return min(risk, 100)
