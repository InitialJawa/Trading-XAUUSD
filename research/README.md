# RESEARCH — Multi-Asset Edge Discovery

## Struktur

```
research/
  gold/          — 19 phase (30 scripts), hasil: 0 edge
  bitcoin/       — 8 phase (8 scripts), hasil: 0 edge  
  oil/           — 8 phase (8 scripts), hasil: 0 edge
  silver/        — Generic screener, hasil: 0 edge
  bbca/          — Generic screener, hasil: 0 edge
  bbri/          — Generic screener, hasil: 0 edge
  tlkm/          — Generic screener, hasil: 0 edge
  eurusd/        — Generic screener, hasil: 0 edge
  usdjpy/        — Generic screener, hasil: 0 edge
  gbpusd/        — Generic screener, hasil: 0 edge
  generic_screener.py  — 1 script untuk screening ticker baru
```

## Cara Baca

Setiap folder aset berisi:
- `REPORT.md` — hasil lengkap 8 phase (basic stats, calendar, trend, vol, signal persistence, cross-asset, external)
- `summary.json` — ringkasan 1 baris (BH Sharpe, T1 candidates, WF pass)

## Cara Screening Ticker Baru

```
python research/generic_screener.py TICKER NAMA
```

Hasil otomatis masuk ke `research/{nama}/REPORT.md` dan `data/{nama}/`.

## Hasil Final

Semua 7 aset yang diuji: **tidak ada edge statistik yang bisa diautomasi dengan data publik.**
