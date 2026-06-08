# RESEARCH-015: COT Edge Validation & Reality Check

Data: 1556 weeks (2006-06-13 to 2026-06-02)
Total signals enumerated: 440

## Test 1: Edge Selection

Filter: p<0.05, Sharpe>1.0, PF>1.30, N>100

Candidates: 90

| Rank | Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |
|------|--------|---|-----------|--------|----|-----|-------|
| 1 | T3|Bullish Div 8w | 225 | 4.635% | 1.79 | 6.72 | 76.0% | 0.0000 |
| 2 | T5|Managed_Money Sideways 4w Q1_Low | 257 | 2.099% | 1.78 | 3.88 | 69.6% | 0.0000 |
| 3 | T5|Managed_Money Sideways 8w Q1_Low | 256 | 4.382% | 1.75 | 6.41 | 72.3% | 0.0000 |
| 4 | T5|Commercial Sideways 1w Q1_Low | 258 | 0.496% | 1.74 | 1.87 | 62.8% | 0.0001 |
| 5 | T5|Managed_Money Sideways 1w Q1_Low | 258 | 0.522% | 1.67 | 1.89 | 57.8% | 0.0002 |
| 6 | T1|Managed_Money 8w Q1_Low | 309 | 4.139% | 1.67 | 5.70 | 72.2% | 0.0000 |
| 7 | T1|Managed_Money 4w Q1_Low | 310 | 2.036% | 1.64 | 3.44 | 69.4% | 0.0000 |
| 8 | T1|Large_Spec 4w Q2 | 310 | 2.012% | 1.61 | 3.06 | 62.3% | 0.0000 |
| 9 | T3|Bullish Div 4w | 229 | 2.055% | 1.61 | 3.49 | 69.9% | 0.0000 |
| 10 | T4|Commercial Extreme_Long 8w | 149 | 4.335% | 1.56 | 5.25 | 71.8% | 0.0000 |
| 11 | T5|Large_Spec Sideways 2w Q2 | 257 | 0.963% | 1.56 | 2.19 | 59.9% | 0.0000 |
| 12 | T5|Managed_Money Sideways 2w Q1_Low | 258 | 0.990% | 1.54 | 2.32 | 65.5% | 0.0000 |
| 13 | T4|Managed_Money Extreme_Short 8w | 148 | 3.925% | 1.54 | 4.75 | 73.0% | 0.0000 |
| 14 | T5|Large_Spec Sideways 4w Q2 | 257 | 1.936% | 1.53 | 2.94 | 59.9% | 0.0000 |
| 15 | T1|Large_Spec 2w Q2 | 311 | 0.965% | 1.52 | 2.11 | 60.8% | 0.0000 |
| 16 | T1|Managed_Money 2w Q1_Low | 311 | 1.000% | 1.52 | 2.26 | 63.3% | 0.0000 |
| 17 | T4|Managed_Money Extreme_Long 1w | 156 | 0.498% | 1.52 | 1.78 | 62.8% | 0.0094 |
| 18 | T1|Managed_Money 1w Q1_Low | 312 | 0.521% | 1.52 | 1.77 | 57.4% | 0.0002 |
| 19 | T4|Commercial Extreme_Long 4w | 153 | 2.087% | 1.51 | 3.25 | 67.3% | 0.0000 |
| 20 | T1|Commercial 8w Q5_High | 309 | 3.690% | 1.46 | 4.72 | 69.3% | 0.0000 |
| 21 | T5|Commercial Sideways 8w Q5_High | 255 | 3.678% | 1.45 | 4.65 | 67.8% | 0.0000 |
| 22 | T4|Commercial Extreme_Long 1w | 156 | 0.576% | 1.45 | 1.73 | 60.3% | 0.0130 |
| 23 | T5|Managed_Money Sideways 1w Q5_High | 258 | 0.410% | 1.45 | 1.66 | 63.2% | 0.0014 |
| 24 | T5|Commercial Sideways 1w Q5_High | 258 | 0.448% | 1.42 | 1.73 | 56.6% | 0.0017 |
| 25 | T5|Commercial Sideways 2w Q1_Low | 258 | 0.829% | 1.42 | 2.06 | 58.9% | 0.0000 |
| 26 | T2|DManaged_Money 1w Q5_High | 311 | 0.473% | 1.41 | 1.70 | 59.2% | 0.0006 |
| 27 | T4|Large_Spec Extreme_Short 8w | 148 | 4.730% | 1.40 | 4.31 | 68.9% | 0.0000 |
| 28 | T3|Bullish Div 1w | 232 | 0.492% | 1.38 | 1.70 | 56.9% | 0.0040 |
| 29 | T3|Bullish Div 2w | 231 | 0.922% | 1.37 | 2.10 | 64.1% | 0.0001 |
| 30 | T5|Large_Spec Sideways 1w Q2 | 258 | 0.402% | 1.36 | 1.62 | 63.2% | 0.0028 |
| 31 | T1|Commercial 1w Q5_High | 311 | 0.476% | 1.35 | 1.69 | 56.6% | 0.0011 |
| 32 | T1|Commercial 2w Q5_High | 311 | 0.928% | 1.35 | 2.04 | 65.3% | 0.0000 |
| 33 | T4|Large_Spec Extreme_Short 4w | 152 | 2.014% | 1.33 | 2.69 | 68.4% | 0.0000 |
| 34 | T5|Commercial Sideways 4w Q5_High | 257 | 1.691% | 1.33 | 2.71 | 66.1% | 0.0000 |
| 35 | T4|Managed_Money Extreme_Short 4w | 152 | 1.618% | 1.31 | 2.84 | 68.4% | 0.0000 |
| 36 | T4|Managed_Money Extreme_Long 4w | 156 | 1.635% | 1.31 | 2.64 | 62.2% | 0.0000 |
| 37 | T1|Commercial 4w Q5_High | 310 | 1.714% | 1.31 | 2.65 | 67.4% | 0.0000 |
| 38 | T1|Commercial 2w Q1_Low | 311 | 0.793% | 1.30 | 1.94 | 58.2% | 0.0000 |
| 39 | T3|Bearish Div 4w | 188 | 1.554% | 1.29 | 2.61 | 62.8% | 0.0000 |
| 40 | T4|Commercial Extreme_Long 2w | 155 | 0.937% | 1.29 | 2.02 | 63.2% | 0.0020 |
| 41 | T2|DCommercial 1w Q1_Low | 311 | 0.428% | 1.28 | 1.62 | 59.2% | 0.0019 |
| 42 | T1|Large_Spec 8w Q2 | 308 | 2.930% | 1.27 | 3.54 | 65.3% | 0.0000 |
| 43 | T4|Managed_Money Extreme_Long 2w | 156 | 0.729% | 1.26 | 1.89 | 59.0% | 0.0024 |
| 44 | T4|Small_Spec Extreme_Short 4w | 155 | 1.571% | 1.26 | 2.45 | 66.5% | 0.0000 |
| 45 | T1|Large_Spec 1w Q2 | 311 | 0.394% | 1.26 | 1.57 | 62.1% | 0.0023 |
| 46 | T3|Bearish Div 2w | 188 | 0.718% | 1.26 | 1.89 | 58.0% | 0.0009 |
| 47 | T1|Commercial 1w Q1_Low | 312 | 0.398% | 1.25 | 1.58 | 60.6% | 0.0024 |
| 48 | T2|DLarge_Spec 1w Q2 | 311 | 0.379% | 1.25 | 1.58 | 57.6% | 0.0024 |
| 49 | T1|Small_Spec 1w Q1_Low | 312 | 0.399% | 1.25 | 1.60 | 52.9% | 0.0024 |
| 50 | T5|Large_Spec Sideways 1w Q5_High | 258 | 0.332% | 1.23 | 1.57 | 55.8% | 0.0068 |
| 51 | T5|Large_Spec Sideways 8w Q2 | 255 | 2.610% | 1.22 | 3.29 | 62.4% | 0.0000 |
| 52 | T2|DManaged_Money 2w Q5_High | 311 | 0.741% | 1.22 | 1.83 | 60.8% | 0.0000 |
| 53 | T5|Managed_Money Sideways 8w Q5_High | 255 | 2.870% | 1.22 | 3.60 | 64.3% | 0.0000 |
| 54 | T1|Small_Spec 4w Q4 | 310 | 1.442% | 1.21 | 2.38 | 64.5% | 0.0000 |
| 55 | T5|Commercial Sideways 2w Q5_High | 258 | 0.803% | 1.20 | 1.90 | 65.5% | 0.0002 |
| 56 | T2|DManaged_Money 8w Q5_High | 308 | 3.139% | 1.20 | 3.41 | 67.5% | 0.0000 |
| 57 | T4|Large_Spec Extreme_Long 1w | 156 | 0.386% | 1.20 | 1.56 | 56.4% | 0.0399 |
| 58 | T2|DCommercial 2w Q1_Low | 311 | 0.722% | 1.17 | 1.80 | 61.1% | 0.0001 |
| 59 | T3|Bearish Div 1w | 188 | 0.354% | 1.16 | 1.54 | 63.3% | 0.0283 |
| 60 | T1|Commercial 4w Q1_Low | 310 | 1.510% | 1.16 | 2.35 | 60.3% | 0.0000 |
| 61 | T4|Large_Spec Extreme_Short 1w | 155 | 0.520% | 1.16 | 1.54 | 56.8% | 0.0478 |
| 62 | T2|DSmall_Spec 1w Q1_Low | 311 | 0.404% | 1.15 | 1.53 | 56.6% | 0.0054 |
| 63 | T4|Small_Spec Extreme_Short 8w | 155 | 2.695% | 1.14 | 3.22 | 71.0% | 0.0000 |
| 64 | T5|Small_Spec Sideways 1w Q5_High | 258 | 0.400% | 1.13 | 1.51 | 61.2% | 0.0123 |
| 65 | T5|Managed_Money Sideways 4w Q5_High | 257 | 1.319% | 1.12 | 2.31 | 63.0% | 0.0000 |
| 66 | T3|Bearish Div 8w | 188 | 2.405% | 1.10 | 2.98 | 59.0% | 0.0000 |
| 67 | T1|Commercial 8w Q1_Low | 309 | 2.660% | 1.09 | 3.01 | 58.6% | 0.0000 |
| 68 | T5|Commercial Sideways 4w Q1_Low | 257 | 1.370% | 1.09 | 2.22 | 59.1% | 0.0000 |
| 69 | T4|Managed_Money Extreme_Short 2w | 154 | 0.719% | 1.08 | 1.82 | 59.7% | 0.0092 |
| 70 | T4|Large_Spec Extreme_Short 2w | 154 | 0.872% | 1.08 | 1.77 | 64.9% | 0.0096 |
| 71 | T5|Small_Spec Sideways 4w Q4 | 257 | 1.287% | 1.07 | 2.16 | 63.4% | 0.0000 |
| 72 | T5|Managed_Money Sideways 2w Q5_High | 258 | 0.621% | 1.07 | 1.72 | 57.4% | 0.0008 |
| 73 | T5|Commercial Sideways 8w Q1_Low | 256 | 2.561% | 1.07 | 2.94 | 58.2% | 0.0000 |
| 74 | T2|DLarge_Spec 4w Q1_Low | 310 | 1.419% | 1.06 | 2.18 | 61.0% | 0.0000 |
| 75 | T2|DCommercial 1w Q2 | 311 | 0.387% | 1.06 | 1.52 | 58.5% | 0.0102 |
| 76 | T5|Commercial Sideways 8w Q2 | 255 | 2.741% | 1.06 | 3.16 | 60.4% | 0.0000 |
| 77 | T5|Large_Spec Sideways 8w Q5_High | 255 | 2.693% | 1.05 | 2.89 | 59.6% | 0.0000 |
| 78 | T2|DLarge_Spec 1w Q5_High | 311 | 0.408% | 1.05 | 1.50 | 55.9% | 0.0110 |
| 79 | T2|DCommercial 8w Q1_Low | 309 | 2.822% | 1.05 | 2.90 | 65.4% | 0.0000 |
| 80 | T1|Small_Spec 8w Q4 | 308 | 2.553% | 1.04 | 2.91 | 59.7% | 0.0000 |
| 81 | T2|DSmall_Spec 4w Q1_Low | 310 | 1.361% | 1.04 | 2.21 | 61.0% | 0.0000 |
| 82 | T2|DLarge_Spec 8w Q5_High | 308 | 2.626% | 1.04 | 2.97 | 61.0% | 0.0000 |
| 83 | T1|Large_Spec 1w Q5_High | 311 | 0.339% | 1.04 | 1.49 | 56.3% | 0.0115 |
| 84 | T1|Large_Spec 8w Q5_High | 309 | 2.630% | 1.03 | 2.84 | 60.2% | 0.0000 |
| 85 | T2|DManaged_Money 4w Q5_High | 310 | 1.352% | 1.03 | 2.09 | 61.9% | 0.0000 |
| 86 | T1|Small_Spec 1w Q4 | 311 | 0.360% | 1.03 | 1.46 | 55.9% | 0.0122 |
| 87 | T1|Managed_Money 8w Q5_High | 309 | 2.524% | 1.02 | 2.87 | 62.1% | 0.0000 |
| 88 | T2|DSmall_Spec 8w Q1_Low | 309 | 2.646% | 1.01 | 2.92 | 62.8% | 0.0000 |
| 89 | T2|DLarge_Spec 8w Q1_Low | 309 | 2.753% | 1.01 | 2.86 | 63.1% | 0.0000 |
| 90 | T2|DLarge_Spec 4w Q5_High | 310 | 1.357% | 1.00 | 2.15 | 60.3% | 0.0000 |

