from pathlib import Path
import json,pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[1]
def test_benchmarks():
 d=pd.read_csv(ROOT/'results/paper_vs_python.csv');assert d.passed.all();assert (abs(d.difference)<1e-6).all()
def test_samples():
 d=pd.read_csv(ROOT/'results/robustness_results.csv');assert d.n.tolist()==[67,66,63,51];assert d.formula.nunique()==1;assert np.allclose(d.r_squared,[.6079569056,.56809708,.5311222293,.6920474004],atol=1e-6)
def test_missingness():
 d=pd.read_csv(ROOT/'results/missingness_by_year.csv');assert d['sum'].sum()==244;assert d['count'].sum()==501;assert dict(zip(d.year,d['sum']))=={2015:31,2016:52,2017:53,2018:52,2019:52,2020:0,2021:0,2022:0,2023:0,2024:0,2025:4,2026:0}
def test_integrity():
 q=json.loads((ROOT/'results/qa.json').read_text());assert q['production_shape']==[67,19];assert q['market_shape']==[501,21];assert q['market_duplicate_dates']==0;assert q['nonpositive_gross']==0;assert q['log_gross_max_error']<1e-6
 def_unused=0
def test_artifacts():
 for name in ['capacity','gross_distribution','missingness','residuals','coefficients','market','groups']:assert (ROOT/f'figures/{name}.png').stat().st_size>1000
 for name in ['index','production','market']:assert (ROOT/f'docs/{name}.html').is_file()
