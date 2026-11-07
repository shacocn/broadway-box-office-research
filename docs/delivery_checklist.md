# Delivery and demo readiness checklist

Use this checklist immediately before repository delivery or a research meeting. Every checked item should be supported by a visible file, command result, or live page—not memory alone.

## Repository and environment

- [ ] The local branch is clean: `git status --short` returns no changed files.
- [ ] The local `main` commit matches `origin/main`.
- [ ] [Research artifact checks](https://github.com/shacocn/broadway-box-office-research/actions/workflows/ci.yml) are passing.
- [ ] [GitHub Pages deployment](https://github.com/shacocn/broadway-box-office-research/actions/workflows/pages.yml) is passing.
- [ ] The [live dashboard](https://shacocn.github.io/broadway-box-office-research/) loads over HTTPS.
- [ ] All six Plotly charts render, and the Gross/Attendance control works.

## Authorized-input reproduction

- [ ] The authorized workbook is stored outside public Git history.
- [ ] `BROADWAY_INPUT_DIR` points to the workbook's containing directory.
- [ ] `BROADWAY_PRIVATE_INPUT_DIR` points to the same directory for integration tests.
- [ ] `python -m broadway_research.pipeline --input-dir <authorized-directory> --output-dir .` completes with `status: passed`.
- [ ] `python -m pytest -q` passes with the authorized-input integration tests executed rather than skipped.
- [ ] [`validation_summary.json`](../results/validation_summary.json) reports production benchmarks passed and all market models full rank.

## Notebook readiness

- [ ] [`01_data_and_provenance.ipynb`](../notebooks/01_data_and_provenance.ipynb) runs and verifies the two source units and shapes.
- [ ] [`02_exploratory_analysis.ipynb`](../notebooks/02_exploratory_analysis.ipynb) runs and labels its comparisons as descriptive.
- [ ] [`03_production_regression.ipynb`](../notebooks/03_production_regression.ipynb) runs and recomputes the production model from the workbook.
- [ ] [`04_diagnostics_and_robustness.ipynb`](../notebooks/04_diagnostics_and_robustness.ipynb) runs and recomputes influence and all four sensitivity samples.
- [ ] [`05_market_analysis.ipynb`](../notebooks/05_market_analysis.ipynb) runs and verifies repaired model C is full rank.
- [ ] All 28 code cells have execution counts and no error outputs.

## Result provenance

- [ ] I can trace the `1.007385` capacity coefficient from Notebook 03 to `production_analysis.fit()`, [`production_coefficients.csv`](../results/production_coefficients.csv), and [`paper_vs_python.csv`](../results/paper_vs_python.csv).
- [ ] I can explain why the coefficient is elasticity-like but not causal.
- [ ] I can trace the four sensitivity samples to `production_analysis.samples()` and [`robustness_results.csv`](../results/robustness_results.csv).
- [ ] I can trace the 244 missing unemployment observations to Notebook 05, [`missingness_by_year.csv`](../results/missingness_by_year.csv), and the dashboard missingness chart.
- [ ] I can trace market models A-D to `market_analysis._specifications()`, `models()`, and [`market_extensions.csv`](../results/market_extensions.csv).
- [ ] I know which result file and code function generated each dashboard chart; if unsure, I can use [`paper_to_code_traceability.md`](paper_to_code_traceability.md).

## Interpretation readiness

- [ ] I can distinguish the **exact aggregate production reproduction** from the **exploratory market extensions**.
- [ ] I can explain that model C is both a methodological repair and an exploratory extension.
- [ ] I can explain why annual tourism and full year fixed effects are collinear.
- [ ] I can explain what HC3 addresses and what it does not address.
- [ ] I can explain what HAC(8) addresses and why repeated monthly or annual covariates remain a limitation.
- [ ] I can explain why missing unemployment makes the complete-case market sample time-selected.
- [ ] I can state that gross is nominal revenue, not profit or investor return.
- [ ] I can explain that the unavailable show-week microdata and original market matrices were not reconstructed.

## Contribution boundary

- [ ] I can state my actual individual contribution without claiming work I did not perform.
- [ ] I describe unperformed work as a repository feature, not as my personal authorship.
- [ ] I do not claim authorship of the source paper, original data collection, or redistribution rights.
- [ ] I do not claim causal identification from the production regression.
- [ ] I do not call market models A-D exact reproductions.
- [ ] I do not present model C's higher R² as evidence of a superior reproduction.
- [ ] I can explain the public/private boundary: code and aggregate outputs are public; the workbook and source rows remain private.

## Meeting flow

- [ ] I can give the 30-second summary without mixing production and market units.
- [ ] I can complete the 2-minute research overview using the live dashboard.
- [ ] I can complete the 3-minute code walkthrough using `ingest.py`, `production_analysis.py`, `market_analysis.py`, `pipeline.py`, and the relevant notebooks.
- [ ] I have the main results, traceability map, methodology, and limitations open before the meeting begins.
- [ ] I can use the transitions in [`student_demo_walkthrough.md`](student_demo_walkthrough.md) naturally rather than reading a scripted answer.
