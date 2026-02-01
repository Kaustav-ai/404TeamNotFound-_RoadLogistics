def simulate_future(truck, load):
    penalty = 0

    future_time = truck["time_left_hours"] - load["additional_time_hours"]
    future_capacity = truck["capacity_left_tons"] - load["load_weight_tons"]

    if future_time < 1:
        penalty += 6
    if future_capacity < 1:
        penalty += 4
    if truck["fuel_percent"] < 25:
        penalty += 3

    if penalty == 0:
        return "Future state looks flexible.", 0

    return "Accepting may restrict future options.", penalty
