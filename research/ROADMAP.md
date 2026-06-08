# ROADMAP — Multi-Asset Edge Discovery Framework

## Cara Pakai

Copy-paste file ini ke AI baru sebagai instruksi tunggal.
AI akan menjalankan seluruh rangkaian tes secara berurutan.

Perintah dasar: `python research/{asset}/scripts/{script}.py`

---

## Prasyarat

```bash
pip install yfinance pandas numpy scipy statsmodels openpyxl
```

- Data: Yahoo Finance (yfinance), Gate.io API / BitMEX API (BTC funding only)
- Struktur folder: `research/{asset}/scripts/`, `reports/{asset}/`, `data/{asset}/`
- Master chronicle: `master_chronicle/{ASSET}_MASTER_CHRONICLE.md`

---

## STANDAR VALIDASI (WAJIB — semua fase)

Setiap kandidat sinyal harus lolos 5 lapis validasi:

### T1 — Initial Screening
| Kriteria | Threshold |
|----------|-----------|
| Profit Factor (PF) | > 1.30 |
| Sharpe Ratio | > 1.00 |
| p-value (t-test) | < 0.05 |
| Min N | > 50 |

### T2 — Walk-Forward (WF)
Data dibagi 5 periode historis. Sinyal harus positif mean di ≥ 4/5 periode.
Gunakan periode: `['2005-2010','2011-2016','2017-2021','2022-2026']` (atau disesuaikan data asset).

### T3 — Out-of-Sample (OOS)
70/30 split temporal (train/test). Sharpe > 0.50 di unseen data.

### T4 — Monte Carlo (MC)
10,000 random shuffle of signal labels. p-value < 0.05.
**Ini tes paling penting.** Hanya sinyal yang lolos MC yang dianggap robust.

### T5 — Drift Neutralization
Bandingkan equity curve sinyal vs buy-and-hold.
Jika BH outperforms sinyal, sinyal adalah *trend artifact* — bukan edge.

### Multiple Testing Correction
Gunakan Bonferroni: α_adj = 0.05 / N_hypotheses.
Contoh: 100 hipotesis → α = 0.0005.

### Klasifikasi Final
| Label | Definisi |
|-------|----------|
| **ROBUST EDGE** | Lolos T1 + T2 + T3 + T4 + T5 |
| **SUSPECT** | Lolos T1 + T2 tapi gagal T3/T4/T5 (artifact / overfit) |
| **NO EDGE** | Gagal T1 |

---

## 1. GOLD — 19 Phase

**Data:** `GC=F` (Gold Futures), 2000-08-30 to 2026-06-08, 6,466 daily bars
**BH Sharpe:** 0.69 | **BH Return:** +12.4%/yr
**Hasil final:** 0 robust edges

### Urutan Eksekusi

| Phase | Script | Deskripsi |
|-------|--------|-----------|
| 1A | `phase1_data_audit.py` | Data audit: completeness, gaps, quality score |
| 1B | `investigate_outliers.py` | Investigate every >4% extreme return event |
| 1C | `compare_futures_vs_spot.py` | GC=F vs GLD correlation check |
| 2 | `phase2_return_dist.py` | Return distribution, normality test, skew/kurtosis |
| 3 | `phase3_mean_reversion.py` | Z-score mean reversion (window×threshold grid) |
| 4 | `phase4_trend_persistence.py` | Streak analysis, momentum tests |
| 5 | `phase5_volatility.py` | Vol clustering, ATR autocorrelation |
| 5A | `audit_overlap_bias.py` | Overlap bias correction for vol prediction |
| **6** | **(SKIPPED — no intraday data at time)** | *Nanti di-cover H1-001* |
| 7 | `phase7_dayofweek.py` | Day of week calendar effects |
| 8 | `phase8_macro_events.py` | NFP, CPI, FOMC event study |
| 9 | `phase9_driver_analysis.py` | Cross-asset: DXY, SP500, VIX, US10Y, Crude, Silver, TLT |
| 10 | `phase10_scorecard.py` | Edge scorecard — ranking semua kandidat |
| 11 | `research_011_conditional_regime.py` | Regime-conditional strategies (50+ conditions) |
| 12 | `research_012_indicator_ensemble.py` | Indicator ensemble models |
| *13-15* | *(numbering gap — no phases)* | |
| 16 | `research_013_signal_persistence.py` | 6 models × 9 holding periods (1d-60d) |
| 17 | `research_014_cot_analysis.py` | CFTC disaggregated COT positioning |
| 18 | `research_015_cot_reality_check.py` | COT validation (T1-T8 tests) |
| 19 | `research_016_external_drivers.py` | Term structure, real yields, ETF flows |
| H1-001 | `research_h1_001_intraday.py` | Intraday session/hour analysis (11,395 hourly bars) |
| H1-002 | `research_h1_002_validation.py` | MC validation of intraday near-misses |