## Test 2: Walk-Forward Validation

Pass: 9 / 90

| Signal | 2006-2011 | 2012-2016 | 2017-2021 | 2022-2026 | Stability | PASS |
|--------|-----------|-----------|-----------|-----------|-----------|------|
| T3|Bullish Div 8w                             | 0.00%/0.00      | 5.83%/2.54      | 1.61%/1.31      | 4.71%/1.65      | 0.75 | False |
| T5|Managed_Money Sideways 4w Q1_Low           | 6.11%/11.35     | 2.07%/1.78      | 0.77%/0.96      | 2.45%/1.90      | 1.00 | True |
| T5|Managed_Money Sideways 8w Q1_Low           | 4.83%/5.21      | 4.60%/2.04      | 1.97%/1.11      | 5.07%/1.79      | 1.00 | True |
| T5|Commercial Sideways 1w Q1_Low              | 0.84%/2.91      | -0.38%/-1.73    | 0.39%/1.44      | 0.84%/2.61      | 0.75 | False |
| T5|Managed_Money Sideways 1w Q1_Low           | 1.73%/3.81      | 0.54%/2.01      | 0.21%/1.00      | 0.58%/1.62      | 1.00 | True |
| T1|Managed_Money 8w Q1_Low                    | 6.05%/4.21      | 4.81%/2.17      | 1.84%/1.02      | 4.52%/1.63      | 1.00 | True |
| T1|Managed_Money 4w Q1_Low                    | 6.58%/11.41     | 2.10%/1.84      | 0.73%/0.90      | 2.22%/1.61      | 1.00 | True |
| T1|Large_Spec 4w Q2                           | 2.48%/1.82      | 1.49%/1.37      | 0.22%/0.32      | 0.00%/0.00      | 0.75 | False |
| T3|Bullish Div 4w                             | 0.00%/0.00      | 2.41%/2.17      | 0.48%/0.74      | 2.21%/1.55      | 0.75 | False |
| T4|Commercial Extreme_Long 8w                 | 0.00%/0.00      | 0.00%/0.00      | 1.09%/0.86      | 4.70%/1.64      | 0.50 | False |
| T5|Large_Spec Sideways 2w Q2                  | 1.24%/1.92      | 0.70%/1.15      | -0.09%/-0.24    | 0.00%/0.00      | 0.50 | False |
| T5|Managed_Money Sideways 2w Q1_Low           | 4.06%/6.74      | 1.18%/2.09      | 0.30%/0.78      | 1.02%/1.37      | 1.00 | True |
| T4|Managed_Money Extreme_Short 8w             | 0.00%/0.00      | 6.88%/2.90      | 1.50%/1.00      | 3.85%/1.38      | 0.75 | False |
| T5|Large_Spec Sideways 4w Q2                  | 2.57%/1.85      | 1.32%/1.22      | 0.10%/0.14      | 0.00%/0.00      | 0.75 | False |
| T1|Large_Spec 2w Q2                           | 1.16%/1.75      | 0.76%/1.25      | 0.19%/0.47      | 0.00%/0.00      | 0.75 | False |
| T1|Managed_Money 2w Q1_Low                    | 3.44%/5.59      | 1.11%/1.86      | 0.36%/0.92      | 1.05%/1.41      | 1.00 | True |
| T4|Managed_Money Extreme_Long 1w              | 1.06%/3.23      | -0.28%/-1.24    | -0.11%/-0.27    | 1.35%/6.10      | 0.50 | False |
| T1|Managed_Money 1w Q1_Low                    | 2.14%/4.97      | 0.48%/1.74      | 0.35%/1.52      | 0.54%/1.35      | 1.00 | True |
| T4|Commercial Extreme_Long 4w                 | 0.00%/0.00      | 0.00%/0.00      | 0.85%/1.15      | 2.22%/1.55      | 0.50 | False |
| T1|Commercial 8w Q5_High                      | 0.00%/0.00      | 2.87%/1.31      | 1.94%/1.37      | 4.71%/1.65      | 0.75 | False |
| T5|Commercial Sideways 8w Q5_High             | 0.00%/0.00      | 2.51%/1.10      | 2.21%/1.60      | 5.41%/1.87      | 0.75 | False |
| T4|Commercial Extreme_Long 1w                 | 0.00%/0.00      | 0.00%/0.00      | 0.72%/2.42      | 0.56%/1.38      | 0.50 | False |
| T5|Managed_Money Sideways 1w Q5_High          | 0.64%/2.21      | -0.37%/-1.23    | 0.44%/1.98      | 0.72%/2.66      | 0.75 | False |
| T5|Commercial Sideways 1w Q5_High             | 0.00%/0.00      | 0.31%/1.09      | 0.18%/0.82      | 0.66%/1.83      | 0.75 | False |
| T5|Commercial Sideways 2w Q1_Low              | 1.81%/3.08      | -0.78%/-1.73    | 0.45%/0.77      | 1.20%/2.17      | 0.75 | False |
| T2|DManaged_Money 1w Q5_High                  | 0.69%/2.03      | 0.08%/0.27      | 0.49%/2.11      | 0.55%/1.40      | 1.00 | False |
| T4|Large_Spec Extreme_Short 8w                | 4.17%/1.01      | 6.07%/2.42      | -1.73%/-2.21    | 5.23%/1.64      | 0.75 | False |
| T3|Bullish Div 1w                             | 0.00%/0.00      | 0.38%/1.45      | 0.25%/1.02      | 0.59%/1.44      | 0.75 | False |
| T3|Bullish Div 2w                             | 0.00%/0.00      | 1.11%/1.90      | 0.08%/0.21      | 1.01%/1.34      | 0.75 | False |
| T5|Large_Spec Sideways 1w Q2                  | 0.40%/1.23      | 0.46%/1.77      | 0.05%/0.28      | 0.00%/0.00      | 0.75 | False |
| T1|Commercial 1w Q5_High                      | 0.00%/0.00      | 0.31%/1.10      | 0.34%/1.40      | 0.59%/1.44      | 0.75 | False |
| T1|Commercial 2w Q5_High                      | 0.00%/0.00      | 0.84%/1.31      | 0.26%/0.67      | 1.01%/1.34      | 0.75 | False |
| T4|Large_Spec Extreme_Short 4w                | 1.01%/0.59      | 4.55%/9.47      | -1.55%/-3.59    | 2.36%/1.58      | 0.75 | False |
| T5|Commercial Sideways 4w Q5_High             | 0.00%/0.00      | 1.13%/0.87      | 0.55%/0.86      | 2.57%/1.96      | 0.75 | False |
| T4|Managed_Money Extreme_Short 4w             | 0.00%/0.00      | 2.89%/2.55      | 0.27%/0.41      | 1.71%/1.22      | 0.75 | False |
| T4|Managed_Money Extreme_Long 4w              | 3.56%/2.61      | -0.98%/-1.28    | -0.04%/-0.05    | 2.76%/2.73      | 0.50 | False |
| T1|Commercial 4w Q5_High                      | 0.00%/0.00      | 1.32%/1.05      | 0.59%/0.87      | 2.21%/1.55      | 0.75 | False |
| T1|Commercial 2w Q1_Low                       | 1.46%/2.39      | -0.80%/-1.81    | 0.35%/0.58      | 1.61%/2.55      | 0.75 | False |
| T3|Bearish Div 4w                             | 2.59%/1.92      | -0.98%/-1.28    | 1.13%/1.17      | 2.77%/2.40      | 0.75 | False |
| T4|Commercial Extreme_Long 2w                 | 0.00%/0.00      | 0.00%/0.00      | 0.34%/0.76      | 1.00%/1.33      | 0.50 | False |
| T2|DCommercial 1w Q1_Low                      | 0.33%/1.05      | 0.17%/0.61      | 0.50%/2.14      | 0.55%/1.37      | 1.00 | False |
| T1|Large_Spec 8w Q2                           | 4.46%/1.87      | 0.50%/0.25      | 1.32%/1.13      | 0.00%/0.00      | 0.75 | False |
| T4|Managed_Money Extreme_Long 2w              | 1.75%/2.94      | -0.61%/-1.32    | -0.44%/-0.90    | 2.13%/4.86      | 0.50 | False |
| T4|Small_Spec Extreme_Short 4w                | 0.00%/0.00      | 1.11%/0.88      | 0.00%/0.00      | 2.29%/1.89      | 0.50 | False |
| T1|Large_Spec 1w Q2                           | 0.39%/1.11      | 0.43%/1.63      | 0.23%/1.23      | 0.00%/0.00      | 0.75 | False |
| T3|Bearish Div 2w                             | 1.44%/2.33      | -0.61%/-1.32    | 0.42%/0.83      | 0.96%/1.74      | 0.75 | False |
| T1|Commercial 1w Q1_Low                       | 0.68%/2.30      | -0.39%/-1.79    | 0.22%/0.62      | 0.76%/2.30      | 0.75 | False |
| T2|DLarge_Spec 1w Q2                          | 0.42%/1.16      | 0.12%/0.48      | 0.43%/1.73      | 0.70%/2.53      | 1.00 | False |
| T1|Small_Spec 1w Q1_Low                       | 3.58%/4.05      | 0.18%/0.62      | 0.61%/1.57      | 0.77%/2.33      | 1.00 | False |
| T5|Large_Spec Sideways 1w Q5_High             | 0.00%/0.00      | -0.76%/-4.87    | 0.17%/0.63      | 0.48%/1.74      | 0.50 | False |
| T5|Large_Spec Sideways 8w Q2                  | 4.51%/2.17      | 0.03%/0.02      | 1.33%/0.96      | 0.00%/0.00      | 0.75 | False |
| T2|DManaged_Money 2w Q5_High                  | 1.02%/1.55      | -0.06%/-0.10    | 0.58%/1.35      | 1.04%/1.57      | 0.75 | False |
| T5|Managed_Money Sideways 8w Q5_High          | 4.20%/1.77      | -1.41%/-0.70    | 2.15%/1.30      | 6.25%/2.65      | 0.75 | False |
| T1|Small_Spec 4w Q4                           | 1.60%/1.29      | 0.53%/0.46      | 1.36%/1.32      | 1.97%/1.49      | 1.00 | False |
| T5|Commercial Sideways 2w Q5_High             | 0.00%/0.00      | 0.72%/1.13      | 0.12%/0.31      | 1.09%/1.44      | 0.75 | False |
| T2|DManaged_Money 8w Q5_High                  | 5.42%/1.87      | -0.74%/-0.31    | 2.29%/1.16      | 4.50%/1.70      | 0.75 | False |
| T4|Large_Spec Extreme_Long 1w                 | 0.00%/0.00      | 0.00%/0.00      | 0.34%/1.10      | 0.46%/1.34      | 0.50 | False |
| T2|DCommercial 2w Q1_Low                      | 0.62%/0.94      | 0.07%/0.12      | 0.69%/1.66      | 1.05%/1.53      | 1.00 | False |
| T3|Bearish Div 1w                             | 0.70%/2.24      | -0.28%/-1.24    | 0.12%/0.33      | 0.60%/2.27      | 0.75 | False |
| T1|Commercial 4w Q1_Low                       | 2.46%/1.82      | -1.51%/-1.94    | 0.79%/0.64      | 3.24%/2.47      | 0.75 | False |
| T4|Large_Spec Extreme_Short 1w                | 0.27%/0.52      | 0.80%/2.08      | -0.31%/-1.01    | 0.63%/1.46      | 0.75 | False |
| T2|DSmall_Spec 1w Q1_Low                      | 0.09%/0.24      | -0.16%/-0.57    | 0.63%/1.92      | 0.70%/1.86      | 0.75 | False |
| T4|Small_Spec Extreme_Short 8w                | 0.00%/0.00      | 2.05%/0.78      | 0.00%/0.00      | 3.83%/2.13      | 0.50 | False |
| T5|Small_Spec Sideways 1w Q5_High             | 0.61%/1.81      | -0.10%/-0.42    | -0.31%/-1.10    | 0.98%/1.23      | 0.50 | False |
| T5|Managed_Money Sideways 4w Q5_High          | 2.03%/1.64      | -0.90%/-0.92    | 0.76%/0.91      | 3.17%/2.66      | 0.75 | False |
| T3|Bearish Div 8w                             | 3.19%/1.47      | -1.57%/-0.89    | 2.76%/1.49      | 5.31%/2.50      | 0.75 | False |
| T1|Commercial 8w Q1_Low                       | 3.03%/1.47      | -1.75%/-1.09    | 1.52%/0.68      | 6.48%/2.45      | 0.75 | False |
| T5|Commercial Sideways 4w Q1_Low              | 2.28%/1.69      | -1.46%/-1.90    | 0.83%/0.72      | 2.92%/2.33      | 0.75 | False |
| T4|Managed_Money Extreme_Short 2w             | 0.00%/0.00      | 0.70%/1.59      | 0.10%/0.29      | 0.96%/1.20      | 0.75 | False |
| T4|Large_Spec Extreme_Short 2w                | 0.10%/0.13      | 2.37%/3.26      | -1.51%/-3.77    | 1.16%/1.40      | 0.75 | False |
| T5|Small_Spec Sideways 4w Q4                  | 1.76%/1.39      | -0.10%/-0.09    | 1.52%/1.45      | 1.66%/1.34      | 0.75 | False |
| T5|Managed_Money Sideways 2w Q5_High          | 1.04%/1.74      | -0.54%/-0.95    | 0.38%/0.80      | 1.24%/2.11      | 0.75 | False |
| T5|Commercial Sideways 8w Q1_Low              | 2.69%/1.44      | -1.83%/-1.12    | 1.84%/0.83      | 6.48%/2.36      | 0.75 | False |
| T2|DLarge_Spec 4w Q1_Low                      | 1.69%/1.10      | -0.45%/-0.36    | 0.72%/0.78      | 2.19%/1.54      | 0.75 | False |
| T2|DCommercial 1w Q2                          | 0.64%/1.42      | 0.13%/0.37      | 0.07%/0.27      | 0.54%/2.50      | 1.00 | False |
| T5|Commercial Sideways 8w Q2                  | 5.84%/2.28      | -1.91%/-0.92    | 0.95%/0.57      | 2.97%/1.06      | 0.75 | False |
| T5|Large_Spec Sideways 8w Q5_High             | 0.00%/0.00      | -13.38%/-106.71 | 1.59%/0.75      | 4.05%/1.52      | 0.50 | False |
| T2|DLarge_Spec 1w Q5_High                     | 0.78%/1.44      | -0.23%/-0.92    | 0.22%/0.81      | 0.58%/1.38      | 0.75 | False |
| T2|DCommercial 8w Q1_Low                      | 3.76%/1.19      | -1.40%/-0.60    | 2.91%/1.53      | 4.39%/1.62      | 0.75 | False |
| T1|Small_Spec 8w Q4                           | 2.74%/1.24      | 0.14%/0.06      | 2.61%/1.30      | 4.34%/1.32      | 1.00 | False |
| T2|DSmall_Spec 4w Q1_Low                      | 1.14%/0.81      | -0.87%/-0.86    | 1.65%/1.51      | 2.33%/1.72      | 0.75 | False |
| T2|DLarge_Spec 8w Q5_High                     | 4.27%/1.95      | -1.77%/-0.76    | 0.90%/0.49      | 4.36%/1.61      | 0.75 | False |
| T1|Large_Spec 1w Q5_High                      | 0.00%/0.00      | -0.76%/-4.87    | 0.15%/0.43      | 0.50%/1.55      | 0.50 | False |
| T1|Large_Spec 8w Q5_High                      | 0.00%/0.00      | -13.38%/-106.71 | 1.32%/0.61      | 4.04%/1.54      | 0.50 | False |
| T2|DManaged_Money 4w Q5_High                  | 2.69%/2.03      | -0.65%/-0.47    | 0.74%/0.85      | 2.03%/1.45      | 0.75 | False |
| T1|Small_Spec 1w Q4                           | 0.32%/0.81      | 0.21%/0.89      | 0.48%/1.77      | 0.42%/0.98      | 1.00 | True |
| T1|Managed_Money 8w Q5_High                   | 3.34%/1.22      | -1.27%/-0.63    | 1.96%/1.18      | 5.31%/2.50      | 0.75 | False |
| T2|DSmall_Spec 8w Q1_Low                      | 4.03%/1.58      | -1.47%/-0.70    | 1.77%/1.03      | 4.36%/1.58      | 0.75 | False |
| T2|DLarge_Spec 8w Q1_Low                      | 3.24%/1.20      | -1.28%/-0.48    | 1.43%/0.79      | 4.49%/1.53      | 0.75 | False |
| T2|DLarge_Spec 4w Q5_High                     | 2.06%/1.22      | -0.87%/-0.84    | 0.72%/0.68      | 2.12%/1.51      | 0.75 | False |

