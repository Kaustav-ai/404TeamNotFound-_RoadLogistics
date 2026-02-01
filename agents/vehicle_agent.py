from agents.decision_scorer import decision_score
from agents.memory_agent import memory_insight
from agents.risk_engine import compute_risk
from agents.memory_trainer import load_and_train_memory


def normalize_load(load):
    return {
        "load_weight_tons": load.get("load_weight_tons") or load.get("weight") or 0,
        "additional_time_hours": load.get("additional_time_hours") or load.get("extra_time") or 0,
        "profit_inr": load.get("profit_inr") or load.get("profit") or 0,
        "destination": load.get("destination", "Unknown")
    }


def vehicle_agent(truck, load, journey):
    load = normalize_load(load)

    base = decision_score(truck, load)
    mem_delta, mem_msg = memory_insight(truck, load)
    risk = compute_risk(truck, journey)

    # 🔥 WAIT COST (NO FREE WAITING)
    idle_cost = journey["idle_hours"] * 100
    urgency_bonus = journey["urgency"]

    final_score = round(base + mem_delta - (risk / 10) - idle_cost / 100 + urgency_bonus, 2)

    if final_score >= 10:
        decision = "ACCEPT"
        confidence = "High"
    elif final_score <= -10:
        decision = "REJECT"
        confidence = "High"
    else:
        decision = "WAIT"
        confidence = "Medium"

    explanation = f"""
AI Decision: {decision}
Confidence: {confidence}

Numbers:
• Profit: ₹{load['profit_inr']}
• Extra time needed: {load['additional_time_hours']} hrs
• Time left today: {round(truck['time_left_hours'],2)} hrs
• Fuel left: {truck['fuel_percent']}%
• Risk score: {risk}/100
• Idle cost so far: ₹{round(idle_cost,0)}

Experience:
• {mem_msg}

Final Score = {final_score}
"""

    return decision, explanation
