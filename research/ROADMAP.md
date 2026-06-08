# ROADMAP — Multi-Asset Edge Discovery

## Cara Pakai

Copy-paste file ini ke AI baru sebagai instruksi. AI akan menjalankan
seluruh rangkaian tes secara berurutan tanpa perlu konteks sebelumnya.

---

## Prasyarat

- Python 3.10+
- `yfinance`, `pandas`, `numpy`, `scipy`, `statsmodels`, `openpyxl`
- Direktori: `research/`, `data/`, `reports/`, `master_chronicle/`
- Data dari Yahoo Finance (`yfinance`)

## Urutan Tes

### 1. GOLD — 19 Phase (prioritas utama)

Semua script ada di `research/gold/scripts/GC=F_*`.

| Phase | Script | Judul |
|-------|--------|-------|
| 1 | 01_basic_stats.py | Basic Statistics & Distribution |
| 2 | 02_calendar_monthly.py | Calendar Effects (Monthly) |
| 3 | 03_calendar_weekly.py | Calendar Effects (Weekly) |
| 4-5 | 04_oil_corr.py, 04_brent_corr.py | Cross-Asset: Oil Correlation |
| 6 | 05_dxy_corr.py | Cross-Asset: DXY Correlation |
| 7 | 06_rate_corr.py | Cross-Asset: Interest Rates |
| 8 | 07_inflation_corr.py | Cross-Asset: Inflation |
| 9 | 08_gld_corr.py | Cross-Asset: GLD ETF |
| 10 | 09_goldminers_corr.py | Cross-Asset: Gold Miners |
| 11 | 10_cot.py | COT Report Analysis |
| 12 | 11_trend.py | Trend Following |
| 13 | 12_meanreversion.py | Mean Reversion |
| 14 | 13_volatility.py | Volatility Analysis |
| 15 | 14_intraday.py | Intraday Patterns |
| 16 | 15_signal_persistence.py | Signal Persistence |
| 17 | 16_macro.py | Macro Events |
| 18 | 17_external.py | External Drivers |
| 19 | 18_summary.py | Summary Report |

Jalankan: `python research/gold/scripts/GC=F_XX_*.py`

Setelah selesai, update `master_chronicle/GOLD_MASTER_CHRONICLE.md`.

### 2. BITCOIN — 8 Phase

Script di `research/bitcoin/scripts/BTC-*.py`.

| Phase | Script | Judul |
|-------|--------|-------|
| 1 | BTC-001A_Basic_Stats.py | Basic Statistics |
| 2 | BTC-003_Calendar_Effects.py | Calendar Effects |
| 3 | BTC-004_Macro_Events.py | Macro Events |
| 4 | BTC-005_Driver_Analysis.py | Cross-Asset Drivers |
| 5 | BTC-006_Intraday_Analysis.py | Intraday H1 |
| 6 | BTC-007_Signal_Persistence.py | Signal Persistence |
| 7 | BTC-008_External_Drivers.py | External Drivers |

Jalankan: `python research/bitcoin/scripts/BTC-*.py`

Setelah selesai, update `master_chronicle/BTC_MASTER_CHRONICLE.md`.

### 3. OIL — 8 Phase

Script di `research/oil/scripts/OIL-*.py`. Struktur sama kayak Bitcoin,
tambah term structure phase.

Jalankan: `python research/oil/scripts/OIL-*.py`

Setelah selesai, update `master_chronicle/OIL_MASTER_CHRONICLE.md`.

### 4. Asset Lain — Generic Screener

Untuk SILVER, BBRI, BBCA, TLKM, EUR/USD, USD/JPY, GBP/USD,
atau ticker baru:

```
python research/generic_screener.py TICKER NAMA
```

Ini jalanin 8 phase otomatis: basic stats → calendar → trend →
mean reversion → volatility → signal persistence → cross-asset → macro.

---

## Standar Validasi (Wajib)

1. **Walk-Forward Analysis (WF)**: Data dibagi 5 periode, tiap periode di-test
   terpisah. Wajib majority pass.
2. **Out-of-Sample (OOS)**: 70/30 split, test on unseen data.
3. **Monte Carlo (MC)**: 10,000 shuffle. p-value < 0.05 buat robust.
4. **Drift Neutralization**: Bandingin sinyal vs buy-and-hold. Kalah BH = no edge.
5. **Multiple Testing Correction**: Bonferroni sesuai jumlah hipotesis.

Semua fase harus lolos WF + MC sebelum dibilang "robust edge."
Threshold minimum: PF > 1.30, Sharpe > 0.50.

---

## Output

- Report: `reports/{asset}/{PHASE}_{judul}.md`
- Master chronicle per asset: `master_chronicle/{ASSET}_MASTER_CHRONICLE.md`
- Data olahan: `data/{asset}/`

---

## Catatan Penting

- **Bitcoin**: Tidak pakai COT (n/a), term structure digabung. Skip BTC-002 (n/a).
- **Oil**: Zero drift (Sharpe -0.02). Tidak ada trend following, tidak ada mean reversion.
- **Gold**: Drift tinggi (Sharpe ~0.30). Hati-hati sinyal trend-confounded.
- **BTC-007 Trend Following** (Sharpe 1.88, MC p=0.024): Satu-satunya robust survivor,
  tapi long-biased karena BTC tren naik. Wajib drift neutralize sebelum dipakai.
- **Generic screener**: Walk-forward periodya fix (5 period). Untuk akurasi lebih,
  rebuild dengan framework proper.
