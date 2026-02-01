def decision_prompt(truck, load, profit, risk, regret, score):
    return f"""
DECISION SCORE RULES:
- Score > +10  → ACCEPT
- Score between -10 and +10 → BORDERLINE
- Score < -10 → REJECT

Score: {score}

TRUCK STATUS:
Fuel: {truck['fuel_percent']}%
Time Left: {truck['time_left_hours']} hrs
Capacity Left: {truck['capacity_left_tons']} tons

CURRENT LOAD:
{truck['current_load']['weight_tons']} tons → {truck['current_load']['destination']}

INCOMING LOAD:
{load['load_weight_tons']} tons → {load['destination']}
Extra Time: {load['additional_time_hours']} hrs
Profit: ₹{load['profit_inr']}

AGENT SIGNALS:
- Profit Agent: {profit}
- Risk Agent: {risk}
- Regret Agent: {regret}

FORMAT:
Decision: ACCEPT or REJECT
Why:
- max 3 bullets
Confidence: High / Medium / Low
"""
