# ROUTE_WISE
### *AI-assisted fleet decision dashboard*


> **Team:** 404TeamNotFound | **Hackathon:** Hackron 2026

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red) ![Groq](https://img.shields.io/badge/AI%20Speed-Groq-orange) ![Gemini](https://img.shields.io/badge/AI%20Logic-Gemini-blue) ![Twilio](https://img.shields.io/badge/Notifications-Twilio%20WhatsApp-green)

---

## The Problem
Modern logistics is rigid. Once a truck leaves the warehouse, it is "blind" to new opportunities or sudden risks.
* **Deadhead Problem:** Trucks often return empty, losing money.
* **Static Routing:** Drivers walk into traffic jams or weather hazards because plans were made days ago.
* **Communication Gaps:** Critical updates are missed due to poor network coverage.

## The Solution: OptiFleet
OptiFleet is a **Multi-Agent System (MAS)** that acts as a "Digital Co-Pilot" for logistics operators. It constantly scans for new high-profit loads, evaluates risks (weather/fragility), and autonomously communicates decisions to drivers via WhatsApp & SMS.

### Key Features
* **  Hybrid Brain Architecture:**
    * **Groq (Llama-3):** Handles high-speed reasoning and JSON parsing (Speed Layer).
    * **Google Gemini:** Validates complex math and profit logic (Logic Layer).
* **  Human-in-the-Loop Notifications:**
    * AI proposes a decision -> Human operator approves -> **Twilio** sends a WhatsApp message to the driver.
    * **Hybrid Connectivity:** Falls back to SMS if the driver has no data coverage.
* **  Multi-Agent Logic:**
    * `RiskAgent`: Analyzes cargo fragility and weather conditions.
    * `ProfitAgent`: Calculates fuel costs vs. new load revenue.
    * `VehicleAgent`: The orchestrator that makes the final Accept/Reject call.


##  Tech Stack

| Component | Technology | Usage |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Real-time dashboard for operators |
| **Fast AI** | Groq (Llama-3-8b) | Speed reasoning & decision making |
| **Smart AI** | Google Gemini 1.5 | Complex validation & math checks |
| **Comms** | Twilio API | Sending WhatsApp & SMS alerts |
| **Language** | Python | Core logic |

---

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Kaustav-ai/404TeamNotFound-_RoadLogistics.git](https://github.com/Kaustav-ai/404TeamNotFound-_RoadLogistics.git)
cd road-logistics_final
