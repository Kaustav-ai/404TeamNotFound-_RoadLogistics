def decision_score(truck, load):
    profit_score = load["profit_inr"] / 100
    time_penalty = (load["additional_time_hours"] / max(truck["time_left_hours"], 1)) * 40
    capacity_penalty = (load["load_weight_tons"] / max(truck["capacity_left_tons"], 1)) * 20

    return round(profit_score - time_penalty - capacity_penalty, 2)
