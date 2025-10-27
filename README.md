#  Kasparro Agentic Facebook Performance Analyst  
**Author:** Dattatray Bodake  
**Repository:** `kasparro-agentic-fb-analyst-dattatray-bodake`  
**Version:** v1.0  

---

##  Overview

This project implements a **multi-agent system** that autonomously diagnoses Facebook Ads performance, identifies causes behind **ROAS fluctuations**, and recommends **new creative directions** using both quantitative and creative data insights.

The system simulates an **agentic marketing analyst** — capable of planning, reasoning, validating hypotheses, and generating data-driven creative recommendations.

---

##  Objectives

The system is designed to:

- Diagnose **why ROAS changed** over time.
- Identify **drivers** behind changes (e.g., audience fatigue, creative underperformance).
- Propose **new creative ideas** for low-CTR campaigns.
- Generate an **end-to-end report** summarizing analysis, insights, and recommendations.

---

##  Agentic Architecture

###  Agent Flow Diagram

```mermaid
flowchart TD
    A[User Query: "Analyze ROAS Drop"] --> B[Planner Agent]
    B --> C[Data Agent]
    C --> D[Insight Agent]
    D --> E[Evaluator Agent]
    E --> F[Creative Agent]
    F --> G[Report Generator]
    G --> H[Final Report + Logs + JSON Outputs]

    style A fill:#ffd,stroke:#555
    style H fill:#cfc,stroke:#555
