# Student demo walkthrough

Use this as a meeting structure, not as a memorized script. Keep the repository open, point to the file that supports each claim, and distinguish paper benchmarks from new analysis every time the distinction matters.

## Before the meeting

Open these tabs in advance:

1. The [live dashboard](https://shacocn.github.io/broadway-box-office-research/).
2. [`paper_to_code_traceability.md`](paper_to_code_traceability.md).
3. [`03_production_regression.ipynb`](../notebooks/03_production_regression.ipynb).
4. [`04_diagnostics_and_robustness.ipynb`](../notebooks/04_diagnostics_and_robustness.ipynb).
5. [`05_market_analysis.ipynb`](../notebooks/05_market_analysis.ipynb).
6. [`results/paper_vs_python.csv`](../results/paper_vs_python.csv) and [`results/market_extensions.csv`](../results/market_extensions.csv).
7. [`research/limitations.md`](../research/limitations.md).

Check that the dashboard loads, the Gross/Attendance control responds, and the six Plotly charts render. Do not open or screen-share the private workbook unless the meeting context and data permissions explicitly allow it.

## 30-second project summary

Cover four points, in this order:

- The repository studies Broadway box office performance at two separate levels: 67 production aggregates and 501 observed market weeks.
- The production OLS model is an exact aggregate-level reproduction of the supplied paper benchmarks.
- The market regressions are transparent exploratory extensions because the original market design matrices are unavailable.
- The public repository adds a reproducible Python pipeline, executed notebooks, robust inference, diagnostics, privacy-aware aggregate outputs, tests, and an interactive dashboard.

Suggested transition: **“I will first show the exact production reproduction, then separate it from the exploratory market work.”**

## 2-minute research overview

### Research question and units

Explain that the production path asks which recorded production characteristics are associated with average weekly gross. The market path asks how Broadway-wide weekly gross varies with calendar and macroeconomic measures.

Point to the dashboard hero metrics: 67 productions, 501 weeks, production R² `0.608`, and HC3/HAC robust inference.

State clearly that the two datasets are not merged row for row. A production aggregate and a market week are different observational units.

### Main production result

Move to **Production → Coefficient estimates**. The main result is the `log_seats` coefficient of `1.007385`, with an HC3 95% interval from `0.529649` to `1.485121` and p = `0.0000358`.

Interpret it as an elasticity-like conditional association: a 1% capacity difference is associated with about a 1.01% difference in average weekly gross, holding included controls fixed.

Immediately add the limitation: high-demand productions may be allocated to larger theatres, so this is not the causal revenue effect of adding seats.

### Market evidence

Move to **Market → Annual market profile**, **Mean gross by month**, and **Unemployment coverage by year**. Explain that unemployment is missing for 244 of 501 weeks and that missingness is concentrated in earlier years. Complete-case macro models therefore describe a selected period.

End with **Market model fit**. Models A-D are exploratory, and C is a repaired specification rather than an exact reproduction.

Suggested transition: **“The dashboard summarizes the evidence; here is where each result is actually computed.”**

## 3-minute code walkthrough

### 1. Loading and validation

Open [`src/broadway_research/ingest.py`](../src/broadway_research/ingest.py). Show `load(path)` and explain that it selects the production worksheet by `Show`, the market worksheet by `week_ending`, and parses dates.

Then open [`01_data_and_provenance.ipynb`](../notebooks/01_data_and_provenance.ipynb). Show the assertions for source shapes, uniqueness, positive gross, transformation consistency, and missingness.

Suggested transition: **“Before any model is fit, the repository verifies that the expected research extract is present.”**

### 2. Production model

Open [`src/broadway_research/production_analysis.py`](../src/broadway_research/production_analysis.py). Point to:

- `formula(p)` for the exact predictor set.
- `fit(p)` for OLS with `cov_type='HC3'`.
- `samples(p)` for the four deterministic sensitivity samples.

Open [`03_production_regression.ipynb`](../notebooks/03_production_regression.ipynb) and show that it calls these functions, fits from the workbook, and calculates the benchmark comparison rather than merely displaying precomputed CSV values.

Suggested transition: **“This notebook reproduces the production model directly; the CSV is an output, not the analytical input.”**

### 3. Diagnostics and robustness

Open [`04_diagnostics_and_robustness.ipynb`](../notebooks/04_diagnostics_and_robustness.ipynb). Show the design-rank check, influence calculation, and sensitivity table. Mention that excluding `Hamilton` also removes the only HipHop category, which explains why that check changes categorical support.

### 4. Market extensions and repair

Open [`src/broadway_research/market_analysis.py`](../src/broadway_research/market_analysis.py). Show `_specifications()`, `_fit()`, and `models()`.

Point out that `_fit()` performs complete-case selection before constructing the design matrix and uses HAC with eight lags. In `models()`, show the construction of `time_years` and `post_reopening` for repaired model C.

Suggested transition: **“This model is exploratory rather than an exact reproduction because the original market matrix is unavailable, and model C requires a different full-rank design.”**

### 5. Pipeline and tests

Open [`src/broadway_research/pipeline.py`](../src/broadway_research/pipeline.py). Explain that `run_pipeline()` checks source shapes, benchmarks, missingness, and model rank, then writes `results/` and `figures/` without overwriting the curated website or research narrative.

Finish with [`tests/test_research.py`](../tests/test_research.py) and [`tests/test_pipeline_integration.py`](../tests/test_pipeline_integration.py). Explain the difference between public artifact validation and authorized-input end-to-end regeneration.

## Explaining the 1.007385 capacity coefficient

Use this five-step chain:

1. **Data:** the production worksheet contains 67 title-level aggregates, including `log_gross` and `log_seats`.
2. **Specification:** `production_analysis.formula()` includes `log_seats`, adaptation, revival, year, music style, and all `Plot_` indicators.
3. **Estimator:** `production_analysis.fit()` runs OLS and requests HC3 covariance.
4. **Output:** the `log_seats` row in [`production_coefficients.csv`](../results/production_coefficients.csv) contains estimate `1.007384848`, interval `0.529649–1.485121`, and p = `0.0000358`.
5. **Verification:** [`paper_vs_python.csv`](../results/paper_vs_python.csv) shows that the coefficient and p-value match the supplied paper benchmarks within `1e-6`.

Then separate interpretation from identification:

- Appropriate: **“Conditional on the recorded controls, a 1% capacity difference is associated with approximately a 1.01% gross difference.”**
- Inappropriate: **“Increasing capacity by 1% causes gross to increase by 1.01%.”**

Suggested transition: **“Here is where the result comes from, and here is the limit of what it can support.”**

## Explaining why model C needed repair

The paper context combines market gross, calendar controls, macro variables, and annual tourism. In the supplied data, annual tourism is repeated within each year. A full set of year indicators already spans all variables that are constant within year, so adding annual tourism creates exact collinearity and a rank-deficient design.

The public model C therefore:

- retains month effects;
- replaces full year fixed effects with continuous elapsed time (`time_years`);
- adds a coarse post-reopening indicator;
- retains unemployment, monthly sentiment, and annual tourism;
- uses complete cases and HAC(8) inference;
- verifies rank `18/18`.

Its R² is `0.707511`, compared with the paper-reported `0.671`. Do not present the higher R² as a better reproduction. The design changed, so the estimand and fit changed.

Suggested transition: **“The repair resolves a mathematical identification problem, but it also means this result belongs to the exploratory part of the repository.”**

## Explaining missingness and evidence limitations

Use [`missingness_by_year.csv`](../results/missingness_by_year.csv) or the dashboard missingness chart.

- Unemployment is missing for 244 of 501 weeks, or 48.7%.
- Missingness is concentrated by calendar period rather than scattered randomly.
- Models B-D use complete cases, so their samples emphasize later periods.
- Monthly sentiment and unemployment values repeat across weeks; annual tourism repeats even more broadly.
- HAC(8) addresses heteroskedasticity and short-run serial correlation in observed rows, but it does not create independent weekly variation in repeated macro values.
- Shutdown, reopening, and calendar gaps make the series structurally unusual.
- Gross is nominal revenue, not inflation-adjusted profit.

Suggested transition: **“These limitations do not invalidate the descriptive analysis, but they narrow the claims that can be made from it.”**

## What to claim as your contribution

Only claim work that you personally performed and can demonstrate. Use repository-level wording first, then specify your individual role accurately.

Repository-level contributions that are visible and auditable include:

- an independent Python reproduction of the supplied aggregate production benchmarks;
- explicit OLS/HC3 and exploratory OLS/HAC specifications;
- reproducible data validation, diagnostics, and prespecified sensitivity checks;
- identification and repair of the rank-deficient market model C extension;
- disclosure-controlled aggregate summaries that keep private source rows out of the public repository;
- five executed computational notebooks;
- an end-to-end pipeline, integration tests, CI, and GitHub Pages deployment;
- methodology, limitations, literature context, traceability, and an interactive dashboard.

Examples of honest individual contribution statements, when true:

- **“I implemented and verified the Python reproduction against the supplied paper benchmarks.”**
- **“I built or maintained the reproducible pipeline, notebook sequence, tests, and documentation.”**
- **“I audited the market specifications, documented the collinearity problem, and implemented the full-rank exploratory repair.”**
- **“I developed the public presentation layer using aggregate outputs while preserving the restricted-data boundary.”**
- **“I validated the repository end to end and can trace each published result to its code and output.”**

If you did not personally perform one of these tasks, describe it as a repository feature rather than your individual contribution.

## What not to overclaim

Do not say that you:

- authored the original paper or collected all original source data;
- possess or reconstructed the unavailable approximately 4,972 show-week records;
- proved that theatre capacity causally increases gross;
- exactly reproduced the market A-D models;
- improved model C merely because its R² is higher;
- inferred profitability, investor return, or operating cost from gross revenue;
- resolved source redistribution rights;
- created independent weekly macroeconomic variation from repeated monthly or annual values;
- validated conclusions beyond the supplied aggregate extract and documented period.

## Closing the meeting

End with three concrete points:

1. The aggregate production benchmarks reproduce exactly within tolerance.
2. The market work is useful but explicitly exploratory, with model C documented as a repair.
3. The repository is auditable from authorized input through notebooks, Python modules, results, figures, tests, and the live dashboard.

Suggested closing transition: **“The main value of this repository is not a stronger causal claim; it is that the evidence, assumptions, differences from the paper, and reproducibility boundary are all visible.”**

Use [`delivery_checklist.md`](delivery_checklist.md) for a final readiness check.