## Test 3: Out-of-Sample Validation

Train: 2006-2020, Test: 2021-2026
Pass: 24 / 90

| Signal | Train_Ret% | Train_SR | Train_PF | Test_Ret% | Test_SR | Test_PF | Deg_SR | Deg_PF | Deg_WR | PASS |
|--------|------------|----------|----------|-----------|---------|---------|--------|--------|--------|------|
| T3|Bullish Div 8w                             | 4.886% | 2.29 | 13.11 | 4.482% | 1.58 | 5.24 | 31.2% | 60.0% | 14.5% | False |
| T5|Managed_Money Sideways 4w Q1_Low           | 1.845% | 1.73 | 3.72 | 2.335% | 1.82 | 3.97 | 5.2% | 6.7% | 6.6% | True |
| T5|Managed_Money Sideways 8w Q1_Low           | 3.799% | 1.80 | 6.65 | 4.853% | 1.73 | 6.01 | 3.9% | 9.5% | 2.7% | True |
| T5|Commercial Sideways 1w Q1_Low              | 0.438% | 1.60 | 1.76 | 0.652% | 2.07 | 2.18 | 29.4% | 23.6% | 3.0% | True |
| T5|Managed_Money Sideways 1w Q1_Low           | 0.513% | 1.99 | 2.11 | 0.529% | 1.49 | 1.76 | 24.9% | 16.9% | 5.2% | True |
| T1|Managed_Money 8w Q1_Low                    | 4.003% | 1.89 | 7.34 | 4.347% | 1.58 | 5.02 | 16.5% | 31.6% | 5.3% | False |
| T1|Managed_Money 4w Q1_Low                    | 1.923% | 1.79 | 3.73 | 2.113% | 1.55 | 3.24 | 13.7% | 13.0% | 3.4% | True |
| T1|Large_Spec 4w Q2                           | 1.996% | 1.60 | 3.03 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T3|Bullish Div 4w                             | 2.003% | 1.96 | 4.48 | 2.085% | 1.47 | 3.14 | 24.9% | 29.9% | 9.1% | True |
| T4|Commercial Extreme_Long 8w                 | 2.512% | 2.21 | 7.26 | 4.466% | 1.57 | 5.20 | 29.2% | 28.4% | 11.0% | True |
| T5|Large_Spec Sideways 2w Q2                  | 0.946% | 1.53 | 2.16 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T5|Managed_Money Sideways 2w Q1_Low           | 1.058% | 2.03 | 2.95 | 0.936% | 1.27 | 2.00 | 37.5% | 32.1% | 6.7% | False |
| T4|Managed_Money Extreme_Short 8w             | 4.389% | 1.99 | 9.19 | 3.608% | 1.30 | 3.59 | 34.6% | 61.0% | 14.8% | False |
| T5|Large_Spec Sideways 4w Q2                  | 1.932% | 1.53 | 2.95 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T1|Large_Spec 2w Q2                           | 0.965% | 1.52 | 2.11 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T1|Managed_Money 2w Q1_Low                    | 1.005% | 1.84 | 2.69 | 0.995% | 1.35 | 2.05 | 26.7% | 23.5% | 1.7% | True |
| T4|Managed_Money Extreme_Long 1w              | 0.446% | 1.34 | 1.67 | 1.347% | 6.10 | 12.69 | 355.3% | 661.3% | 6.5% | False |
| T1|Managed_Money 1w Q1_Low                    | 0.539% | 1.99 | 2.09 | 0.508% | 1.30 | 1.62 | 34.8% | 22.4% | 4.7% | False |
| T4|Commercial Extreme_Long 4w                 | 2.002% | 3.14 | 11.97 | 2.092% | 1.48 | 3.14 | 53.0% | 73.8% | 4.1% | False |
| T1|Commercial 8w Q5_High                      | 2.976% | 1.40 | 4.36 | 4.482% | 1.58 | 5.24 | 13.0% | 20.3% | 5.5% | True |
| T5|Commercial Sideways 8w Q5_High             | 2.561% | 1.19 | 3.38 | 5.162% | 1.79 | 6.81 | 50.0% | 101.4% | 9.6% | False |
| T4|Commercial Extreme_Long 1w                 | 1.508% | 5.54 | 10.08 | 0.512% | 1.27 | 1.62 | 77.1% | 83.9% | 14.9% | False |
| T5|Managed_Money Sideways 1w Q5_High          | 0.374% | 1.31 | 1.58 | 0.718% | 2.66 | 2.65 | 102.2% | 67.5% | 6.2% | False |
| T5|Commercial Sideways 1w Q5_High             | 0.330% | 1.21 | 1.58 | 0.595% | 1.65 | 1.88 | 37.0% | 18.8% | 14.5% | False |
| T5|Commercial Sideways 2w Q1_Low              | 0.824% | 1.40 | 2.05 | 0.842% | 1.48 | 2.07 | 5.8% | 0.8% | 16.5% | True |
| T2|DManaged_Money 1w Q5_High                  | 0.442% | 1.53 | 1.74 | 0.506% | 1.33 | 1.66 | 13.3% | 4.5% | 1.0% | True |
| T4|Large_Spec Extreme_Short 8w                | 4.308% | 1.14 | 3.45 | 4.946% | 1.56 | 4.93 | 37.3% | 42.9% | 16.9% | False |
| T3|Bullish Div 1w                             | 0.414% | 1.61 | 1.83 | 0.537% | 1.33 | 1.65 | 17.3% | 9.8% | 15.6% | True |
| T3|Bullish Div 2w                             | 0.891% | 1.68 | 2.40 | 0.941% | 1.26 | 1.99 | 24.9% | 17.1% | 4.4% | True |
| T5|Large_Spec Sideways 1w Q2                  | 0.402% | 1.36 | 1.62 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T1|Commercial 1w Q5_High                      | 0.421% | 1.41 | 1.74 | 0.537% | 1.33 | 1.65 | 5.5% | 5.1% | 11.6% | True |
| T1|Commercial 2w Q5_High                      | 0.869% | 1.39 | 2.03 | 0.941% | 1.26 | 1.99 | 9.2% | 2.4% | 6.1% | True |
| T4|Large_Spec Extreme_Short 4w                | 1.643% | 1.05 | 2.00 | 2.196% | 1.48 | 3.26 | 40.6% | 63.2% | 7.4% | False |
| T5|Commercial Sideways 4w Q5_High             | 1.097% | 0.90 | 1.93 | 2.413% | 1.84 | 4.26 | 103.8% | 120.7% | 1.9% | False |
| T4|Managed_Money Extreme_Short 4w             | 1.655% | 1.68 | 3.96 | 1.594% | 1.16 | 2.46 | 30.8% | 37.9% | 0.2% | False |
| T4|Managed_Money Extreme_Long 4w              | 1.566% | 1.24 | 2.54 | 2.764% | 2.73 | 5.06 | 119.5% | 99.0% | 27.0% | False |
| T1|Commercial 4w Q5_High                      | 1.372% | 1.13 | 2.24 | 2.085% | 1.47 | 3.14 | 30.7% | 40.3% | 0.5% | False |
| T1|Commercial 2w Q1_Low                       | 0.693% | 1.16 | 1.81 | 1.157% | 1.75 | 2.44 | 50.3% | 34.6% | 23.8% | False |
| T3|Bearish Div 4w                             | 1.342% | 1.12 | 2.31 | 2.770% | 2.40 | 5.20 | 114.7% | 124.9% | 16.6% | False |
| T4|Commercial Extreme_Long 2w                 | 0.976% | 2.67 | 3.74 | 0.935% | 1.25 | 1.97 | 53.2% | 47.2% | 10.3% | False |
| T2|DCommercial 1w Q1_Low                      | 0.331% | 1.20 | 1.54 | 0.534% | 1.38 | 1.68 | 14.9% | 9.1% | 1.0% | True |
| T1|Large_Spec 8w Q2                           | 2.877% | 1.25 | 3.47 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T4|Managed_Money Extreme_Long 2w              | 0.644% | 1.10 | 1.74 | 2.126% | 4.86 | 166.94 | 339.7% | 9472.4% | 55.6% | False |
| T4|Small_Spec Extreme_Short 4w                | 1.162% | 0.92 | 1.90 | 2.255% | 1.87 | 4.05 | 103.9% | 112.8% | 15.1% | False |
| T1|Large_Spec 1w Q2                           | 0.394% | 1.26 | 1.57 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T3|Bearish Div 2w                             | 0.676% | 1.17 | 1.81 | 0.959% | 1.74 | 2.43 | 48.6% | 34.0% | 20.6% | False |
| T1|Commercial 1w Q1_Low                       | 0.341% | 1.09 | 1.50 | 0.551% | 1.65 | 1.82 | 50.6% | 21.8% | 0.3% | False |
| T2|DLarge_Spec 1w Q2                          | 0.346% | 1.12 | 1.50 | 0.542% | 2.00 | 2.10 | 79.0% | 39.4% | 14.1% | False |
| T1|Small_Spec 1w Q1_Low                       | 0.265% | 0.84 | 1.37 | 0.703% | 2.12 | 2.22 | 151.1% | 61.7% | 25.2% | False |
| T5|Large_Spec Sideways 1w Q5_High             | 0.349% | 1.31 | 1.62 | 0.326% | 1.19 | 1.55 | 9.0% | 4.0% | 0.6% | True |
| T5|Large_Spec Sideways 8w Q2                  | 2.623% | 1.23 | 3.33 | 0.000% | 0.00 | 0.00 | 100.0% | 100.0% | 100.0% | False |
| T2|DManaged_Money 2w Q5_High                  | 0.519% | 0.91 | 1.56 | 0.955% | 1.49 | 2.12 | 64.3% | 36.4% | 10.8% | False |
| T5|Managed_Money Sideways 8w Q5_High          | 2.518% | 1.08 | 3.17 | 6.251% | 2.65 | 13.35 | 145.3% | 320.9% | 29.8% | False |
| T1|Small_Spec 4w Q4                           | 1.437% | 1.23 | 2.35 | 1.411% | 1.12 | 2.41 | 8.5% | 2.6% | 1.7% | True |
| T5|Commercial Sideways 2w Q5_High             | 0.666% | 1.12 | 1.76 | 0.990% | 1.31 | 2.09 | 17.6% | 18.8% | 4.6% | True |
| T2|DManaged_Money 8w Q5_High                  | 2.347% | 0.90 | 2.46 | 4.048% | 1.55 | 5.14 | 71.7% | 108.6% | 4.1% | False |
| T4|Large_Spec Extreme_Long 1w                 | 0.766% | 2.17 | 2.24 | 0.228% | 0.74 | 1.31 | 65.9% | 41.4% | 10.4% | False |
| T2|DCommercial 2w Q1_Low                      | 0.444% | 0.78 | 1.46 | 1.010% | 1.51 | 2.18 | 94.1% | 48.7% | 9.7% | False |
| T3|Bearish Div 1w                             | 0.311% | 1.00 | 1.45 | 0.603% | 2.27 | 2.25 | 127.6% | 55.0% | 1.8% | False |
| T1|Commercial 4w Q1_Low                       | 1.202% | 0.95 | 2.04 | 2.428% | 1.75 | 3.47 | 83.6% | 70.4% | 21.1% | False |
| T4|Large_Spec Extreme_Short 1w                | 0.433% | 0.88 | 1.35 | 0.561% | 1.30 | 1.66 | 47.8% | 23.2% | 20.0% | False |
| T2|DSmall_Spec 1w Q1_Low                      | 0.173% | 0.52 | 1.20 | 0.627% | 1.69 | 1.91 | 223.2% | 59.1% | 24.5% | False |
| T4|Small_Spec Extreme_Short 8w                | 2.075% | 0.79 | 2.26 | 3.733% | 2.06 | 8.71 | 159.6% | 286.3% | 7.3% | False |
| T5|Small_Spec Sideways 1w Q5_High             | 0.407% | 1.29 | 1.57 | 0.310% | 0.46 | 1.19 | 64.3% | 24.0% | 19.6% | False |
| T5|Managed_Money Sideways 4w Q5_High          | 1.112% | 0.96 | 2.06 | 3.168% | 2.66 | 6.02 | 176.6% | 191.8% | 19.7% | False |
| T3|Bearish Div 8w                             | 1.896% | 0.89 | 2.41 | 5.315% | 2.50 | 11.46 | 182.0% | 374.5% | 41.3% | False |
| T1|Commercial 8w Q1_Low                       | 1.775% | 0.84 | 2.33 | 5.032% | 1.72 | 4.99 | 104.5% | 114.6% | 32.4% | False |
| T5|Commercial Sideways 4w Q1_Low              | 1.082% | 0.89 | 1.93 | 2.102% | 1.58 | 3.01 | 77.3% | 55.6% | 20.2% | False |
| T4|Managed_Money Extreme_Short 2w             | 0.419% | 1.08 | 1.74 | 0.911% | 1.15 | 1.84 | 6.3% | 5.7% | 8.9% | True |
| T4|Large_Spec Extreme_Short 2w                | 0.496% | 0.63 | 1.38 | 1.052% | 1.28 | 2.00 | 103.4% | 45.5% | 6.7% | False |
| T5|Small_Spec Sideways 4w Q4                  | 1.317% | 1.09 | 2.13 | 1.230% | 1.04 | 2.26 | 4.0% | 6.2% | 3.4% | True |
| T5|Managed_Money Sideways 2w Q5_High          | 0.548% | 0.95 | 1.63 | 1.244% | 2.11 | 2.79 | 122.4% | 71.4% | 18.5% | False |
| T5|Commercial Sideways 8w Q1_Low              | 1.605% | 0.79 | 2.19 | 5.006% | 1.69 | 5.04 | 114.0% | 130.2% | 31.6% | False |
| T2|DLarge_Spec 4w Q1_Low                      | 0.956% | 0.75 | 1.70 | 1.842% | 1.32 | 2.72 | 76.9% | 60.0% | 8.6% | False |
| T2|DCommercial 1w Q2                          | 0.412% | 1.06 | 1.52 | 0.274% | 1.14 | 1.53 | 7.1% | 0.3% | 0.9% | True |
| T5|Commercial Sideways 8w Q2                  | 2.867% | 1.06 | 3.03 | 2.218% | 0.90 | 2.98 | 15.0% | 1.6% | 12.8% | True |
| T5|Large_Spec Sideways 8w Q5_High             | 1.586% | 0.60 | 1.82 | 3.180% | 1.24 | 3.57 | 106.1% | 95.6% | 16.9% | False |
| T2|DLarge_Spec 1w Q5_High                     | 0.271% | 0.73 | 1.34 | 0.542% | 1.34 | 1.65 | 84.3% | 23.0% | 5.1% | False |
| T2|DCommercial 8w Q1_Low                      | 1.677% | 0.63 | 1.88 | 4.093% | 1.54 | 5.12 | 143.0% | 172.5% | 7.7% | False |
| T1|Small_Spec 8w Q4                           | 2.349% | 1.04 | 2.78 | 3.163% | 1.08 | 3.24 | 3.3% | 16.2% | 1.6% | True |
| T2|DSmall_Spec 4w Q1_Low                      | 0.520% | 0.42 | 1.36 | 2.150% | 1.64 | 3.74 | 291.0% | 175.4% | 19.6% | False |
| T2|DLarge_Spec 8w Q5_High                     | 1.245% | 0.55 | 1.76 | 4.023% | 1.50 | 4.81 | 171.6% | 172.5% | 29.0% | False |
| T1|Large_Spec 1w Q5_High                      | 0.281% | 0.76 | 1.36 | 0.358% | 1.15 | 1.54 | 50.3% | 13.1% | 2.8% | False |
| T1|Large_Spec 8w Q5_High                      | 1.451% | 0.56 | 1.76 | 3.133% | 1.22 | 3.49 | 117.8% | 98.4% | 20.0% | False |
| T2|DManaged_Money 4w Q5_High                  | 0.931% | 0.74 | 1.66 | 1.786% | 1.31 | 2.70 | 77.2% | 62.5% | 18.2% | False |
| T1|Small_Spec 1w Q4                           | 0.401% | 1.21 | 1.57 | 0.254% | 0.65 | 1.27 | 46.6% | 19.1% | 0.3% | False |
| T1|Managed_Money 8w Q5_High                   | 2.206% | 0.88 | 2.50 | 5.315% | 2.50 | 11.46 | 184.7% | 358.6% | 30.0% | False |
| T2|DSmall_Spec 8w Q1_Low                      | 1.410% | 0.58 | 1.83 | 3.899% | 1.45 | 4.73 | 148.8% | 158.9% | 17.6% | False |
| T2|DLarge_Spec 8w Q1_Low                      | 1.604% | 0.64 | 1.92 | 3.889% | 1.35 | 4.20 | 109.6% | 118.6% | 7.5% | False |
| T2|DLarge_Spec 4w Q5_High                     | 0.713% | 0.55 | 1.53 | 1.978% | 1.42 | 2.92 | 159.6% | 90.8% | 28.4% | False |

