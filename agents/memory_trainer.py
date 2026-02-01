import pandas as pd

def load_and_train_memory(csv_path: str):
    df = pd.read_csv(csv_path)

    # -------- find decision column --------
    decision_col = None
    for col in ["decision", "decision_taken", "action", "final_decision", "status"]:
        if col in df.columns:
            decision_col = col
            break

    if decision_col is None:
        return {"bias": "neutral", "reason": "No decision column", "samples": 0}

    df["decision"] = df[decision_col].astype(str).str.upper()

    df["profit_actual"] = (
        df["actual_profit_inr"] if "actual_profit_inr" in df.columns
        else df["actual_profit"] if "actual_profit" in df.columns
        else 0
    )

    df["delay"] = (
        df["delay_hours"] if "delay_hours" in df.columns
        else df["delay"] if "delay" in df.columns
        else 0
    )

    accepted = df[df["decision"] == "ACCEPT"]

    if len(accepted) < 3:
        return {"bias": "neutral", "reason": "Insufficient data", "samples": len(accepted)}

    avg_profit = accepted["profit_actual"].mean()
    avg_delay = accepted["delay"].mean()

    if avg_profit < 800 and avg_delay > 1:
        return {
            "bias": "conservative",
            "avg_profit": round(avg_profit, 2),
            "avg_delay": round(avg_delay, 2),
            "samples": len(accepted),
            "reason": "Past accepts caused low profit and high delays"
        }

    if avg_profit > 1500 and avg_delay < 0.5:
        return {
            "bias": "aggressive",
            "avg_profit": round(avg_profit, 2),
            "avg_delay": round(avg_delay, 2),
            "samples": len(accepted),
            "reason": "Past accepts yielded high profit with low delay"
        }

    return {
        "bias": "neutral",
        "avg_profit": round(avg_profit, 2),
        "avg_delay": round(avg_delay, 2),
        "samples": len(accepted),
        "reason": "Mixed historical performance"
    }
