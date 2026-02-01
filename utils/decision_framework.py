def build_decision_matrix(truck, load):
    """
    Extended decision matrix with additional context signals.
    Nothing removed from original logic.
    """

    # ---- BASE ACCEPT ----
    accept = {
        "profit": load["profit_inr"] / 100,
        "time_risk": - (load["additional_time_hours"] / truck["time_left_hours"]) * 30,
        "capacity": (load["load_weight_tons"] / truck["capacity_left_tons"]) * 10,
        "future": -10 if truck["time_left_hours"] - load["additional_time_hours"] < 1 else 0,
        "safety": -15 if truck["fuel_percent"] < 30 else 0,
    }

    # ---- ADDITIVE SIGNALS ----
    # Market pressure: high profit loads are usually competitive
    market_pressure = 5 if load["profit_inr"] > 4000 else 0
    accept["market_pressure"] = market_pressure

    # Time buffer awareness
    remaining_time = truck["time_left_hours"] - load["additional_time_hours"]
    accept["buffer_bonus"] = 5 if remaining_time > 1.5 else 0

    # ---- REJECT ----
    reject = {
        "profit": 0,
        "time_risk": 0,
        "capacity": 0,
        "future": 10,
        "safety": 5,
        "stability": 5
    }

    # ---- WAIT ----
    wait = {
        "profit": -2,
        "time_risk": -5,
        "capacity": 0,
        "future": 15,
        "safety": 5,
        "option_value": 5
    }

    return {
        "ACCEPT": accept,
        "REJECT": reject,
        "WAIT": wait
    }


def score_option(option: dict):
    return round(sum(option.values()), 2)
