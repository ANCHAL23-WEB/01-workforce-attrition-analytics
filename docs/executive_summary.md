# Executive Summary: Workforce Attrition & Bench Utilization Analytics

## The Problem
Employee attrition and idle "bench" time are two of the most expensive, least visible costs in IT-services organizations. Replacing an employee typically costs a significant fraction of their annual salary, while employees sitting unassigned on the bench generate cost without generating revenue. Most organizations react to attrition after it happens — this project builds a system to anticipate it and act early.

## What Was Built
An end-to-end analytics pipeline that:

1. **Analyzes historical patterns** — using SQL to surface attrition rates by department, bench-related costs, and the relationship between time spent on the bench and the likelihood of an employee leaving.
2. **Predicts attrition risk** — a machine learning model (comparing Logistic Regression and Random Forest) that scores each employee's probability of leaving, tuned to correctly catch at-risk employees even though attrition is a relatively rare event in the data.
3. **Explains *why*** — using SHAP (SHapley Additive exPlanations), the model's predictions are broken down per employee, showing exactly which factors (bench days, tenure, salary, department, performance) are driving their risk — not just a black-box score.
4. **Translates risk into money** — a decision layer that converts each employee's attrition probability into an expected financial loss (probability × replacement cost), compares it against the cost of a retention intervention, and flags only the ~22% of cases where intervention is genuinely worth the spend.
5. **Visualizes it all** — an interactive Tableau dashboard with department-level drill-downs, hover tooltips, and a guided story flow for non-technical stakeholders.

## Why It's Trustworthy
The dataset is synthetically generated (for privacy and reproducibility) but calibrated against real industry data — the project's 9.70% attrition rate closely tracks NASSCOM-reported figures for Indian IT-services firms (~12.7% as of Q1FY25), confirming the synthetic data behaves realistically rather than arbitrarily.

## The Business Impact
Instead of treating retention as a blanket, expensive effort applied everywhere, this project identifies a focused, high-ROI shortlist of employees where a retention intervention would save the company more money than it costs — turning attrition management from a reactive HR task into a targeted, financially justified decision.

## Tools Used
Python (pandas, scikit-learn, SHAP), SQL (SQLite), Tableau, GitHub.