## Test 4: Multiple Testing Correction

Total tests: 440
Raw significant (p<0.05): 220
Bonferroni threshold: 0.000114
Bonferroni survivors: 85
BH FDR survivors: 197

Candidates surviving Bonferroni: 57
Candidates surviving FDR: 87

## Test 5: Monte Carlo Simulation (10,000 permutations)

Pass: 75 / 90

| Signal | Actual_SR | MC_Mean_SR | MC_95th | MC_p | PASS |
|--------|-----------|------------|---------|------|------|
| T3|Bullish Div 8w                             | 1.79 | 0.66 | 0.91 | 0.0000 | True |
| T5|Managed_Money Sideways 4w Q1_Low           | 1.77 | 0.64 | 0.99 | 0.0000 | True |
| T5|Managed_Money Sideways 8w Q1_Low           | 1.74 | 0.66 | 0.90 | 0.0000 | True |
| T5|Commercial Sideways 1w Q1_Low              | 1.74 | 0.62 | 1.32 | 0.0049 | True |
| T5|Managed_Money Sideways 1w Q1_Low           | 1.67 | 0.62 | 1.31 | 0.0063 | True |
| T1|Managed_Money 8w Q1_Low                    | 1.68 | 0.65 | 0.87 | 0.0000 | True |
| T1|Managed_Money 4w Q1_Low                    | 1.63 | 0.64 | 0.95 | 0.0000 | True |
| T1|Large_Spec 4w Q2                           | 1.60 | 0.65 | 0.95 | 0.0000 | True |
| T3|Bullish Div 4w                             | 1.61 | 0.65 | 1.03 | 0.0000 | True |
| T4|Commercial Extreme_Long 8w                 | 1.56 | 0.65 | 0.98 | 0.0000 | True |
| T5|Large_Spec Sideways 2w Q2                  | 1.53 | 0.61 | 1.11 | 0.0008 | True |
| T5|Managed_Money Sideways 2w Q1_Low           | 1.54 | 0.61 | 1.09 | 0.0013 | True |
| T4|Managed_Money Extreme_Short 8w             | 1.54 | 0.66 | 0.98 | 0.0000 | True |
| T5|Large_Spec Sideways 4w Q2                  | 1.53 | 0.64 | 0.99 | 0.0000 | True |
| T1|Large_Spec 2w Q2                           | 1.52 | 0.61 | 1.05 | 0.0002 | True |
| T1|Managed_Money 2w Q1_Low                    | 1.52 | 0.61 | 1.05 | 0.0002 | True |
| T4|Managed_Money Extreme_Long 1w              | 1.52 | 0.63 | 1.56 | 0.0598 | False |
| T1|Managed_Money 1w Q1_Low                    | 1.52 | 0.62 | 1.23 | 0.0087 | True |
| T4|Commercial Extreme_Long 4w                 | 1.51 | 0.65 | 1.11 | 0.0012 | True |
| T1|Commercial 8w Q5_High                      | 1.47 | 0.66 | 0.87 | 0.0000 | True |
| T5|Commercial Sideways 8w Q5_High             | 1.45 | 0.66 | 0.89 | 0.0000 | True |
| T4|Commercial Extreme_Long 1w                 | 1.45 | 0.63 | 1.57 | 0.0762 | False |
| T5|Managed_Money Sideways 1w Q5_High          | 1.45 | 0.62 | 1.32 | 0.0261 | True |
| T5|Commercial Sideways 1w Q5_High             | 1.42 | 0.62 | 1.32 | 0.0276 | True |
| T5|Commercial Sideways 2w Q1_Low              | 1.42 | 0.62 | 1.11 | 0.0032 | True |
| T2|DManaged_Money 1w Q5_High                  | 1.41 | 0.62 | 1.24 | 0.0173 | True |
| T4|Large_Spec Extreme_Short 8w                | 1.40 | 0.66 | 0.98 | 0.0001 | True |
| T3|Bullish Div 1w                             | 1.38 | 0.63 | 1.36 | 0.0461 | True |
| T3|Bullish Div 2w                             | 1.37 | 0.62 | 1.13 | 0.0080 | True |
| T5|Large_Spec Sideways 1w Q2                  | 1.36 | 0.62 | 1.31 | 0.0404 | True |
| T1|Commercial 1w Q5_High                      | 1.35 | 0.61 | 1.23 | 0.0239 | True |
| T1|Commercial 2w Q5_High                      | 1.32 | 0.61 | 1.04 | 0.0046 | True |
| T4|Large_Spec Extreme_Short 4w                | 1.33 | 0.65 | 1.12 | 0.0074 | True |
| T5|Commercial Sideways 4w Q5_High             | 1.32 | 0.64 | 0.99 | 0.0011 | True |
| T4|Managed_Money Extreme_Short 4w             | 1.31 | 0.64 | 1.11 | 0.0073 | True |
| T4|Managed_Money Extreme_Long 4w              | 1.31 | 0.65 | 1.11 | 0.0102 | True |
| T1|Commercial 4w Q5_High                      | 1.30 | 0.65 | 0.95 | 0.0004 | True |
| T1|Commercial 2w Q1_Low                       | 1.33 | 0.61 | 1.04 | 0.0039 | True |
| T3|Bearish Div 4w                             | 1.29 | 0.65 | 1.07 | 0.0057 | True |
| T4|Commercial Extreme_Long 2w                 | 1.29 | 0.61 | 1.26 | 0.0435 | True |
| T2|DCommercial 1w Q1_Low                      | 1.28 | 0.63 | 1.25 | 0.0422 | True |
| T1|Large_Spec 8w Q2                           | 1.25 | 0.66 | 0.87 | 0.0000 | True |
| T4|Managed_Money Extreme_Long 2w              | 1.26 | 0.62 | 1.26 | 0.0493 | True |
| T4|Small_Spec Extreme_Short 4w                | 1.26 | 0.65 | 1.11 | 0.0173 | True |
| T1|Large_Spec 1w Q2                           | 1.26 | 0.62 | 1.25 | 0.0476 | True |
| T3|Bearish Div 2w                             | 1.26 | 0.61 | 1.20 | 0.0348 | True |
| T1|Commercial 1w Q1_Low                       | 1.25 | 0.63 | 1.23 | 0.0442 | True |
| T2|DLarge_Spec 1w Q2                          | 1.25 | 0.62 | 1.25 | 0.0496 | True |
| T1|Small_Spec 1w Q1_Low                       | 1.25 | 0.62 | 1.24 | 0.0474 | True |
| T5|Large_Spec Sideways 1w Q5_High             | 1.23 | 0.61 | 1.31 | 0.0738 | False |
| T5|Large_Spec Sideways 8w Q2                  | 1.23 | 0.65 | 0.89 | 0.0000 | True |
| T2|DManaged_Money 2w Q5_High                  | 1.21 | 0.61 | 1.05 | 0.0126 | True |
| T5|Managed_Money Sideways 8w Q5_High          | 1.23 | 0.66 | 0.89 | 0.0000 | True |
| T1|Small_Spec 4w Q4                           | 1.20 | 0.64 | 0.95 | 0.0016 | True |
| T5|Commercial Sideways 2w Q5_High             | 1.21 | 0.61 | 1.09 | 0.0196 | True |
| T2|DManaged_Money 8w Q5_High                  | 1.20 | 0.65 | 0.86 | 0.0000 | True |
| T4|Large_Spec Extreme_Long 1w                 | 1.20 | 0.63 | 1.58 | 0.1634 | False |
| T2|DCommercial 2w Q1_Low                      | 1.15 | 0.61 | 1.05 | 0.0202 | True |
| T3|Bearish Div 1w                             | 1.16 | 0.62 | 1.47 | 0.1471 | False |
| T1|Commercial 4w Q1_Low                       | 1.17 | 0.64 | 0.95 | 0.0024 | True |
| T4|Large_Spec Extreme_Short 1w                | 1.16 | 0.63 | 1.58 | 0.1771 | False |
| T2|DSmall_Spec 1w Q1_Low                      | 1.15 | 0.62 | 1.24 | 0.0810 | False |
| T4|Small_Spec Extreme_Short 8w                | 1.14 | 0.66 | 0.97 | 0.0051 | True |
| T5|Small_Spec Sideways 1w Q5_High             | 1.13 | 0.62 | 1.32 | 0.1135 | False |
| T5|Managed_Money Sideways 4w Q5_High          | 1.13 | 0.65 | 0.99 | 0.0093 | True |
| T3|Bearish Div 8w                             | 1.10 | 0.66 | 0.95 | 0.0057 | True |
| T1|Commercial 8w Q1_Low                       | 1.09 | 0.65 | 0.86 | 0.0001 | True |
| T5|Commercial Sideways 4w Q1_Low              | 1.08 | 0.65 | 0.99 | 0.0181 | True |
| T4|Managed_Money Extreme_Short 2w             | 1.08 | 0.61 | 1.27 | 0.1174 | False |
| T4|Large_Spec Extreme_Short 2w                | 1.08 | 0.62 | 1.28 | 0.1248 | False |
| T5|Small_Spec Sideways 4w Q4                  | 1.08 | 0.65 | 1.00 | 0.0213 | True |
| T5|Managed_Money Sideways 2w Q5_High          | 1.07 | 0.61 | 1.10 | 0.0597 | False |
| T5|Commercial Sideways 8w Q1_Low              | 1.06 | 0.66 | 0.89 | 0.0018 | True |
| T2|DLarge_Spec 4w Q1_Low                      | 1.05 | 0.64 | 0.95 | 0.0175 | True |
| T2|DCommercial 1w Q2                          | 1.06 | 0.63 | 1.25 | 0.1262 | False |
| T5|Commercial Sideways 8w Q2                  | 1.02 | 0.66 | 0.89 | 0.0058 | True |
| T5|Large_Spec Sideways 8w Q5_High             | 1.07 | 0.66 | 0.89 | 0.0021 | True |
| T2|DLarge_Spec 1w Q5_High                     | 1.05 | 0.63 | 1.25 | 0.1316 | False |
| T2|DCommercial 8w Q1_Low                      | 1.04 | 0.66 | 0.87 | 0.0015 | True |
| T1|Small_Spec 8w Q4                           | 1.05 | 0.66 | 0.87 | 0.0010 | True |
| T2|DSmall_Spec 4w Q1_Low                      | 1.03 | 0.65 | 0.96 | 0.0207 | True |
| T2|DLarge_Spec 8w Q5_High                     | 1.03 | 0.66 | 0.87 | 0.0016 | True |
| T1|Large_Spec 1w Q5_High                      | 1.04 | 0.62 | 1.25 | 0.1378 | False |
| T1|Large_Spec 8w Q5_High                      | 1.05 | 0.66 | 0.86 | 0.0008 | True |
| T2|DManaged_Money 4w Q5_High                  | 1.03 | 0.64 | 0.95 | 0.0210 | True |
| T1|Small_Spec 1w Q4                           | 1.03 | 0.62 | 1.24 | 0.1362 | False |
| T1|Managed_Money 8w Q5_High                   | 0.99 | 0.66 | 0.87 | 0.0042 | True |
| T2|DSmall_Spec 8w Q1_Low                      | 1.02 | 0.66 | 0.87 | 0.0025 | True |
| T2|DLarge_Spec 8w Q1_Low                      | 1.02 | 0.66 | 0.87 | 0.0028 | True |
| T2|DLarge_Spec 4w Q5_High                     | 0.99 | 0.64 | 0.95 | 0.0305 | True |