**Catatan Gold:**
- Drift tinggi (Sharpe ~0.69). Banyak sinyal palsu karena trend.
- **Silver→Gold 1d** (Phase 9): r=+0.52, PF 3.07 — ternyata data alignment artifact.
- **Model B (Trend Pullback) 60d** (Phase 16): Sharpe 0.81, MC p=0.000 — gagal SR>1.0.
- **COT** (Phase 17-18): 90 T1 candidates, 89/90 gagal di drift neutralization.
- **Hour 20 UTC / Hour 23 UTC** (H1-001): PF 1.49-1.59 — gagal MC (N terlalu kecil).

---

## 2. BITCOIN — 8 Phase (+ Funding Rate)

**Data:** `BTC-USD`, 2014-09-17 to 2026-06-07, 4,283 daily bars + 17,487 hourly
**BH Sharpe:** 0.97 | **BH Return:** +42.6%/yr
**Hasil final:** 0 robust edges (satu MC survivor tapi trend-confounded)

### Urutan Eksekusi

| Phase | Script | Deskripsi |
|-------|--------|-----------|
| 1 (BTC-001A) | `research_btc_001a.py` | Price structure: trend, MR, vol, regimes |
| 2 (BTC-002) | `research_btc_002.py` | **Funding Rate**: Gate.io + BitMEX perpetual swap data |
| 3 (BTC-003) | `btc_003_calendar.py` | Calendar: day-of-week, month, halving cycles |
| 4 (BTC-004) | `btc_004_macro_events.py` | Macro: NFP, CPI, FOMC, halving, ETF, crash days |
| 5 (BTC-005) | `btc_005_driver_analysis.py` | Cross-asset: DXY, SP500, VIX, US10Y, GLD |
| 6 (BTC-006) | `btc_006_intraday.py` | Intraday H1: sessions, hours, ORB, vol regimes |
| 7 (BTC-007) | `btc_007_signal_persistence.py` | 6 models × 9 holding periods |
| 8 (BTC-008) | `btc_008_external_drivers.py` | GBTC, IBIT, BITO, US10Y, DXY, VIX |

**Catatan Bitcoin:**
- BTC-001A: 1,117 signals → 31 survivors → semuanya trend artifacts.
- BTC-002: Gate.io 4 survivors → BitMEX replication 0/3 fail. **0 robust.**
- BTC-004: NFP Post+3d (WR 63.83%, p=0.0013) — N=47 < 300. FOMC Post+1d (WR 36.17%) — contrarian artifact.
- BTC-006: Hour 22 (PF 1.25) — gagal threshold PF>1.30.
- **BTC-007 Model A (Trend Following) 1d: Sharpe 1.88, MC p=0.024, N=1,513 — satu-satunya MC survivor di seluruh proyek.** Tapi long-biased, tertukar dengan tren naik BTC.
- BTC-008: 79 T1 candidates → 100% WF/OOS pass → **suspicious, semua trend artifact.**

### BTC-002 Detail — Funding Rate

