# Student reproduction guide

This guide walks through a complete rerun of the Broadway Box Office Research repository using an authorized source workbook. It assumes moderate Python familiarity and no prior knowledge of this codebase.

## 1. Understand the evidence boundary first

The public repository does not contain the original paper, the six-sheet workbook, title-level source rows, weekly source rows, or the approximately 4,972 show-week records described by the paper. Do not download a substitute file and present it as the authorized source.

What the repository does provide is the complete Python implementation, executed notebooks, aggregate results, figures, dashboard, methodology, and tests. With the authorized workbook, you can rerun the published analysis end to end.

## 2. Prerequisites

You need:

- Python 3.11 or later; Python 3.12 is the validated environment.
- Git and a local clone of this repository.
- The authorized six-sheet `.xlsx` workbook in a private directory outside the public Git history.
- A notebook-capable editor that can use the project virtual environment, such as VS Code with Jupyter support or Jupyter installed in your existing environment.

Start in the repository root—the directory containing [`pyproject.toml`](../pyproject.toml), [`README.md`](../README.md), `src/`, `notebooks/`, and `results/`.

## 3. Clone and create the environment

```bash
git clone https://github.com/shacocn/broadway-box-office-research.git
cd broadway-box-office-research
python -m venv .venv
python -m pip install -e ".[research,test]"
```

Activate the environment if your editor requires it.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

If PowerShell prevents activation, use the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[research,test]"
```

## 4. Place and identify the authorized workbook

Create a private input directory that is not committed to Git. For example:

```text
broadway-box-office-research/
├── private_inputs/          # ignored by .gitignore
│   └── authorized_workbook.xlsx
├── notebooks/
├── results/
└── src/
```

The exact workbook filename is not important. [`ingest.load()`](../src/broadway_research/ingest.py) reads the first `.xlsx` file in the directory, selects the production table by the presence of a `Show` column, and selects the market table by `week_ending`.

Place only the intended authorized workbook in this directory. Multiple `.xlsx` files make “first file” selection ambiguous.

## 5. Set the input environment variables

The notebooks use `BROADWAY_INPUT_DIR`. The authorized-input integration tests use `BROADWAY_PRIVATE_INPUT_DIR`. Point both variables to the same private directory.

Windows PowerShell:

```powershell
$env:BROADWAY_INPUT_DIR = (Resolve-Path ".\private_inputs").Path
$env:BROADWAY_PRIVATE_INPUT_DIR = $env:BROADWAY_INPUT_DIR
```

macOS or Linux:

```bash
export BROADWAY_INPUT_DIR="$(pwd)/private_inputs"
export BROADWAY_PRIVATE_INPUT_DIR="$BROADWAY_INPUT_DIR"
```

Confirm that the path refers to a directory, not to the workbook file itself.

## 6. Run the complete pipeline

Windows PowerShell:

```powershell
python -m broadway_research.pipeline `
  --input-dir $env:BROADWAY_INPUT_DIR `
  --output-dir .
```

macOS or Linux:

```bash
python -m broadway_research.pipeline \
  --input-dir "$BROADWAY_INPUT_DIR" \
  --output-dir .
