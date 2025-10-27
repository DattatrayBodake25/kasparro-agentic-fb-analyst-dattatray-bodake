## System Architecture Diagram

```mermaid
flowchart TD

    A[User Query<br>("Analyze ROAS drop")] --> B[Planner Agent]
    B --> C[Data Agent]
    C --> D[Insight Agent]
    D --> E[Evaluator Agent]
    E --> F[Creative Agent]
    F --> G[Report Generator]
    G --> H[(Final Reports<br>report.md, insights.json, creatives.json)]

    subgraph Data Flow
        I[(Dataset: data/synthetic_fb_ads_undergarments.csv)] --> C
        C --> D
        D --> E
        E --> F
        F --> G
    end

    style A fill:#f7f7f7,stroke:#333,stroke-width:1px
    style B fill:#ffdfba,stroke:#333,stroke-width:1px
    style C fill:#baffc9,stroke:#333,stroke-width:1px
    style D fill:#bae1ff,stroke:#333,stroke-width:1px
    style E fill:#ffffba,stroke:#333,stroke-width:1px
    style F fill:#ffb3ba,stroke:#333,stroke-width:1px
    style G fill:#d5b3ff,stroke:#333,stroke-width:1px
    style H fill:#f7f7f7,stroke:#333,stroke-width:1px
```

## Agent Roles and Responsibilities

### 1. Planner Agent
- Input: User query (e.g., "Analyze ROAS drop")
- Output: Structured plan with ordered subtasks
- Responsibilities:
   - Parse user intent and decompose into actionable tasks
   - Define sequence of agent calls and expected outputs
   - Ensure reasoning flow: Think → Analyze → Conclude

### 2. Data Agent
- Input: Dataset path from config (data/synthetic_fb_ads_undergarments.csv)
- Output: Summarized data (spend, impressions, CTR, ROAS trend, etc.)
- Responsibilities:
   - Load and validate dataset integrity
   - Compute quantitative metrics over time
   - Identify outliers and trends (e.g., declining ROAS, CTR drops)

### 3. Insight Agent
- Input: Data summary from Data Agent
- Output: Hypotheses explaining performance shifts (JSON structure)
- Responsibilities:
   - Generate potential causes for ROAS decline (e.g., audience fatigue, creative burnout)
   - Apply structured LLM prompts using "Think → Analyze → Hypothesize"
   - Return hypotheses with confidence scores and rationale

### 4. Evaluator Agent
- Input: Hypotheses + summarized dataset
- Output: Validated hypotheses with quantitative evidence
- Responsibilities:
   - Validate or reject hypotheses using statistical checks (e.g., correlation between CTR and ROAS)
   - Quantify confidence of each insight
   - Produce a structured evaluation summary

### 5. Creative Agent
- Input: Evaluated hypotheses + dataset
- Output: creatives.json — recommended new headlines, CTAs, and messages
- Responsibilities:
   - Identify underperforming campaigns or creatives
   - Use validated insights to propose improved messaging ideas
   - Generate structured creative recommendations with reasoning context

### 6. Report Generator
- Input: Outputs from all previous agents
- Output: Final markdown report (reports/report.md)
- Responsibilities:
   - Combine data summaries, validated insights, and creative suggestions
   - Produce a readable, structured report for marketers
   - Ensure traceability between raw data → reasoning → recommendations

### Design Principles
- Agentic Loop: Planner → Executor → Evaluator → Reporter
- Structured Prompts: Each LLM call follows a JSON or Markdown schema
- Traceable Outputs: Every step logs structured artifacts in reports/ and logs/
- Configurable: All paths, thresholds, and model parameters in config/config.yaml
- Reproducible: Deterministic seeds and small synthetic dataset ensure consistent evaluation