Data dari Gate.io (2019-2024) dan BitMEX (2016-2024).

```
python research/bitcoin/scripts/research_btc_002.py
python research/bitcoin/scripts/analyze_btc002.py
python research/bitcoin/scripts/fetch_bitmex_funding.py
python research/bitcoin/scripts/replication_btc002_bitmex.py
python research/bitcoin/scripts/check_bitmex_replication.py
```

Flow: `research_btc_002.py` → Gate.io survivors → test on BitMEX → replication check.

---

## 3. OIL — 8 Phase

**Data:** `CL=F` (Crude Oil Futures), 2004-01-02 to 2026-06-07, ~5,600 daily
**BH Sharpe:** -0.02 | **BH Return:** -0.2%/yr (zero drift!)
**Hasil final:** 0 edges

### Urutan Eksekusi

| Phase | Script | Deskripsi |
|-------|--------|-----------|
| 1 (OIL-001) | `oil_001_price_structure.py` | Price structure: trend, MR, vol, regimes |
| 2 (OIL-002) | `oil_002_calendar.py` | Calendar + seasonality (driving season vs winter) |
| 3 (OIL-003) | `oil_003_macro_events.py` | Hurricane season, OPEC, crash events |
| 4 (OIL-004) | `oil_004_cross_asset.py` | Cross-asset: DXY, USO, XLE, Brent, SP500 |
| 5 (OIL-005) | `oil_005_term_structure.py` | Term structure (USO/CL=F spread) |
| 6 (OIL-006) | `oil_006_intraday.py` | Intraday H1 + EIA inventory release |
| 7 (OIL-007) | `oil_007_signal_persistence.py` | 6 models × 9 holding periods |
| 8 (OIL-008) | `oil_008_external_drivers.py` | USO vol/divergence, XLE, DXY, US10Y |

**Catatan Oil:**
- **Zero drift** — Sharpe -0.02, beda total dengan Gold/BTC yang punya tren naik.
- Trend following tidak berguna (best Sharpe 0.44 di OIL-007).
- Mean reversion juga tidak berguna.
- Oil dominated oleh *unpredictable supply shocks* (OPEC, geopolitik, hurricane).
- **OIL-004 DXY Q3** (SR 1.36, PF 1.64) dan **USO Q1** (PF 11.13) — T1 survivors yang **belum di-validasi WF/OOS/MC**.

---

## 4. GENERIC SCREENER — Asset Lain

Untuk aset non-core: Silver, IDX30 stocks, Forex.

```bash
python research/generic_screener.py SI=F Silver
python research/generic_screener.py BBCA.JK BBCA
python research/generic_screener.py BBRI.JK BBRI
python research/generic_screener.py TLKM.JK TLKM
python research/generic_screener.py EURUSD=X EURUSD
python research/generic_screener.py USDJPY=X USDJPY
python research/generic_screener.py GBPUSD=X GBPUSD
```

Generic screener menjalankan 8 phase otomatis:
1. Basic Stats
2. Calendar (day + month)
3. Trend & Mean Reversion (streaks + z-score)
4. Volatility Regimes (ATR quintiles)
5. Signal Persistence (6 models × 9 horizons)
6. Cross-Asset Correlation (DXY, SP500, VIX, US10Y, Gold, Oil, USO)
7. Simple MA Crossover (10×30, 20×50, 50×200)
8. External Drivers (driver quintile quantiles + volume)

**Keterbatasan generic screener:**
- Walk-forward pakai 4 periode FIX (`2005-2010, 2011-2016, 2017-2021, 2022-2026`)
- Tidak semua aset punya data sejak 2005 → WF bisa false negative
- Tidak ada MC test
- Tidak ada drift neutralization
- Untuk hasil lebih akurat, rebuild dengan framework proper (pisah fase kayak Gold)

### Hasil yang sudah didapat:

