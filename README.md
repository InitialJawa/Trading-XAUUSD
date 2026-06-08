# XAU/USD Edge Discovery Framework

A systematic, reproducible research framework for detecting statistically robust trading edges in XAU/USD (Gold Futures, GC=F) across daily and intraday (H1) timeframes.

## Result

**No statistically robust, tradeable edge was discovered.** XAU/USD appears highly efficient for simple statistical patterns.

| Phase | Research | Result |
|-------|----------|--------|
| 001 | Data Audit | 6,466 daily bars, 25.8 yrs, 90/100 quality |
| 001A | Outlier Investigation | 0 anomalies, all valid market events |
| 001B | Futures vs Spot | GC=F is best proxy (weekly r=0.98) |
| 002 | Return Distribution | Fat-tailed, not normal, Sharpe 0.69 |
| 003 | Mean Reversion | 0 edges (anti-edge, loss-making) |
| 004 | Trend Persistence | 0 edges (no momentum) |
| 005 | Volatility Clustering | Magnitude predictable, direction not |
| 005A | Overlap Bias Audit | True R²=0.26 (corrected from 0.91) |
| 007 | Day of Week | 0 edges (Mon/Fri near-misses) |
| 008 | Macro Events | 0 edges (NFP/CPI/FOMC) |
| 009 | Cross-Asset Drivers | Silver→Gold r=0.52, likely artifact |
| 010 | Edge Scorecard | 0 edges pass all criteria |
| 011 | Conditional Regime | 50+ conditions, 0 edges |
| H1-001 | Intraday Session | 5 tests, 0 edges |
| H1-002 | Candidate Validation | 5 near-misses, all rejected by MC |

## Project Structure

```
├── scripts/           # Python research scripts (14 files)
├── reports/           # Markdown research reports (17 files)
├── charts/            # Visualization PNGs (15 files)
├── data/              # CSV datasets
├── validasi.py        # Validation entry point
└── README.md
```

## Data Sources

- **GC=F**: Gold Futures (primary), Yahoo Finance, 2000–2026
- **SI=F**: Silver Futures, Yahoo Finance, 2005–2026
- **DXY**: US Dollar Index, Yahoo Finance, 2002–2026
- **H1 data**: Yahoo Finance (limited to 730 days, 2024–2026)

## Requirements

- Python 3.14+
- pandas, numpy, scipy, matplotlib, yfinance, scikit-learn, requests

## Usage

```powershell
python scripts/phase1_data_audit.py
python scripts/phase2_return_dist.py
# ... run any script independently
```

## Key Finding

The single candidate (Silver closing price → next-day Gold direction) achieves 64.9% win rate, PF 3.07, R²=0.27, consistent across 22 years — but extreme asymmetry (Silver→Gold r=0.52 vs Gold→Silver r=-0.01) suggests a Yahoo Finance data labeling artifact rather than a genuine market inefficiency.

## License

MIT
