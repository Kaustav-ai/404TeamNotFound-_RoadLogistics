def risk_agent(truck, load):
    if load["load_weight_tons"] > truck["capacity_left_tons"]:
        return "High risk: capacity exceeded."
    if load["additional_time_hours"] > truck["time_left_hours"]:
        return "High risk: deadline miss."
    if truck["fuel_percent"] < 30:
        return "Medium risk: low fuel."
    return "Low risk."
    