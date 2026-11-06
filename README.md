# Broadway Box Office: A Reproducible Two-Level Empirical Analysis

This project estimates associations between production characteristics and average weekly gross for 67 musicals, and separately explores total market gross over 501 observed weeks. Production OLS with HC3 uncertainty is checked against the supplied research paper. Market extensions use explicit formulas and HAC uncertainty; they are not exact reproductions of the original models.

## Reproduce

Use Python 3.12. Install `python -m pip install -r requirements.txt` and `python -m pip install -e . --no-deps`.

Run `python -m broadway_research.pipeline --input-dir /path/to/authorized/private_inputs --output-dir .`, then `python -m pytest -q`.

The input directory must contain the original six-sheet analysis workbook. It is not distributed: source redistribution rights have not been established. No synthetic substitute is provided. Artifact tests run on the generated outputs; scientific regeneration requires authorized source access.

## Explore

Run `python -m http.server 8000 --directory docs` and open http://localhost:8000. Interactive charts bundle Plotly and work without external JavaScript services.

- [Results](research/results.md)
- [Methods](research/methodology.md)
- [Limitations](research/limitations.md)
- [Reproducibility](research/reproducibility.md)
- [Source coverage](research/source_coverage.md)
- [Data dictionary](results/data_dictionary.csv)

## Publication boundary

The public demo exposes aggregate model summaries only. Regenerating the pipeline creates detailed charts with embedded observations: do not publish regenerated detailed charts without source redistribution authorization. Original documents are excluded. No data or code license is asserted on behalf of the owner.

Once rights are confirmed, create a GitHub repository, push this directory and enable GitHub Pages from the main branch, `/docs` folder. The static demo requires no build service. Repository: https://github.com/shacocn/broadway-box-office-research. Deployment status is available under Actions.
