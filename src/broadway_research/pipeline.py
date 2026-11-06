import argparse,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
from .ingest import load
from .production_analysis import fit,samples,formula
from .market_analysis import models
from .diagnostics import inspect

def main():
 a=argparse.ArgumentParser();a.add_argument('--input-dir',required=True);a.add_argument('--output-dir',default='.');args=a.parse_args();o=Path(args.output_dir)
 for d in ['results','figures','docs','research','data']: (o/d).mkdir(parents=True,exist_ok=True)
 p,m=load(args.input_dir);f=fit(p)
 assert p.shape==(67,19) and m.shape==(501,21)
 assert m.unemployment_rate_pct.isna().sum()==244
 expected={'r_squared':(.6079569056109908,f.rsquared),'capacity':(1.0073848481499095,f.params['log_seats']),'capacity_p':(3.582017220037733e-5,f.pvalues['log_seats']),'adapted':(.2867209169,f.params['Adapted'])}
 comparison=pd.DataFrame([dict(metric=k,benchmark=v[0],computed=v[1],difference=v[1]-v[0],passed=abs(v[1]-v[0])<1e-6) for k,v in expected.items()]);assert comparison.passed.all();comparison.to_csv(o/'results/paper_vs_python.csv',index=False)
 ci=f.conf_int();coef=pd.DataFrame(dict(estimate=f.params,se=f.bse,p=f.pvalues,lower=ci[0],upper=ci[1]));coef.to_csv(o/'results/production_coefficients.csv')
 robust=[]
 for name,s in samples(p).items():
  g=fit(s);c=g.conf_int().loc['log_seats'];robust.append(dict(sample=name,n=int(g.nobs),r_squared=g.rsquared,adjusted_r_squared=g.rsquared_adj,capacity=g.params['log_seats'],lower=c.iloc[0],upper=c.iloc[1],p=g.pvalues['log_seats'],formula=formula(p)))
 r=pd.DataFrame(robust);r.to_csv(o/'results/robustness_results.csv',index=False)
 missing=m.assign(missing=m.unemployment_rate_pct.isna()).groupby('year').missing.agg(['sum','count']);missing['rate']=missing['sum']/missing['count'];missing.to_csv(o/'results/missingness_by_year.csv')
 qa={'production_shape':list(p.shape),'market_shape':list(m.shape),'production_duplicates':int(p.duplicated().sum()),'market_duplicate_dates':int(m.week_ending.duplicated().sum()),'log_gross_max_error':float(abs(np.log(p.Avg_Gross_USD)-p.log_gross).max()),'seat_range':np.exp(p.log_seats).agg(['min','max']).to_dict(),'nonpositive_gross':int((m.market_gross_usd<=0).sum()),'date_min':str(m.week_ending.min()),'date_max':str(m.week_ending.max()),'style_counts':p.Music_Style.value_counts().to_dict(),'production_diagnostics':inspect(f),'unemployment_missing':244}
 (o/'results/qa.json').write_text(json.dumps(qa,indent=2))
 dictionary=pd.concat([pd.DataFrame({'level':level,'variable':d.columns,'dtype':d.dtypes.astype(str).values,'missing':d.isna().sum().values}) for level,d in [('production',p),('market',m)]],ignore_index=True);dictionary.to_csv(o/'results/data_dictionary.csv',index=False)
 inf=f.get_influence();pd.DataFrame({'observation':np.arange(len(p)),'leverage':inf.hat_matrix_diag,'cooks_distance':inf.cooks_distance[0],'residual':f.resid}).to_csv(o/'results/influence.csv',index=False)
 market=[]
 for k,(form,g) in models(m).items():
  market.append(dict(model=k,status='Exploratory extension; not exact reproduction',n=int(g.nobs),r_squared=g.rsquared,paper_n={'A':501,'B':257,'C':236,'D':257}[k],paper_r_squared={'A':.507,'B':.699,'C':.671,'D':.696}[k],formula=form,**inspect(g)))
  pd.DataFrame({'estimate':g.params,'p':g.pvalues,'lower':g.conf_int()[0],'upper':g.conf_int()[1]}).to_csv(o/f'results/market_{k}_coefficients.csv')
 market=pd.DataFrame(market);market.to_csv(o/'results/market_extensions.csv',index=False)
 def save(name):
  plt.tight_layout();plt.savefig(o/f'figures/{name}.png',dpi=180);plt.close()
 plt.scatter(np.exp(p.log_seats),p.Avg_Gross_USD/1e6);plt.xlabel('Theatre seats (back-transformed)');plt.ylabel('Average weekly gross (million USD)');save('capacity')
 plt.hist(p.Avg_Gross_USD/1e6,bins=15);plt.xlabel('Average weekly gross (million USD), N=67');plt.ylabel('Productions');save('gross_distribution')
 plt.bar(missing.index,missing['sum']);plt.ylabel('Weeks missing unemployment');plt.xlabel('Year');save('missingness')
 plt.scatter(f.fittedvalues,f.resid);plt.axhline(0,color='black');plt.xlabel('Fitted log gross');plt.ylabel('Residual');save('residuals')
 plt.figure(figsize=(9,9));plt.errorbar(coef.estimate,range(len(coef)),xerr=[coef.estimate-coef.lower,coef.upper-coef.estimate],fmt='o');plt.yticks(range(len(coef)),coef.index);plt.axvline(0,color='gray');plt.xlabel('OLS coefficient and HC3 95% interval');save('coefficients')
 market_sorted=m.sort_values('week_ending');segments=market_sorted.week_ending.diff().dt.days.gt(14).cumsum()
 for _,s in market_sorted.groupby(segments):plt.plot(s.week_ending,s.market_gross_usd/1e6)
 plt.xlabel('Week ending; gaps remain unconnected');plt.ylabel('Market gross (million USD)');save('market')
 groups=[]
 for v in ['Adapted','Revival']:
  for k,s in p.groupby(v):groups.append(dict(variable=v,value=int(k),n=len(s),mean=s.Avg_Gross_USD.mean(),se=s.Avg_Gross_USD.sem()))
 pd.DataFrame(groups).to_csv(o/'results/group_comparisons.csv',index=False)
 plt.bar(range(4),[x['mean']/1e6 for x in groups],yerr=[1.96*x['se']/1e6 for x in groups]);plt.xticks(range(4),[x['variable']+'='+str(x['value'])+' n='+str(x['n']) for x in groups],rotation=15);plt.ylabel('Mean gross (million USD); normal 95% intervals');save('groups')
 scatter=px.scatter(p.assign(seats=np.exp(p.log_seats)),x='seats',y='Avg_Gross_USD',color='Music_Style',hover_name='Show',labels={'Avg_Gross_USD':'Average weekly gross (USD)'})
 scatter.write_html(o/'docs/production.html',include_plotlyjs=True)
 timeline=px.line(market_sorted.assign(segment=segments.astype(str)),x='week_ending',y='market_gross_usd',line_group='segment');timeline.write_html(o/'docs/market.html',include_plotlyjs=True)
 limitations='The 67 production aggregates cannot reconstruct the unavailable 4,972 show-week records or selection trail. These are observational associations, not causal effects. Budgets, casting, pricing and marketing are unmeasured. Labels are provisional. Hamilton is the only HipHop production. Removing it changes category support. R-squared across different samples is not a model ranking. Unemployment is missing for 244 of 501 weeks (48.7%), systematically by time. Annual tourism and monthly macro indicators repeat across weeks. Pandemic shutdown and reopening create structural breaks. Original market design matrices are unavailable; current market estimates are exploratory. Annual tourism with year indicators creates collinearity. HAC uses eight successive observed rows, which need not be consecutive calendar weeks across gaps. No missing values are imputed. Source redistribution permission remains unconfirmed.'
 methods='Production OLS uses HC3 covariance and the exact formula: `'+formula(p)+'`. Categorical levels use sorted treatment coding; coefficient labels identify comparisons with the omitted baseline. Market extensions use month and year controls with HAC maximum lag 8, complete cases per formula, and chronological ordering. Their explicit formulas and matrix diagnostics are in results/market_extensions.csv. Seats are exp(log_seats), not independently verified capacity counts. Gross is nominal USD. No inflation adjustment is applied.'
 results='Production N=67; R-squared '+str(f.rsquared)+'; adjusted R-squared '+str(f.rsquared_adj)+'. Capacity elasticity '+str(f.params['log_seats'])+', 95% CI '+str(ci.loc['log_seats'].tolist())+', HC3 p='+str(f.pvalues['log_seats'])+'. A 1% capacity difference is associated with approximately 1.01% gross difference conditional on controls.\n\n'+comparison.to_markdown(index=False)+'\n\n'+r.drop(columns='formula').to_markdown(index=False)+'\n\n'+market.drop(columns='formula').to_markdown(index=False)
 for name,body in {'methodology':methods,'limitations':limitations,'results':results,'report':'## Abstract\n\n'+results+'\n\n## Methods\n\n'+methods+'\n\n## Discussion and limitations\n\n'+limitations,'reproducibility':'Install with `python -m pip install -e .` then run `python -m broadway_research.pipeline --input-dir /path/to/authorized/private_inputs --output-dir .` and `python -m pytest -q`. Original data must be obtained separately with authorization. Generated interactive charts embed source observations and require a rights review before public deployment.','source_coverage':'The supplied paper establishes reported benchmarks and methods. The six-sheet workbook supplies two analysis tables, production coefficients, selected market coefficients, model comparisons and provenance notes. Production coefficients are directly reproducible. Original upstream workbooks, acquisition snapshots, full market matrices and microdata are absent. Reference CSV files are secondary exports, not independent evidence.'}.items(): (o/f'research/{name}.md').write_text('# '+name.replace('_',' ').title()+'\n\n'+body,encoding='utf-8')
 html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Broadway Box Office Research</title><style>body{font:18px system-ui;color:#193044;background:#f7f5ef;max-width:1100px;margin:auto;padding:28px}a{color:#075985}iframe{width:100%;height:560px;border:0}table{font-size:13px;display:block;overflow:auto}section{padding:24px 0}img{max-width:100%}</style><h1>Broadway Box Office</h1><p>A Reproducible Two-Level Empirical Analysis</p><p>67 productions · 501 observed market weeks</p><nav><a href="#production">Production</a> · <a href="#market">Market</a> · <a href="#methods">Methods</a></nav><section id="production"><h2>Production characteristics</h2><p>Descriptive capacity–gross relationship. This scatter is not the multivariable coefficient and does not identify causality. Click legend entries to filter styles.</p><iframe title="Production capacity and gross" src="production.html"></iframe>'+comparison.to_html(index=False)+'<h2>Sensitivity analysis</h2>'+r.drop(columns='formula').to_html(index=False)+'</section><section id="market"><h2>Market conditions</h2><p>Observed periods are separated across gaps, including the pandemic shutdown. Exploratory models do not reproduce original A–D design matrices.</p><iframe title="Weekly market gross" src="market.html"></iframe>'+market.drop(columns='formula').to_html(index=False)+'<h3>Unemployment coverage</h3>'+missing.to_html()+'</section><section id="methods"><h2>Methods and limitations</h2><p>'+methods+'</p><p>'+limitations+'</p></section></html>'
 (o/'docs/index.html').write_text(html,encoding='utf-8')
 print(results)
if __name__=='__main__':main()
