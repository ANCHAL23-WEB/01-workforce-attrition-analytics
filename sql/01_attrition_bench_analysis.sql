-- ============================================
-- Workforce Attrition & Bench Utilization Analytics
-- Core SQL Analysis Queries
-- ============================================

-- 1. Attrition rate by department
SELECT department, COUNT(*) AS total_employees, SUM(attrition_flag) AS attrition_count,
       ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM employee_master
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- 2. Bench cost by department
SELECT e.department,
       SUM(f.bench_cost_incurred) AS total_bench_cost,
       ROUND(AVG(b.bench_days), 1) AS avg_bench_days
FROM employee_master e
JOIN bench_allocation b ON e.employee_id = b.employee_id
JOIN finance_cost f ON e.employee_id = f.employee_id
GROUP BY e.department
ORDER BY total_bench_cost DESC;

-- 3. Impact score — highest-value current employees (ranked by potential loss)
SELECT e.employee_id, e.name, e.department, e.performance_rating, e.tenure_years, e.salary,
       f.replacement_cost_estimate,
       ROUND(f.replacement_cost_estimate * (1 + e.tenure_years/10.0), 0) AS impact_score
FROM employee_master e
JOIN finance_cost f ON e.employee_id = f.employee_id
WHERE e.attrition_flag = 0
ORDER BY impact_score DESC
LIMIT 20;

-- 4. Bench days vs attrition rate — proves bench time predicts attrition
SELECT
  CASE
    WHEN b.bench_days = 0 THEN '0 days'
    WHEN b.bench_days BETWEEN 1 AND 30 THEN '1-30 days'
    WHEN b.bench_days BETWEEN 31 AND 60 THEN '31-60 days'
    ELSE '60+ days'
  END AS bench_bucket,
  COUNT(*) AS total_employees,
  SUM(e.attrition_flag) AS attrition_count,
  ROUND(100.0 * SUM(e.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM employee_master e
JOIN bench_allocation b ON e.employee_id = b.employee_id
GROUP BY bench_bucket
ORDER BY MIN(b.bench_days);