```

The final terminal output should be a JSON validation object with:

```json
{
  "status": "passed",
  "production_benchmarks_passed": true,
  "market_models_full_rank": true,
  "source_shapes": {
    "production": [67, 19],
    "market": [501, 21]
  },
  "generated_public_aggregate_tables": 8,
  "docs_preserved": true
}
```

The pipeline writes only to `results/` and `figures/`. It does not overwrite the maintained dashboard or research prose.

## 7. Run the notebooks in order

Open [`01_data_and_provenance.ipynb`](../notebooks/01_data_and_provenance.ipynb) first. Select the `.venv` Python kernel and use **Run All**. Continue in numerical order.

| Notebook | What it recomputes | What you should be able to explain afterward |
|---|---|---|
| [`01_data_and_provenance.ipynb`](../notebooks/01_data_and_provenance.ipynb) | Workbook loading, sheet roles, shapes, duplicates, positive values, log checks, missingness, and market coverage. | Why production and market rows are different units and why the private workbook is required. |
| [`02_exploratory_analysis.ipynb`](../notebooks/02_exploratory_analysis.ipynb) | Gross distribution, capacity relationship, and descriptive production groups. | Why a bivariate pattern is descriptive and not the main multivariable coefficient. |
| [`03_production_regression.ipynb`](../notebooks/03_production_regression.ipynb) | Paper-aligned production OLS, HC3 intervals, and benchmark differences calculated directly from the workbook. | How the 1.007385 capacity result is obtained and why it is not causal. |
| [`04_diagnostics_and_robustness.ipynb`](../notebooks/04_diagnostics_and_robustness.ipynb) | Rank, condition number, influence, residual checks, and four sensitivity samples. | Why no record is automatically discarded and why removing `Hamilton` changes categorical support. |
| [`05_market_analysis.ipynb`](../notebooks/05_market_analysis.ipynb) | Market gaps, unemployment missingness, HAC(8) models A-D, and the full-rank model C repair. | Why every market model is exploratory and why model C differs from the paper setup. |

Each code cell should receive an execution count and no cell should end with an error output. The committed notebooks contain 28 code cells in total.

## 8. Run the tests

```bash
python -m pytest -q
```

With `BROADWAY_PRIVATE_INPUT_DIR` set correctly, the integration tests rerun the real pipeline in a temporary directory. A successful authorized-input run should report all tests passed, not source-dependent skips.

The two test layers have different purposes:

- [`test_research.py`](../tests/test_research.py) validates benchmark tolerances, missingness, committed artifacts, notebook execution, dashboard assets, model rank, and documentation links.
- [`test_pipeline_integration.py`](../tests/test_pipeline_integration.py) runs `pipeline.run_pipeline()` with the authorized workbook, checks regenerated outputs, verifies small-cell suppression, and confirms that the maintained website survives regeneration.

## 9. Expected outputs

After a successful pipeline run, inspect these files first:

| File | Expected evidence |
|---|---|
| [`results/validation_summary.json`](../results/validation_summary.json) | Overall `passed` status, paper benchmarks true, and market models full rank. |
| [`results/paper_vs_python.csv`](../results/paper_vs_python.csv) | Four benchmark rows with `passed=True` and absolute differences below `1e-6`. |
| [`results/production_coefficients.csv`](../results/production_coefficients.csv) | `log_seats` estimate near `1.007384848`, HC3 p-value near `3.582e-05`, and interval near `0.529649` to `1.485121`. |
| [`results/robustness_results.csv`](../results/robustness_results.csv) | Sample sizes `[67, 66, 63, 51]` and a positive capacity estimate in all four samples. |
| [`results/missingness_by_year.csv`](../results/missingness_by_year.csv) | Missing unemployment totals sum to `244`; observed-week counts sum to `501`. |
| [`results/market_extensions.csv`](../results/market_extensions.csv) | Models A-D all have `full_rank=True`; repaired C has rank and columns both equal to 18 and R² near `0.707511`. |
| [`results/dashboard_data.json`](../results/dashboard_data.json) | Strict aggregate JSON with no `NaN` token or source rows. |

The pipeline also refreshes seven static files in [`figures/`](../figures/): capacity, gross distribution, missingness, residuals, coefficients, market trend, and group comparisons.

`results/influence.csv` is generated locally but ignored by Git. It contains observation-level diagnostic rows and is not part of the public publication set.

## 10. Verify the main result manually

Open [`results/production_coefficients.csv`](../results/production_coefficients.csv) and find the row where `term` is `log_seats`. Confirm:

- `estimate` ≈ `1.007384848`
- `ci95_lower` ≈ `0.529649100`
- `ci95_upper` ≈ `1.485120596`
- `p_hc3` ≈ `0.0000358202`

Then open [`results/paper_vs_python.csv`](../results/paper_vs_python.csv) and confirm that the `capacity` and `capacity_p` rows pass the tolerance check. This two-file check distinguishes the complete coefficient record from the paper benchmark verification.

## 11. Common failure points

### “Authorized source workbook not found”

- Confirm that `BROADWAY_INPUT_DIR` is set in the same terminal or editor session that starts the notebook.
- Confirm that the value is the containing directory, not the `.xlsx` path.
- Confirm that the directory contains exactly the intended workbook.

### The loader selects the wrong file or cannot find a table

- Remove unrelated `.xlsx` files from the input directory.
- Confirm that the authorized workbook contains a production worksheet with `Show` and a market worksheet with `week_ending`.
- Do not rename workbook columns to make a different dataset fit.

### A source-shape assertion fails

The validated extract is exactly 67 by 19 for production and 501 by 21 for market before derived variables. A different shape usually means a different workbook version, altered columns, or a different source file. Investigate provenance before changing the assertion.

### A production benchmark fails

Check that the workbook is unchanged, `numpy`, `pandas`, and `statsmodels` were installed from this project, and the production formula was not edited. Do not loosen the `1e-6` tolerance merely to make a changed result pass.

### Model C becomes rank deficient

Confirm that [`market_analysis.py`](../src/broadway_research/market_analysis.py) uses `time_years` and `post_reopening` rather than combining annual tourism with a full set of year indicators. `results/market_extensions.csv` should report rank `18`, columns `18`, and `full_rank=True` for C.

### Notebook imports fail

- Install the package with `python -m pip install -e ".[research,test]"` from the repository root.
- Select the `.venv` kernel.
- Open the notebooks from the repository's `notebooks/` directory so their project-root calculation is correct.

### Tests skip the integration layer

Set `BROADWAY_PRIVATE_INPUT_DIR` before running pytest. Public GitHub Actions intentionally lacks the workbook, so its source-dependent integration tests can skip while public artifact checks still run.

### Results appear in the wrong location

Pass the repository root as `--output-dir .`. A different output directory is useful for temporary validation but will not refresh the committed `results/` and `figures/` folders.

## 12. What a successful reproduction means

A successful run establishes that the provided authorized aggregate workbook produces the documented production benchmarks, diagnostics, robustness results, market extensions, and public aggregates under the repository's current code.

It does **not** establish access to the unavailable show-week microdata, prove a causal effect of capacity, reconstruct the paper's original market matrices, or grant permission to redistribute the workbook. Those limitations remain part of the correct reproduction result.

After reproducing, use [`paper_to_code_traceability.md`](paper_to_code_traceability.md) to connect individual values to files and [`student_demo_walkthrough.md`](student_demo_walkthrough.md) to prepare a concise explanation.