| Asset | Ticker | Bars | BH Sharpe | T1 | WF | Catatan |
|-------|--------|------|-----------|----|----|---------|
| Silver | SI=F | 7,210 | 0.64 | 10 | 0 | T1 candidates gagal WF |
| BBCA | BBCA.JK | 5,423 | 0.77 | 116 | 0 | WF gagal karena data mulai 2004 |
| BBRI | BBRI.JK | 5,423 | 0.54 | 71 | 71 | **Semua WF pass — suspicious, trend artifact** |
| TLKM | TLKM.JK | 5,423 | 0.48 | 19 | 0 | |
| EUR/USD | EURUSD=X | 5,654 | 0.10 | 11 | 0 | |
| USD/JPY | USDJPY=X | 5,654 | 0.10 | 10 | 0 | |
| GBP/USD | GBPUSD=X | 5,654 | -0.14 | 8 | 0 | |

---

## 5. DATA SOURCES

| Asset | Source | Ticker | Period |
|-------|--------|--------|--------|
| Gold | Yahoo Finance | GC=F | 2000-08-30 to 2026-06-08 |
| Bitcoin | Yahoo Finance | BTC-USD | 2014-09-17 to 2026-06-07 |
| Bitcoin (hourly) | Yahoo Finance | BTC-USD | 2024-06-08 to 2026-06-08 |
| BTC Funding | Gate.io API | BTC_USDT perpetual | 2019-11-18 to 2026-06-08 |
| BTC Funding | BitMEX API | XBTUSD perpetual | 2016-01-01 to 2026-06-08 |
| Oil | Yahoo Finance | CL=F | 2004-01-02 to 2026-06-07 |
| Silver | Yahoo Finance | SI=F | 2004-01-02 to 2026-06-08 |
| BBCA | Yahoo Finance | BBCA.JK | 2004-06-08 to 2026-06-08 |
| BBRI | Yahoo Finance | BBRI.JK | 2004-06-08 to 2026-06-08 |
| TLKM | Yahoo Finance | TLKM.JK | 2004-06-08 to 2026-06-08 |
| EUR/USD | Yahoo Finance | EURUSD=X | 2004-01-02 to 2026-06-08 |
| USD/JPY | Yahoo Finance | USDJPY=X | 2004-01-02 to 2026-06-08 |
| GBP/USD | Yahoo Finance | GBPUSD=X | 2004-01-02 to 2026-06-08 |

Cross-asset drivers: `DX-Y.NYB` (DXY), `^GSPC` (SP500), `^VIX` (VIX), `^TNX` (US10Y),
`GC=F` (Gold), `CL=F` (Oil), `USO` (USO), `GLD` (GLD), `TLT` (TLT), `IEF` (IEF).

---

## 6. MASTER CHRONICLE — Template

Setelah selesai 1 aset, buat/tambahkan master chronicle di `master_chronicle/{ASSET}_MASTER_CHRONICLE.md`.

Format:
```markdown
# {ASSET} Edge Discovery Framework — Master Chronicle

> *Ringkasan 1 kalimat: fase berapa, berapa hipotesis, hasilnya apa.*

## Data Foundation
Tabel sumber data (source, symbol, period, observations).

## Per-Phase Summary
### Phase N — Nama Phase
**Script:** `script.py`
Temuan: 1-2 paragraf.
Hasil: Kandidat T1, WF pass, MC pass, klasifikasi final.

...

## Kesimpulan Akhir
- Total kandidat T1: X
- Lolos WF: Y
- Lolos MC: Z
- Robust: 0
- Sinyal terdekat: ... (jika ada)
```

---

## 7. COMMON FAILURE MODES

### (A) Trend Confounding
Sinyal long-biased yang perform karena asetnya naik terus.
**Ciri:** Sharpe tinggi, MC p signifikan, tapi equity curve mirip BH.
**Solusi:** Drift neutralization test (T5).

*Terjadi di: BTC-001A (31 survivors), BTC-007 (MC survivor), BTC-008 (79 T1), BBRI (71 WF pass).*