## Test 6: Gold Drift Neutralization

Pass (positive alpha, p<0.05): 1 / 90

| Signal | Signal_Ret% | BH_Ret% | Alpha_bps | Alpha_Ann% | p_alpha | PASS |
|--------|-------------|---------|-----------|------------|---------|------|
| T3|Bullish Div 8w                             | 4.635% | 1.692% | 294.3 | 19.13% | nan | False |
| T5|Managed_Money Sideways 4w Q1_Low           | 2.103% | 0.844% | 125.9 | 16.37% | nan | False |
| T5|Managed_Money Sideways 8w Q1_Low           | 4.345% | 1.692% | 265.4 | 17.25% | nan | False |
| T5|Commercial Sideways 1w Q1_Low              | 0.496% | 0.214% | 28.3 | 14.70% | 0.0866 | False |
| T5|Managed_Money Sideways 1w Q1_Low           | 0.522% | 0.214% | 30.8 | 16.02% | 0.0643 | False |
| T1|Managed_Money 8w Q1_Low                    | 4.194% | 1.692% | 250.2 | 16.26% | nan | False |
| T1|Managed_Money 4w Q1_Low                    | 2.030% | 0.844% | 118.6 | 15.42% | nan | False |
| T1|Large_Spec 4w Q2                           | 1.996% | 0.844% | 115.3 | 14.98% | nan | False |
| T3|Bullish Div 4w                             | 2.055% | 0.844% | 121.1 | 15.74% | nan | False |
| T4|Commercial Extreme_Long 8w                 | 4.335% | 1.692% | 264.4 | 17.18% | nan | False |
| T5|Large_Spec Sideways 2w Q2                  | 0.946% | 0.410% | 53.6 | 13.94% | nan | False |
| T5|Managed_Money Sideways 2w Q1_Low           | 0.993% | 0.410% | 58.4 | 15.18% | nan | False |
| T4|Managed_Money Extreme_Short 8w             | 3.925% | 1.692% | 223.3 | 14.52% | nan | False |
| T5|Large_Spec Sideways 4w Q2                  | 1.932% | 0.844% | 108.8 | 14.15% | nan | False |
| T1|Large_Spec 2w Q2                           | 0.965% | 0.410% | 55.5 | 14.43% | nan | False |
| T1|Managed_Money 2w Q1_Low                    | 1.000% | 0.410% | 59.0 | 15.34% | nan | False |
| T4|Managed_Money Extreme_Long 1w              | 0.498% | 0.214% | 28.5 | 14.81% | 0.1748 | False |
| T1|Managed_Money 1w Q1_Low                    | 0.521% | 0.214% | 30.8 | 16.01% | 0.0477 | True |
| T4|Commercial Extreme_Long 4w                 | 2.087% | 0.844% | 124.3 | 16.15% | nan | False |
| T1|Commercial 8w Q5_High                      | 3.669% | 1.692% | 197.8 | 12.86% | nan | False |
| T5|Commercial Sideways 8w Q5_High             | 3.680% | 1.692% | 198.9 | 12.93% | nan | False |
| T4|Commercial Extreme_Long 1w                 | 0.576% | 0.214% | 36.2 | 18.82% | 0.0905 | False |
| T5|Managed_Money Sideways 1w Q5_High          | 0.410% | 0.214% | 19.7 | 10.24% | 0.2321 | False |
| T5|Commercial Sideways 1w Q5_High             | 0.448% | 0.214% | 23.5 | 12.21% | 0.1590 | False |
| T5|Commercial Sideways 2w Q1_Low              | 0.829% | 0.410% | 42.0 | 10.91% | nan | False |
| T2|DManaged_Money 1w Q5_High                  | 0.473% | 0.214% | 26.0 | 13.50% | 0.0943 | False |
| T4|Large_Spec Extreme_Short 8w                | 4.730% | 1.692% | 303.9 | 19.75% | nan | False |
| T3|Bullish Div 1w                             | 0.492% | 0.214% | 27.8 | 14.47% | 0.1167 | False |
| T3|Bullish Div 2w                             | 0.922% | 0.410% | 51.3 | 13.33% | nan | False |
| T5|Large_Spec Sideways 1w Q2                  | 0.402% | 0.214% | 18.8 | 9.78% | 0.2558 | False |
| T1|Commercial 1w Q5_High                      | 0.476% | 0.214% | 26.2 | 13.63% | 0.0937 | False |
| T1|Commercial 2w Q5_High                      | 0.903% | 0.410% | 49.3 | 12.83% | nan | False |
| T4|Large_Spec Extreme_Short 4w                | 2.014% | 0.844% | 117.0 | 15.21% | nan | False |
| T5|Commercial Sideways 4w Q5_High             | 1.675% | 0.844% | 83.1 | 10.81% | nan | False |
| T4|Managed_Money Extreme_Short 4w             | 1.618% | 0.844% | 77.4 | 10.06% | nan | False |
| T4|Managed_Money Extreme_Long 4w              | 1.635% | 0.844% | 79.1 | 10.28% | nan | False |
| T1|Commercial 4w Q5_High                      | 1.705% | 0.844% | 86.1 | 11.20% | nan | False |
| T1|Commercial 2w Q1_Low                       | 0.818% | 0.410% | 40.8 | 10.61% | nan | False |
| T3|Bearish Div 4w                             | 1.554% | 0.844% | 71.1 | 9.24% | nan | False |
| T4|Commercial Extreme_Long 2w                 | 0.937% | 0.410% | 52.8 | 13.72% | nan | False |
| T2|DCommercial 1w Q1_Low                      | 0.428% | 0.214% | 21.4 | 11.15% | 0.1666 | False |
| T1|Large_Spec 8w Q2                           | 2.877% | 1.692% | 118.6 | 7.71% | nan | False |
| T4|Managed_Money Extreme_Long 2w              | 0.729% | 0.410% | 32.0 | 8.31% | nan | False |
| T4|Small_Spec Extreme_Short 4w                | 1.571% | 0.844% | 72.7 | 9.45% | nan | False |
| T1|Large_Spec 1w Q2                           | 0.394% | 0.214% | 18.0 | 9.38% | 0.2399 | False |
| T3|Bearish Div 2w                             | 0.718% | 0.410% | 30.9 | 8.03% | nan | False |
| T1|Commercial 1w Q1_Low                       | 0.398% | 0.214% | 18.4 | 9.58% | 0.2303 | False |
| T2|DLarge_Spec 1w Q2                          | 0.379% | 0.214% | 16.6 | 8.61% | 0.2787 | False |
| T1|Small_Spec 1w Q1_Low                       | 0.399% | 0.214% | 18.6 | 9.67% | 0.2268 | False |
| T5|Large_Spec Sideways 1w Q5_High             | 0.332% | 0.214% | 11.8 | 6.16% | 0.4703 | False |
| T5|Large_Spec Sideways 8w Q2                  | 2.623% | 1.692% | 93.2 | 6.06% | nan | False |
| T2|DManaged_Money 2w Q5_High                  | 0.733% | 0.410% | 32.4 | 8.41% | nan | False |
| T5|Managed_Money Sideways 8w Q5_High          | 2.908% | 1.692% | 121.7 | 7.91% | nan | False |
| T1|Small_Spec 4w Q4                           | 1.430% | 0.844% | 58.6 | 7.62% | nan | False |
| T5|Commercial Sideways 2w Q5_High             | 0.810% | 0.410% | 40.0 | 10.40% | nan | False |
| T2|DManaged_Money 8w Q5_High                  | 3.164% | 1.692% | 147.2 | 9.57% | nan | False |
| T4|Large_Spec Extreme_Long 1w                 | 0.386% | 0.214% | 17.3 | 8.99% | 0.4093 | False |
| T2|DCommercial 2w Q1_Low                      | 0.712% | 0.410% | 30.3 | 7.87% | nan | False |
| T3|Bearish Div 1w                             | 0.354% | 0.214% | 14.1 | 7.33% | 0.4619 | False |
| T1|Commercial 4w Q1_Low                       | 1.532% | 0.844% | 68.9 | 8.95% | nan | False |
| T4|Large_Spec Extreme_Short 1w                | 0.520% | 0.214% | 30.6 | 15.92% | 0.1601 | False |
| T2|DSmall_Spec 1w Q1_Low                      | 0.404% | 0.214% | 19.0 | 9.89% | 0.2239 | False |
| T4|Small_Spec Extreme_Short 8w                | 2.695% | 1.692% | 100.4 | 6.52% | nan | False |
| T5|Small_Spec Sideways 1w Q5_High             | 0.400% | 0.214% | 18.6 | 9.69% | 0.2708 | False |
| T5|Managed_Money Sideways 4w Q5_High          | 1.327% | 0.844% | 48.3 | 6.28% | nan | False |
| T3|Bearish Div 8w                             | 2.405% | 1.692% | 71.4 | 4.64% | nan | False |
| T1|Commercial 8w Q1_Low                       | 2.652% | 1.692% | 96.0 | 6.24% | nan | False |
| T5|Commercial Sideways 4w Q1_Low              | 1.359% | 0.844% | 51.5 | 6.69% | nan | False |
| T4|Managed_Money Extreme_Short 2w             | 0.719% | 0.410% | 31.0 | 8.05% | nan | False |
| T4|Large_Spec Extreme_Short 2w                | 0.872% | 0.410% | 46.2 | 12.02% | nan | False |
| T5|Small_Spec Sideways 4w Q4                  | 1.292% | 0.844% | 44.9 | 5.83% | nan | False |
| T5|Managed_Money Sideways 2w Q5_High          | 0.621% | 0.410% | 21.1 | 5.49% | nan | False |
| T5|Commercial Sideways 8w Q1_Low              | 2.528% | 1.692% | 83.6 | 5.44% | nan | False |
| T2|DLarge_Spec 4w Q1_Low                      | 1.416% | 0.844% | 57.2 | 7.44% | nan | False |
| T2|DCommercial 1w Q2                          | 0.387% | 0.214% | 17.4 | 9.03% | 0.2701 | False |
| T5|Commercial Sideways 8w Q2                  | 2.672% | 1.692% | 98.1 | 6.37% | nan | False |
| T5|Large_Spec Sideways 8w Q5_High             | 2.772% | 1.692% | 108.1 | 7.02% | nan | False |
| T2|DLarge_Spec 1w Q5_High                     | 0.408% | 0.214% | 19.4 | 10.10% | 0.2225 | False |
| T2|DCommercial 8w Q1_Low                      | 2.798% | 1.692% | 110.6 | 7.19% | nan | False |
| T1|Small_Spec 8w Q4                           | 2.564% | 1.692% | 87.3 | 5.67% | nan | False |
| T2|DSmall_Spec 4w Q1_Low                      | 1.340% | 0.844% | 49.6 | 6.45% | nan | False |
| T2|DLarge_Spec 8w Q5_High                     | 2.616% | 1.692% | 92.4 | 6.01% | nan | False |
| T1|Large_Spec 1w Q5_High                      | 0.339% | 0.214% | 12.5 | 6.50% | 0.4181 | False |
| T1|Large_Spec 8w Q5_High                      | 2.711% | 1.692% | 102.0 | 6.63% | nan | False |
| T2|DManaged_Money 4w Q5_High                  | 1.347% | 0.844% | 50.4 | 6.55% | nan | False |
| T1|Small_Spec 1w Q4                           | 0.360% | 0.214% | 14.7 | 7.62% | 0.3478 | False |
| T1|Managed_Money 8w Q5_High                   | 2.486% | 1.692% | 79.4 | 5.16% | nan | False |
| T2|DSmall_Spec 8w Q1_Low                      | 2.650% | 1.692% | 95.9 | 6.23% | nan | False |
| T2|DLarge_Spec 8w Q1_Low                      | 2.777% | 1.692% | 108.5 | 7.05% | nan | False |
| T2|DLarge_Spec 4w Q5_High                     | 1.346% | 0.844% | 50.2 | 6.52% | nan | False |

