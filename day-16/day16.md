# Day 16: Stock Analysis & Career Intelligence

## Overview
Day 16 focused on two distinct but highly analytical domains: Financial Research and Career Strategy. The primary highlight was the development of the **Stock Fundamental Analyzer**, a sophisticated AI skill designed to provide evidence-based insights into Indian and global listed companies. Additionally, the challenge explored recruitment intelligence through a deep-dive "Red Flag" analysis for a Senior Data Science role.

## Prompts Used
### Stock Fundamental Analyzer
The core of today's technical work was the creation of a specialized system prompt for fundamental stock research.
- **Location:** [prompts/used Prompt](prompts/used%20Prompt)
- **Skill Objective:** Analyze NSE/BSE and global stocks using financial statements, business quality, and competitive advantages.
- **Key Frameworks:**
    - **Financial Metrics:** Automated interpretation of P/E (Valuation), D/E (Leverage), ROE/ROCE (Efficiency), and Interest Coverage (Risk).
    - **Analysis Modes:** Supports Quick Take (summary), Deep Dive (full HTML report), and Compare (side-by-side peer analysis).
    - **Strict Compliance:** Explicit rules against providing investment advice or buy/sell recommendations, focusing purely on educational, data-driven views.

## Outputs / Artifacts
### 1. Financial Research: TCS vs Infosys
Using the Stock Fundamental Analyzer, a comparative research report was generated for two giants of the Indian IT sector.
- **File:** [TCS_vs_Infosys_Research_Report.pdf](outputs/TCS_vs_Infosys_Research_Report.pdf)
- **Focus:** Evaluates CMP, Market Cap, Revenue/Profit CAGR, and Promoter holding trends to provide a neutral investor-style summary.

### 2. Career Strategy: Cvent Red Flag Report
This output applies analytical rigor to the recruitment process, specifically for a Senior Data Scientist position.
- **File:** [Cvent_Senior_DS_RedFlag_Report.pdf](outputs/Cvent_Senior_DS_RedFlag_Report.pdf)
- **Focus:** An intelligence report identifying potential "Red Flags" or areas of concern in a specific job role and company context, assisting in high-level career decision-making.

## Key Learnings
- **Evidence-Based AI:** Learned how to constrain AI to prioritize live data sources (Screener, Tickertape, Annual Reports) over general knowledge to ensure financial accuracy.
- **Structured Interpretation:** Developing clear thresholds for metrics (e.g., ROE > 15% as 'Good') allows the AI to provide consistent and objective evaluations.
- **Recruitment Intelligence:** Realized the value of using AI to audit job opportunities by cross-referencing role requirements with industry standards to identify potential career risks.