### (B) Small Sample Artifact
Sinyal dengan N < 300 yang signifikan secara statistik tapi nggak robust.
**Ciri:** p < 0.05 tapi N kecil, gagal MC.
**Solusi:** Wajib N > 300 untuk daily, N > 1,000 untuk hourly.

*Terjadi di: BTC-004 (NFP N=47, FOMC N=47), H1-001 (Hour 20/23 N=490).*

### (C) Data Alignment Artifact
Dua aset terlihat korelatif karena alignment error.
**Ciri:** Korelasi harian tinggi tapi nggak masuk akal fundamental.
**Solusi:** Check lead-lag, weekly correlation, cross-check dengan data lain.

*Terjadi di: Gold Phase 9 (Silver→Gold r=+0.52 tapi artifact).*

### (D) Multiple Testing Inflation
Dari 1,000 hipotesis yang di-test, ~50 akan signifikan secara kebetulan (p<0.05).
**Ciri:** Banyak T1 candidates tapi semuanya gagal OOS/MC.
**Solusi:** Bonferroni correction + MC permutation.

*Terjadi di: Setiap fase. Ini penyebab #1 kegagalan.*

### (E) Period-Dependent WF
Walk-forward pass hanya karena 1-2 periode yang kebetulan bagus.
**Ciri:** WF pass 4/5 tapi mean return di periode lain negatif.
**Solusi:** Periksa tiap periode individual.

*Terjadi di: Generic screener BBRI (WF 71/71 — seluruh periode positif karena tren).*

---

## 8. DECISION TREE — Klasifikasi di Setiap Fase

```
Untuk setiap kandidat sinyal:
├── PF > 1.30? → Ya
├── Sharpe > 1.00? → Ya
├── p < 0.05? → Ya
├── N > 50? → Ya
│   └── → **T1 Candidate**
│       ├── WF pass ≥ 4/5? → Ya
│       │   └── → **WF Candidate**
│       │       ├── OOS Sharpe > 0.50? → Ya
│       │       │   └── → **OOS Candidate**
│       │       │       ├── MC p < 0.05? → Ya
│       │       │       │   └── → **MC Survivor**
│       │       │       │       ├── Drift neutralize? (outperform BH?) → Ya
│       │       │       │       │   └── → 🟢 **ROBUST EDGE**
│       │       │       │       └── Gagal → trend artifact
│       │       │       └── Gagal MC → overfit / noise
│       │       └── Gagal OOS → overfit
│       └── Gagal WF → period-dependent
└── Gagal T1 → **NO EDGE**
```

---

## 9. RINGKASAN HASIL (35 Fase, 7 Aset)

| Aset | Fase | T1 Candidates | WF Pass | MC Pass | Robust |
|------|------|---------------|---------|---------|--------|
| Gold | 19 | ~136 | 0 | 0 | 0 |
| Bitcoin | 8 | ~110 | ~79* | 1** | 0 |
| Oil | 8 | 4*** | 0 | 0 | 0 |
| Silver | 1 (generic) | 10 | 0 | - | 0 |
| BBCA | 1 (generic) | 116 | 0 | - | 0 |
| BBRI | 1 (generic) | 71 | 71 | - | 0 |
| TLKM | 1 (generic) | 19 | 0 | - | 0 |
| EUR/USD | 1 (generic) | 11 | 0 | - | 0 |
| USD/JPY | 1 (generic) | 10 | 0 | - | 0 |
| GBP/USD | 1 (generic) | 8 | 0 | - | 0 |

*BTC-008: 79 T1, semua WF/OOS pass (100%) — suspicious, trend artifact.
**BTC-007 Model A Trend Following 1d: MC p=0.024 — satu-satunya MC survivor, tapi trend-confounded.
***OIL-004: 4 T1 untested (DXY Q3, USO Q1) — belum full validation.

**Kesimpulan final: Dari 35 fase, ribuan hipotesis, nol robust edge yang bisa diautomasi dengan data publik.**
