# Data Benchmarking Note

## Purpose
This project uses a synthetically generated dataset (via `pandas`, `numpy`, and `faker`) rather than a real company dataset, for privacy and reproducibility reasons. To ensure the synthetic data is analytically credible, its key metric — employee attrition rate — is benchmarked against published Indian IT-industry figures.

## Comparison

| Metric | This Project (Synthetic) | Real Industry Benchmark |
|---|---|---|
| Overall attrition rate | 9.70% | ~12.7% (Q1FY25, top 6 IT services firms — TCS, Infosys, HCLTech, Wipro, TechM, LTIMindtree)¹ |
| Historical range | — | Peaked above 20% in 2022, declined for 7 consecutive quarters before stabilizing¹ |

¹ Source: NASSCOM Community, *Tech Industry Insights: Q1FY25 Performance Overview*.

## Interpretation
The synthetic dataset's 9.70% attrition rate sits slightly below the most recent stabilized industry figure (12.7%) but well within a realistic range for the sector, especially considering:

- Real attrition figures are pooled across large multinational firms with varied maturity, geography, and workforce composition.
- This project's synthetic data was deliberately calibrated to represent a mid-sized, single-organization workforce — a segment that can reasonably run a few points below large-firm aggregate averages due to more consistent role design and department structure.
- The gap (~3 percentage points) is small enough to be plausible variance, not a sign of unrealistic data generation.

## Conclusion
The synthetic dataset's attrition rate is directionally consistent with real Indian IT-industry benchmarks, supporting the credibility of downstream analysis (SQL insights, ML model, SHAP explainability, and the rupee-impact decision layer) built on top of it.