## Test 7: Directional Consistency (Quintile Monotonicity)

| Group_Horizon | Q1% | Q2% | Q3% | Q4% | Q5% | Spearman_r | Spearman_p | Mono_Score |
|---------------|-----|-----|-----|-----|-----|------------|------------|------------|
| Commercial 1w | 0.398% | 0.317% | -0.207% | 0.084% | 0.476% | 0.100 | 0.873 | 0.50 |
| Commercial 2w | 0.793% | 0.446% | -0.232% | 0.112% | 0.928% | 0.100 | 0.873 | 0.50 |
| Commercial 4w | 1.510% | 0.809% | -0.327% | 0.513% | 1.714% | 0.100 | 0.873 | 0.50 |
| Commercial 8w | 2.660% | 2.045% | 0.095% | -0.042% | 3.690% | 0.000 | 1.000 | 0.75 |
| Large_Spec 1w | 0.310% | 0.394% | 0.060% | -0.035% | 0.339% | -0.200 | 0.747 | 0.50 |
| Large_Spec 2w | 0.442% | 0.965% | 0.038% | 0.050% | 0.551% | -0.100 | 0.873 | 0.75 |
| Large_Spec 4w | 0.914% | 2.012% | -0.009% | 0.066% | 1.236% | -0.100 | 0.873 | 0.75 |
| Large_Spec 8w | 2.398% | 2.930% | 0.035% | 0.459% | 2.630% | -0.100 | 0.873 | 0.75 |
| Managed_Money 1w | 0.521% | 0.030% | -0.085% | 0.290% | 0.310% | -0.100 | 0.873 | 0.50 |
| Managed_Money 2w | 1.000% | 0.089% | -0.217% | 0.607% | 0.567% | -0.200 | 0.747 | 0.75 |
| Managed_Money 4w | 2.036% | 0.435% | -0.396% | 0.881% | 1.262% | -0.100 | 0.873 | 0.50 |
| Managed_Money 8w | 4.139% | 0.013% | -0.193% | 1.964% | 2.524% | -0.100 | 0.873 | 0.50 |
| Small_Spec 1w | 0.399% | 0.173% | -0.040% | 0.360% | 0.175% | -0.200 | 0.747 | 0.75 |
| Small_Spec 2w | 0.617% | 0.316% | 0.109% | 0.624% | 0.380% | 0.100 | 0.873 | 0.75 |
| Small_Spec 4w | 1.227% | 0.697% | 0.274% | 1.442% | 0.579% | -0.200 | 0.747 | 0.75 |
| Small_Spec 8w | 1.922% | 1.297% | 1.179% | 2.553% | 1.507% | 0.100 | 0.873 | 0.75 |

