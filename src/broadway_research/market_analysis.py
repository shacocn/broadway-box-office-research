import statsmodels.formula.api as smf

def models(m):
    base='log_market_gross ~ holiday_week + C(month) + C(year)'
    formulas={'A':base,'B':base+' + unemployment_rate_pct + consumer_sentiment_monthly','C':base+' + unemployment_rate_pct + consumer_sentiment_monthly + nyc_visitors_millions_annual','D':base+' + unemployment_rate_pct + consumer_sentiment_halfyear'}
    return {k:(v,smf.ols(v,m.sort_values('week_ending')).fit(cov_type='HAC',cov_kwds={'maxlags':8})) for k,v in formulas.items()}
