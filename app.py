# =========================
# FleetMind – FINAL app.py
# =========================

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pydeck as pdk
from dotenv import load_dotenv
from datetime import datetime

from agents.vehicle_agent import vehicle_agent
from agents.journey_state import init_journey
from agents.time_engine import time_tick
from data.truck_state import get_truck_state
from data.load_source import fetch_live_load
from utils.notifications import send_driver_alert

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RouteWise",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION ----------------
if "truck_state" not in st.session_state:
    st.session_state.truck_state = get_truck_state()
if "journey" not in st.session_state:
    st.session_state.journey = init_journey()
if "load_queue" not in st.session_state:
    st.session_state.load_queue = []
if "selected_load" not in st.session_state:
    st.session_state.selected_load = None
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "decision_log" not in st.session_state:
    st.session_state.decision_log = []

truck = st.session_state.truck_state
journey = st.session_state.journey

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background:#0b1220; color:#e5e7eb; }

.header { font-size:28px; font-weight:700; }
.sub { color:#9ca3af; margin-bottom:10px; }

.kpi {
    background:#0f172a; border:1px solid #1e293b;
    padding:16px; border-radius:14px;
}
.kpi h4 { color:#9ca3af; font-size:13px; margin:0; }
.kpi h2 { margin:0; font-size:22px; }

.panel {
    background:#0f172a; border:1px solid #1e293b;
    padding:16px; border-radius:14px; margin-bottom:14px;
}

.ai-box {
    background:#020617; border:1px solid #2563eb;
    padding:16px; border-radius:14px;
}

.accept { border-left:5px solid #22c55e; }
.reject { border-left:5px solid #ef4444; }
.wait   { border-left:5px solid #facc15; }

.badge {
    display:inline-block; padding:4px 10px;
    border-radius:999px; font-size:12px;
}

.high { background:#14532d; color:#dcfce7; }
.medium { background:#713f12; color:#fef3c7; }
.low { background:#7f1d1d; color:#fee2e2; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header'>ROUTE_WISE</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>AI-assisted fleet decision dashboard</div>", unsafe_allow_html=True)
st.divider()

# ---------------- KPI ROW ----------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.markdown("<div class='kpi'><h4>Active Vehicles</h4><h2>1 / 1</h2></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi'><h4>Fuel</h4><h2>{truck['fuel_percent']}%</h2></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi'><h4>Speed</h4><h2>{truck['speed_kmph']} km/h</h2></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi'><h4>Time Left</h4><h2>{round(truck['time_left_hours'],1)} hrs</h2></div>", unsafe_allow_html=True)
k5.markdown(f"<div class='kpi'><h4>Capacity</h4><h2>{truck['capacity_left_tons']} tons</h2></div>", unsafe_allow_html=True)
k6.markdown(f"<div class='kpi'><h4>Urgency</h4><h2>{round(journey['urgency'],1)}</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([7, 3])

# ================= LEFT: MAP =================
with left:
    st.markdown("### 🗺️ Fleet Overview")

    layer = pdk.Layer(
        "ScatterplotLayer",
        [{"lat": truck["latitude"], "lon": truck["longitude"]}],
        get_position=["lon","lat"],
        get_radius=600,
        get_fill_color=[59,130,246]
    )

    view = pdk.ViewState(
        latitude=truck["latitude"],
        longitude=truck["longitude"],
        zoom=9
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

    if st.button("⏱ Advance Time (5 min)"):
        st.session_state.truck_state, st.session_state.journey = time_tick(
            st.session_state.truck_state,
            st.session_state.journey,
            minutes=5
        )
        st.rerun()

# ================= RIGHT: DECISION FLOW =================
with right:

    # ---- LOAD QUEUE ----
    st.markdown("### 📦 Incoming Loads")

    if st.button("➕ Fetch New Load"):
        st.session_state.load_queue.append(fetch_live_load())

    if not st.session_state.load_queue:
        st.info("No incoming loads yet.")
    else:
        for i, load in enumerate(st.session_state.load_queue):
            if st.button(
                f"{load.get('destination','Unknown')} • ₹{load.get('profit_inr',load.get('profit'))}",
                key=f"load_{i}"
            ):
                st.session_state.selected_load = load
                st.session_state.ai_result = None

    # ---- SELECTED LOAD ----
    if st.session_state.selected_load:
        load = st.session_state.selected_load
        st.markdown("### 📄 Selected Load")

        st.markdown(f"""
        <div class='panel'>
            <b>Destination:</b> {load.get("destination","-")}<br>
            <b>Weight:</b> {load.get("load_weight_tons", load.get("weight"))} tons<br>
            <b>Extra Time:</b> {load.get("additional_time_hours", load.get("extra_time"))} hrs<br>
            <b>Profit:</b> ₹{load.get("profit_inr", load.get("profit"))}
        </div>
        """, unsafe_allow_html=True)

        # ---- AI REVIEW BUTTON (RESTORED) ----
        if st.button("🧠 AI Review Load"):
            decision, explanation = vehicle_agent(
                st.session_state.truck_state,
                load,
                st.session_state.journey
            )
            st.session_state.ai_result = (decision, explanation)

    # ---- AI RESULT ----
    if st.session_state.ai_result:
        decision, explanation = st.session_state.ai_result
        cls = "accept" if decision=="ACCEPT" else "reject" if decision=="REJECT" else "wait"
        confidence = "High" if decision=="ACCEPT" else "Low" if decision=="REJECT" else "Medium"
        badge = "high" if confidence=="High" else "low" if confidence=="Low" else "medium"

        st.markdown(f"""
        <div class='ai-box {cls}'>
            <b>AI Recommendation:</b> {decision}
            <span class='badge {badge}'>{confidence} confidence</span><br><br>
            {explanation.replace(chr(10), "<br>")}
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Accept Load"):
                send_driver_alert("✅ Load accepted")
                st.session_state.decision_log.append(
                    (datetime.now().strftime("%H:%M:%S"), "ACCEPT")
                )
        with c2:
            if st.button("❌ Decline Load"):
                send_driver_alert("❌ Load declined")
                st.session_state.decision_log.append(
                    (datetime.now().strftime("%H:%M:%S"), "DECLINE")
                )

    # ---- DECISION HISTORY ----
    if st.session_state.decision_log:
        st.markdown("### 🧾 Decision Timeline")
        for t, d in reversed(st.session_state.decision_log[-5:]):
            st.write(f"{t} → {d}")