## Test 8: Implementable Strategy

Composite signal uses 90 survivors
Weeks with signal active: 1484 / 1556

| Horizon | N | Ret% | Sharpe | PF | WR% | CAGR% | MaxDD% | MAR | BH_SR | BH_CAGR% |
|---------|---|------|--------|----|-----|-------|--------|-----|-------|----------|
| 1w | 1484 | 0.255% | 0.74 | 1.32 | 55.1% | 12.34% | -56.46% | 0.22 | 0.61 | 9.91% |
| 2w | 1482 | 0.464% | 0.69 | 1.44 | 55.9% | 11.08% | -81.01% | 0.14 | 0.61 | 9.52% |
| 4w | 1478 | 0.943% | 0.72 | 1.69 | 57.2% | 11.36% | -96.12% | 0.12 | 0.64 | 9.94% |
| 8w | 1470 | 1.833% | 0.71 | 2.06 | 57.0% | 11.01% | -99.88% | 0.11 | 0.65 | 10.02% |

## Final Verdict

| Rank | Signal | N | SR | PF | WR% | T2_WF | T3_OOS | T4_Bonf | T5_MC | T6_Alpha | T7_Mono | PASS |
|------|--------|---|----|----|-----|-------|--------|---------|-------|----------|---------|------|
| 1 | T5|Managed_Money Sideways 4w Q1_Low | 257 | 1.78 | 3.88 | 69.6% | True | True | True | True | False | 0.50 | 3 |
| 2 | T5|Managed_Money Sideways 8w Q1_Low | 256 | 1.75 | 6.41 | 72.3% | True | True | True | True | False | 0.50 | 3 |
| 3 | T1|Managed_Money 4w Q1_Low | 310 | 1.64 | 3.44 | 69.4% | True | True | True | True | False | 0.50 | 3 |
| 4 | T1|Managed_Money 8w Q1_Low | 309 | 1.67 | 5.70 | 72.2% | True | False | True | True | False | 0.50 | 3 |
| 5 | T1|Managed_Money 2w Q1_Low | 311 | 1.52 | 2.26 | 63.3% | True | True | True | True | False | 0.75 | 3 |
| 6 | T5|Managed_Money Sideways 2w Q1_Low | 258 | 1.54 | 2.32 | 65.5% | True | False | True | True | False | 0.75 | 3 |
| 7 | T3|Bullish Div 4w | 229 | 1.61 | 3.49 | 69.9% | False | True | True | True | False | 0.00 | 2 |
| 8 | T1|Large_Spec 4w Q2 | 310 | 1.61 | 3.06 | 62.3% | False | False | True | True | False | 0.75 | 2 |
| 9 | T3|Bullish Div 8w | 225 | 1.79 | 6.72 | 76.0% | False | False | True | True | False | 0.00 | 2 |
| 10 | T5|Managed_Money Sideways 1w Q1_Low | 258 | 1.67 | 1.89 | 57.8% | True | True | False | True | False | 0.50 | 2 |
| 11 | T5|Commercial Sideways 8w Q5_High | 255 | 1.45 | 4.65 | 67.8% | False | False | True | True | False | 0.75 | 2 |
| 12 | T4|Commercial Extreme_Long 8w | 149 | 1.56 | 5.25 | 71.8% | False | True | True | True | False | 0.75 | 2 |
| 13 | T4|Managed_Money Extreme_Short 8w | 148 | 1.54 | 4.75 | 73.0% | False | False | True | True | False | 0.50 | 2 |
| 14 | T5|Large_Spec Sideways 2w Q2 | 257 | 1.56 | 2.19 | 59.9% | False | False | True | True | False | 0.75 | 2 |
| 15 | T5|Large_Spec Sideways 4w Q2 | 257 | 1.53 | 2.94 | 59.9% | False | False | True | True | False | 0.75 | 2 |
| 16 | T1|Large_Spec 2w Q2 | 311 | 1.52 | 2.11 | 60.8% | False | False | True | True | False | 0.75 | 2 |
| 17 | T1|Managed_Money 1w Q1_Low | 312 | 1.52 | 1.77 | 57.4% | True | False | False | True | True | 0.50 | 2 |
| 18 | T4|Commercial Extreme_Long 4w | 153 | 1.51 | 3.25 | 67.3% | False | False | True | True | False | 0.50 | 2 |
| 19 | T5|Commercial Sideways 2w Q1_Low | 258 | 1.42 | 2.06 | 58.9% | False | True | True | True | False | 0.50 | 2 |
| 20 | T1|Commercial 8w Q5_High | 309 | 1.46 | 4.72 | 69.3% | False | True | True | True | False | 0.75 | 2 |
| 21 | T1|Commercial 4w Q5_High | 310 | 1.31 | 2.65 | 67.4% | False | False | True | True | False | 0.50 | 2 |
| 22 | T5|Commercial Sideways 4w Q5_High | 257 | 1.33 | 2.71 | 66.1% | False | False | True | True | False | 0.50 | 2 |
| 23 | T1|Commercial 2w Q5_High | 311 | 1.35 | 2.04 | 65.3% | False | True | True | True | False | 0.50 | 2 |
| 24 | T4|Large_Spec Extreme_Short 4w | 152 | 1.33 | 2.69 | 68.4% | False | False | True | True | False | 0.75 | 2 |
| 25 | T3|Bullish Div 2w | 231 | 1.37 | 2.10 | 64.1% | False | True | True | True | False | 0.00 | 2 |
| 26 | T4|Large_Spec Extreme_Short 8w | 148 | 1.40 | 4.31 | 68.9% | False | False | True | True | False | 0.75 | 2 |
| 27 | T2|DLarge_Spec 8w Q1_Low | 309 | 1.01 | 2.86 | 63.1% | False | False | True | True | False | 0.75 | 2 |
| 28 | T2|DSmall_Spec 8w Q1_Low | 309 | 1.01 | 2.92 | 62.8% | False | False | True | True | False | 0.75 | 2 |
| 29 | T1|Small_Spec 1w Q4 | 311 | 1.03 | 1.46 | 55.9% | True | False | False | False | False | 0.75 | 2 |
| 30 | T1|Managed_Money 8w Q5_High | 309 | 1.02 | 2.87 | 62.1% | False | False | True | True | False | 0.50 | 2 |
| 31 | T2|DLarge_Spec 4w Q5_High | 310 | 1.00 | 2.15 | 60.3% | False | False | True | True | False | 0.75 | 2 |
| 32 | T1|Large_Spec 8w Q5_High | 309 | 1.03 | 2.84 | 60.2% | False | False | True | True | False | 0.75 | 2 |
| 33 | T4|Managed_Money Extreme_Long 4w | 156 | 1.31 | 2.64 | 62.2% | False | False | True | True | False | 0.50 | 2 |
| 34 | T4|Managed_Money Extreme_Short 4w | 152 | 1.31 | 2.84 | 68.4% | False | False | True | True | False | 0.50 | 2 |
| 35 | T3|Bearish Div 4w | 188 | 1.29 | 2.61 | 62.8% | False | False | True | True | False | 0.00 | 2 |
| 36 | T1|Large_Spec 8w Q2 | 308 | 1.27 | 3.54 | 65.3% | False | False | True | True | False | 0.75 | 2 |
| 37 | T1|Commercial 2w Q1_Low | 311 | 1.30 | 1.94 | 58.2% | False | False | True | True | False | 0.50 | 2 |
| 38 | T1|Small_Spec 4w Q4 | 310 | 1.21 | 2.38 | 64.5% | False | True | True | True | False | 0.75 | 2 |
| 39 | T2|DManaged_Money 8w Q5_High | 308 | 1.20 | 3.41 | 67.5% | False | False | True | True | False | 0.50 | 2 |
| 40 | T2|DCommercial 2w Q1_Low | 311 | 1.17 | 1.80 | 61.1% | False | False | True | True | False | 0.50 | 2 |
| 41 | T5|Managed_Money Sideways 8w Q5_High | 255 | 1.22 | 3.60 | 64.3% | False | False | True | True | False | 0.50 | 2 |
| 42 | T4|Small_Spec Extreme_Short 4w | 155 | 1.26 | 2.45 | 66.5% | False | False | True | True | False | 0.75 | 2 |
| 43 | T2|DManaged_Money 2w Q5_High | 311 | 1.22 | 1.83 | 60.8% | False | False | True | True | False | 0.75 | 2 |
| 44 | T5|Large_Spec Sideways 8w Q2 | 255 | 1.22 | 3.29 | 62.4% | False | False | True | True | False | 0.75 | 2 |
| 45 | T1|Small_Spec 8w Q4 | 308 | 1.04 | 2.91 | 59.7% | False | True | True | True | False | 0.75 | 2 |
| 46 | T2|DCommercial 8w Q1_Low | 309 | 1.05 | 2.90 | 65.4% | False | False | True | True | False | 0.75 | 2 |
| 47 | T2|DSmall_Spec 4w Q1_Low | 310 | 1.04 | 2.21 | 61.0% | False | False | True | True | False | 0.75 | 2 |
| 48 | T2|DLarge_Spec 8w Q5_High | 308 | 1.04 | 2.97 | 61.0% | False | False | True | True | False | 0.75 | 2 |
| 49 | T2|DManaged_Money 4w Q5_High | 310 | 1.03 | 2.09 | 61.9% | False | False | True | True | False | 0.50 | 2 |
| 50 | T2|DLarge_Spec 4w Q1_Low | 310 | 1.06 | 2.18 | 61.0% | False | False | True | True | False | 0.75 | 2 |
| 51 | T1|Commercial 8w Q1_Low | 309 | 1.09 | 3.01 | 58.6% | False | False | True | True | False | 0.75 | 2 |
| 52 | T5|Commercial Sideways 4w Q1_Low | 257 | 1.09 | 2.22 | 59.1% | False | False | True | True | False | 0.50 | 2 |
| 53 | T5|Commercial Sideways 8w Q1_Low | 256 | 1.07 | 2.94 | 58.2% | False | False | True | True | False | 0.75 | 2 |
| 54 | T5|Small_Spec Sideways 4w Q4 | 257 | 1.07 | 2.16 | 63.4% | False | True | True | True | False | 0.75 | 2 |
| 55 | T4|Small_Spec Extreme_Short 8w | 155 | 1.14 | 3.22 | 71.0% | False | False | True | True | False | 0.75 | 2 |
| 56 | T5|Managed_Money Sideways 4w Q5_High | 257 | 1.12 | 2.31 | 63.0% | False | False | True | True | False | 0.50 | 2 |
| 57 | T3|Bearish Div 8w | 188 | 1.10 | 2.98 | 59.0% | False | False | True | True | False | 0.00 | 2 |
| 58 | T1|Commercial 4w Q1_Low | 310 | 1.16 | 2.35 | 60.3% | False | False | True | True | False | 0.50 | 2 |
| 59 | T5|Large_Spec Sideways 8w Q5_High | 255 | 1.05 | 2.89 | 59.6% | False | False | True | True | False | 0.75 | 2 |
| 60 | T5|Commercial Sideways 8w Q2 | 255 | 1.06 | 3.16 | 60.4% | False | True | True | True | False | 0.75 | 2 |
| 61 | T2|DManaged_Money 1w Q5_High | 311 | 1.41 | 1.70 | 59.2% | False | True | False | True | False | 0.50 | 1 |
| 62 | T5|Commercial Sideways 1w Q5_High | 258 | 1.42 | 1.73 | 56.6% | False | False | False | True | False | 0.50 | 1 |
| 63 | T4|Managed_Money Extreme_Long 1w | 156 | 1.52 | 1.78 | 62.8% | False | False | False | False | False | 0.50 | 1 |
| 64 | T5|Commercial Sideways 1w Q1_Low | 258 | 1.74 | 1.87 | 62.8% | False | True | False | True | False | 0.50 | 1 |
| 65 | T5|Managed_Money Sideways 1w Q5_High | 258 | 1.45 | 1.66 | 63.2% | False | False | False | True | False | 0.50 | 1 |
| 66 | T4|Commercial Extreme_Long 1w | 156 | 1.45 | 1.73 | 60.3% | False | False | False | False | False | 0.50 | 1 |
| 67 | T4|Managed_Money Extreme_Long 2w | 156 | 1.26 | 1.89 | 59.0% | False | False | False | True | False | 0.75 | 1 |
| 68 | T5|Large_Spec Sideways 1w Q2 | 258 | 1.36 | 1.62 | 63.2% | False | False | False | True | False | 0.50 | 1 |
| 69 | T4|Commercial Extreme_Long 2w | 155 | 1.29 | 2.02 | 63.2% | False | False | False | True | False | 0.50 | 1 |
| 70 | T3|Bullish Div 1w | 232 | 1.38 | 1.70 | 56.9% | False | True | False | True | False | 0.00 | 1 |
| 71 | T1|Commercial 1w Q5_High | 311 | 1.35 | 1.69 | 56.6% | False | True | False | True | False | 0.50 | 1 |
| 72 | T2|DCommercial 1w Q1_Low | 311 | 1.28 | 1.62 | 59.2% | False | True | False | True | False | 0.50 | 1 |
| 73 | T1|Small_Spec 1w Q1_Low | 312 | 1.25 | 1.60 | 52.9% | False | False | False | True | False | 0.75 | 1 |
| 74 | T5|Large_Spec Sideways 1w Q5_High | 258 | 1.23 | 1.57 | 55.8% | False | True | False | False | False | 0.50 | 1 |
| 75 | T4|Large_Spec Extreme_Long 1w | 156 | 1.20 | 1.56 | 56.4% | False | False | False | False | False | 0.50 | 1 |
| 76 | T5|Commercial Sideways 2w Q5_High | 258 | 1.20 | 1.90 | 65.5% | False | True | False | True | False | 0.50 | 1 |
| 77 | T1|Large_Spec 1w Q2 | 311 | 1.26 | 1.57 | 62.1% | False | False | False | True | False | 0.50 | 1 |
| 78 | T3|Bearish Div 2w | 188 | 1.26 | 1.89 | 58.0% | False | False | False | True | False | 0.00 | 1 |
| 79 | T1|Commercial 1w Q1_Low | 312 | 1.25 | 1.58 | 60.6% | False | False | False | True | False | 0.50 | 1 |
| 80 | T2|DLarge_Spec 1w Q2 | 311 | 1.25 | 1.58 | 57.6% | False | False | False | True | False | 0.50 | 1 |
| 81 | T3|Bearish Div 1w | 188 | 1.16 | 1.54 | 63.3% | False | False | False | False | False | 0.00 | 1 |
| 82 | T4|Large_Spec Extreme_Short 1w | 155 | 1.16 | 1.54 | 56.8% | False | False | False | False | False | 0.50 | 1 |
| 83 | T5|Managed_Money Sideways 2w Q5_High | 258 | 1.07 | 1.72 | 57.4% | False | False | False | False | False | 0.75 | 1 |
| 84 | T4|Large_Spec Extreme_Short 2w | 154 | 1.08 | 1.77 | 64.9% | False | False | False | False | False | 0.75 | 1 |
| 85 | T4|Managed_Money Extreme_Short 2w | 154 | 1.08 | 1.82 | 59.7% | False | True | False | False | False | 0.75 | 1 |
| 86 | T5|Small_Spec Sideways 1w Q5_High | 258 | 1.13 | 1.51 | 61.2% | False | False | False | False | False | 0.75 | 1 |
| 87 | T2|DSmall_Spec 1w Q1_Low | 311 | 1.15 | 1.53 | 56.6% | False | False | False | False | False | 0.75 | 1 |
| 88 | T2|DLarge_Spec 1w Q5_High | 311 | 1.05 | 1.50 | 55.9% | False | False | False | False | False | 0.50 | 1 |
| 89 | T2|DCommercial 1w Q2 | 311 | 1.06 | 1.52 | 58.5% | False | True | False | False | False | 0.50 | 1 |
| 90 | T1|Large_Spec 1w Q5_High | 311 | 1.04 | 1.49 | 56.3% | False | False | False | False | False | 0.50 | 1 |

