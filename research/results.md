# Results

Production N=67; R-squared 0.6079569056109901; adjusted R-squared 0.42500346156278557. Capacity elasticity 1.0073848481499077, 95% CI [0.529649100084592, 1.4851205962152234], HC3 p=3.582017220037491e-05. A 1% capacity difference is associated with approximately 1.01% gross difference conditional on controls.

| metric     |   benchmark |    computed |   difference | passed   |
|:-----------|------------:|------------:|-------------:|:---------|
| r_squared  | 0.607957    | 0.607957    | -6.66134e-16 | True     |
| capacity   | 1.00738     | 1.00738     | -1.77636e-15 | True     |
| capacity_p | 3.58202e-05 | 3.58202e-05 | -2.41913e-18 | True     |
| adapted    | 0.286721    | 0.286721    | -1.40234e-11 | True     |

| sample            |   n |   r_squared |   adjusted_r_squared |   capacity |    lower |   upper |           p |
|:------------------|----:|------------:|---------------------:|-----------:|---------:|--------:|------------:|
| Full sample       |  67 |    0.607957 |             0.425003 |   1.00738  | 0.529649 | 1.48512 | 3.58202e-05 |
| Without Hamilton  |  66 |    0.568097 |             0.37614  |   1.00738  | 0.529649 | 1.48512 | 3.58202e-05 |
| Without top 5%    |  63 |    0.531122 |             0.307847 |   0.923827 | 0.454106 | 1.39355 | 0.000115837 |
| At least 20 weeks |  51 |    0.692047 |             0.469047 |   0.796268 | 0.296038 | 1.2965  | 0.00180928  |

| model   | status                                        |   n |   r_squared |   paper_n |   paper_r_squared |   rank |   columns |   condition_number |   max_leverage |
|:--------|:----------------------------------------------|----:|------------:|----------:|------------------:|-------:|----------:|-------------------:|---------------:|
| A       | Exploratory extension; not exact reproduction | 501 |    0.506952 |       501 |             0.507 |     24 |        24 |       17.1188      |       0.123078 |
| B       | Exploratory extension; not exact reproduction | 257 |    0.698749 |       257 |             0.699 |     21 |        26 |        6.40844e+18 |       0.196494 |
| C       | Exploratory extension; not exact reproduction | 236 |    0.698932 |       236 |             0.671 |     20 |        27 |        2.51462e+35 |       0.202344 |
| D       | Exploratory extension; not exact reproduction | 257 |    0.696198 |       257 |             0.696 |     21 |        26 |        5.19773e+18 |       0.192184 |