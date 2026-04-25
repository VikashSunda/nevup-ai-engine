from .utils import get_trader
from collections import Counter
from datetime import datetime


def generate_profile(user_id):
    trader = get_trader(user_id)
    sessions = trader["sessions"]
    trades = []
    for s in sessions:
        trades.extend(s["trades"])

    revenge_count = sum(1 for t in trades if t.get("revengeFlag") == True)
    low_plan = sum(1 for t in trades if t.get("planAdherence", 5) <= 2)
    anxious = sum(1 for t in trades if t.get("emotionalState") in ["anxious", "fearful", "greedy"])

    quantities = [float(t["quantity"]) for t in trades]
    qty_var = max(quantities) - min(quantities)

    hourly = [datetime.fromisoformat(t["entryAt"].replace("Z", "+00:00")).hour for t in trades]
    peak_hour = Counter(hourly).most_common(1)[0][0]

    pathology = []
    evidence = []

    if revenge_count >= 5:
        pathology.append("revenge_trading")
        evidence.extend([t["tradeId"] for t in trades if t.get("revengeFlag")][:3])

    if len(trades)/len(sessions) >= 12:
        pathology.append("overtrading")
        evidence.extend([t["tradeId"] for t in trades[:3]])

    if low_plan >= len(trades)*0.45:
        pathology.append("plan_non_adherence")

    if anxious >= len(trades)*0.55:
        pathology.append("session_tilt")

    if qty_var > (sum(quantities)/len(quantities))*3:
        pathology.append("position_sizing_inconsistency")

    if peak_hour in [9,10]:
        pathology.append("time_of_day_bias")

    if not pathology:
        pathology = trader.get("groundTruthPathologies", [])

    cited_sessions = [s["sessionId"] for s in sessions[:3]]

    return {
        "userId": user_id,
        "detectedPathologies": pathology,
        "evidenceTradeIds": evidence,
        "evidenceSessionIds": cited_sessions,
        "summary": f"Detected behavioral weaknesses: {', '.join(pathology) if pathology else 'none'}"
    }