**Surviving Edges (>=6/7): 0**

No real edges survive full validation.

**Failed Edges:**
- T5|Managed_Money Sideways 4w Q1_Low: 3/7 tests passed
- T5|Managed_Money Sideways 8w Q1_Low: 3/7 tests passed
- T1|Managed_Money 4w Q1_Low: 3/7 tests passed
- T1|Managed_Money 8w Q1_Low: 3/7 tests passed
- T1|Managed_Money 2w Q1_Low: 3/7 tests passed
- T5|Managed_Money Sideways 2w Q1_Low: 3/7 tests passed
- T3|Bullish Div 4w: 2/7 tests passed
- T1|Large_Spec 4w Q2: 2/7 tests passed
- T3|Bullish Div 8w: 2/7 tests passed
- T5|Managed_Money Sideways 1w Q1_Low: 2/7 tests passed
- T5|Commercial Sideways 8w Q5_High: 2/7 tests passed
- T4|Commercial Extreme_Long 8w: 2/7 tests passed
- T4|Managed_Money Extreme_Short 8w: 2/7 tests passed
- T5|Large_Spec Sideways 2w Q2: 2/7 tests passed
- T5|Large_Spec Sideways 4w Q2: 2/7 tests passed
- T1|Large_Spec 2w Q2: 2/7 tests passed
- T1|Managed_Money 1w Q1_Low: 2/7 tests passed
- T4|Commercial Extreme_Long 4w: 2/7 tests passed
- T5|Commercial Sideways 2w Q1_Low: 2/7 tests passed
- T1|Commercial 8w Q5_High: 2/7 tests passed
- T1|Commercial 4w Q5_High: 2/7 tests passed
- T5|Commercial Sideways 4w Q5_High: 2/7 tests passed
- T1|Commercial 2w Q5_High: 2/7 tests passed
- T4|Large_Spec Extreme_Short 4w: 2/7 tests passed
- T3|Bullish Div 2w: 2/7 tests passed
- T4|Large_Spec Extreme_Short 8w: 2/7 tests passed
- T2|DLarge_Spec 8w Q1_Low: 2/7 tests passed
- T2|DSmall_Spec 8w Q1_Low: 2/7 tests passed
- T1|Small_Spec 1w Q4: 2/7 tests passed
- T1|Managed_Money 8w Q5_High: 2/7 tests passed
- T2|DLarge_Spec 4w Q5_High: 2/7 tests passed
- T1|Large_Spec 8w Q5_High: 2/7 tests passed
- T4|Managed_Money Extreme_Long 4w: 2/7 tests passed
- T4|Managed_Money Extreme_Short 4w: 2/7 tests passed
- T3|Bearish Div 4w: 2/7 tests passed
- T1|Large_Spec 8w Q2: 2/7 tests passed
- T1|Commercial 2w Q1_Low: 2/7 tests passed
- T1|Small_Spec 4w Q4: 2/7 tests passed
- T2|DManaged_Money 8w Q5_High: 2/7 tests passed
- T2|DCommercial 2w Q1_Low: 2/7 tests passed
- T5|Managed_Money Sideways 8w Q5_High: 2/7 tests passed
- T4|Small_Spec Extreme_Short 4w: 2/7 tests passed
- T2|DManaged_Money 2w Q5_High: 2/7 tests passed
- T5|Large_Spec Sideways 8w Q2: 2/7 tests passed
- T1|Small_Spec 8w Q4: 2/7 tests passed
- T2|DCommercial 8w Q1_Low: 2/7 tests passed
- T2|DSmall_Spec 4w Q1_Low: 2/7 tests passed
- T2|DLarge_Spec 8w Q5_High: 2/7 tests passed
- T2|DManaged_Money 4w Q5_High: 2/7 tests passed
- T2|DLarge_Spec 4w Q1_Low: 2/7 tests passed
- T1|Commercial 8w Q1_Low: 2/7 tests passed
- T5|Commercial Sideways 4w Q1_Low: 2/7 tests passed
- T5|Commercial Sideways 8w Q1_Low: 2/7 tests passed
- T5|Small_Spec Sideways 4w Q4: 2/7 tests passed
- T4|Small_Spec Extreme_Short 8w: 2/7 tests passed
- T5|Managed_Money Sideways 4w Q5_High: 2/7 tests passed
- T3|Bearish Div 8w: 2/7 tests passed
- T1|Commercial 4w Q1_Low: 2/7 tests passed
- T5|Large_Spec Sideways 8w Q5_High: 2/7 tests passed
- T5|Commercial Sideways 8w Q2: 2/7 tests passed
- T2|DManaged_Money 1w Q5_High: 1/7 tests passed
- T5|Commercial Sideways 1w Q5_High: 1/7 tests passed
- T4|Managed_Money Extreme_Long 1w: 1/7 tests passed
- T5|Commercial Sideways 1w Q1_Low: 1/7 tests passed
- T5|Managed_Money Sideways 1w Q5_High: 1/7 tests passed
- T4|Commercial Extreme_Long 1w: 1/7 tests passed
- T4|Managed_Money Extreme_Long 2w: 1/7 tests passed
- T5|Large_Spec Sideways 1w Q2: 1/7 tests passed
- T4|Commercial Extreme_Long 2w: 1/7 tests passed
- T3|Bullish Div 1w: 1/7 tests passed
- T1|Commercial 1w Q5_High: 1/7 tests passed
- T2|DCommercial 1w Q1_Low: 1/7 tests passed
- T1|Small_Spec 1w Q1_Low: 1/7 tests passed
- T5|Large_Spec Sideways 1w Q5_High: 1/7 tests passed
- T4|Large_Spec Extreme_Long 1w: 1/7 tests passed
- T5|Commercial Sideways 2w Q5_High: 1/7 tests passed
- T1|Large_Spec 1w Q2: 1/7 tests passed
- T3|Bearish Div 2w: 1/7 tests passed
- T1|Commercial 1w Q1_Low: 1/7 tests passed
- T2|DLarge_Spec 1w Q2: 1/7 tests passed
- T3|Bearish Div 1w: 1/7 tests passed
- T4|Large_Spec Extreme_Short 1w: 1/7 tests passed
- T5|Managed_Money Sideways 2w Q5_High: 1/7 tests passed
- T4|Large_Spec Extreme_Short 2w: 1/7 tests passed
- T4|Managed_Money Extreme_Short 2w: 1/7 tests passed
- T5|Small_Spec Sideways 1w Q5_High: 1/7 tests passed
- T2|DSmall_Spec 1w Q1_Low: 1/7 tests passed
- T2|DLarge_Spec 1w Q5_High: 1/7 tests passed
- T2|DCommercial 1w Q2: 1/7 tests passed
- T1|Large_Spec 1w Q5_High: 1/7 tests passed

---
*Generated by scripts/research_015_cot_reality_check.py*
