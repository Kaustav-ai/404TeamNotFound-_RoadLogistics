from agents.vehicle_agent import vehicle_agent
from agents.future_simulation_agent import simulate_future
from utils.memory_logger import log_decision

def orchestrate(truck, load, user_action=None):
    ai_text = vehicle_agent(truck, load)

    future_msg, future_penalty = simulate_future(truck, load)

    if user_action in ("ACCEPT", "REJECT"):
        regret = 1 if user_action == "ACCEPT" and future_penalty > 5 else 0
        log_decision(truck, load, user_action, regret)

    return ai_text + f"\nFuture Check:\n• {future_msg}"
