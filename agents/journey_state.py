from datetime import datetime

def init_journey():
    return {
        "start_time": datetime.now().isoformat(),
        "idle_hours": 0.0,
        "rejected_loads": 0,
        "accepted_loads": 0,
        "urgency": 0.0  # grows with time
    }


def update_journey(journey, minutes_passed):
    hours = minutes_passed / 60
    journey["idle_hours"] += hours
    journey["urgency"] += hours * 2   # urgency grows with time
    return journey
