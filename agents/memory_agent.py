def memory_insight(truck, load):
    load_weight = (
        load.get("load_weight_tons")
        or load.get("weight_tons")
        or load.get("weight")
        or load.get("load_weight")
        or 0
    )

    extra_time = (
        load.get("additional_time_hours")
        or load.get("extra_time")
        or load.get("delay_hours")
        or 0
    )

    try:
        load_weight = float(load_weight)
    except:
        load_weight = 0

    try:
        extra_time = float(extra_time)
    except:
        extra_time = 0

    penalty = 0
    reason = "Memory neutral."

    if load_weight > truck["capacity_left_tons"]:
        penalty -= 10
        reason = "Memory: Heavy loads caused capacity stress."

    if extra_time > 1.5:
        penalty -= 5
        reason = "Memory: Similar loads caused delays."

    return penalty, reason
