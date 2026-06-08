"""
GENERIC: Multi-Phase Research Script for any ticker
Run: python research/generic_screener.py SI=F Silver
"""
import pandas as pd, numpy as np
from scipy import stats
from pathlib import Path
import warnings, json, sys, yfinance as yf
warnings.filterwarnings('ignore')

TICKER = sys.argv[1] if len(sys.argv) > 1 else 'SI=F'
NAME = sys.argv[2] if len(sys.argv) > 2 else TICKER
BASE = Path('research') / f'{NAME.lower().replace(" ","_")}'
OUT = Path('reports') / f'{NAME.lower().replace(" ","_")}'
DATA = Path('data') / f'{NAME.lower().replace(" ","_")}'
for d in [BASE, BASE/'scripts', OUT, DATA]: d.mkdir(parents=True, exist_ok=True)

print(f"{'='*60}\nGENERIC RESEARCH: {NAME} ({TICKER})\n{'='*60}")

# ── DOWNLOAD DATA ──
print(f"Downloading {TICKER}...")
raw = yf.Ticker(TICKER).history(period='max')
if len(raw) == 0: print("No data"); exit()
if hasattr(raw.index, 'tz') and raw.index.tz is not None: raw.index = raw.index.tz_localize(None)
raw.index = pd.to_datetime(raw.index.date) if hasattr(raw.index, 'date') else raw.index
raw.index.name = 'Date'
raw.to_csv(DATA / f'{TICKER.replace("=","").replace("^","")}_cleaned.csv')
close = raw['Close'].dropna(); ret = close.pct_change().dropna()
high = raw['High']; low = raw['Low']; vol = raw['Volume']
print(f"  {len(close):,} bars, {close.index[0].date()} to {close.index[-1].date()}")

H = {1:'Ret_1d',5:'Ret_5d',10:'Ret_10d',20:'Ret_20d',60:'Ret_60d'}
PPY = {1:252,5:252/5,10:252/10,20:252/20,60:252/60}
for h,c in H.items(): raw[c] = close.pct_change(h).shift(-h)

def metrics(g, label="", ppy=252):
    g=g.dropna(); n=len(g)
    if n<5: return None
    mu=g.mean(); std=g.std(); se=std/max(n**0.5,1)
    t=mu/se if se>0 else 0; p=2*(1-stats.t.cdf(abs(t),max(n-1,1))) if n>1 and se>0 else 1
    sh=mu/std*(ppy**0.5) if std>0 else 0; pos=g[g>0].sum(); neg=abs(g[g<0].sum())
    pf=pos/neg if neg>0 else (np.inf if pos>0 else 0)
    return {'Signal':label,'N':n,'Mean_Ret%':mu*100,'Sharpe':sh,'PF':pf,'WR%':(g>0).mean()*100,'p_val':p}

def quantile(dff, sc, rc, lb, ppy, nq=5):
    d=dff[[sc,rc]].dropna().copy()
    if len(d)<30: return []
    d['Q']=pd.qcut(d[sc].rank(method='first'),nq,labels=[f'Q{i+1}' for i in range(nq)])
    return [metrics(d[d['Q']==q][rc],f'{lb} {q}',ppy) for q in [f'Q{i+1}' for i in range(nq)] if len(d[d['Q']==q])>5]

ALL = []
report = []
report.append(f"# {NAME} ({TICKER}) — Research Report")
report.append(f"**Data:** {len(close):,} bars, {close.index[0].date()} to {close.index[-1].date()}")
report.append("")

# ── PHASE 1: BASIC STATS ──
print("--- Phase 1: Basic Stats ---")
mu=ret.mean()*252*100; std=ret.std()*np.sqrt(252)*100; sh=mu/std if std>0 else 0
report.append("## 1. Basic Statistics")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| Annualized Return | {mu:.2f}% |")
report.append(f"| Annualized Vol | {std:.2f}% |")
report.append(f"| Sharpe (BH) | {sh:.4f} |")
report.append(f"| Min Day | {ret.min()*100:.2f}% |")
report.append(f"| Max Day | {ret.max()*100:.2f}% |")
report.append(f"| Win Rate | {(ret>0).mean()*100:.1f}% |")
ADF_P = "N/A"
try:
    from statsmodels.tsa.stattools import adfuller
    ADF_P = f"{adfuller(ret.dropna())[1]:.4e}"
except: pass
report.append(f"| ADF p-val | {ADF_P} |")
report.append("")

# ── PHASE 2: CALENDAR ──
print("--- Phase 2: Calendar ---")
report.append("## 2. Calendar Effects")
report.append("")
report.append("| Day | N | Mean% | WR% | PF | Sharpe | P |")
report.append("|-----|---|-------|-----|----|--------|---|")
for d in range(5):
    r=ret[ret.index.dayofweek==d]; n=len(r)
    if n<10: continue
    m=r.mean()*100; wr=(r>0).mean()*100; s=r.mean()/r.std()*np.sqrt(252) if r.std()>0 else 0
    pos=r[r>0].sum(); neg=abs(r[r<0].sum()); pf=pos/neg if neg>0 else np.inf
    _,p=stats.ttest_1samp(r,0)
    report.append(f"| {['Monday','Tuesday','Wednesday','Thursday','Friday'][d]} | {n} | {m:.4f} | {wr:.1f} | {pf:.4f} | {s:.4f} | {p:.4e} |")
report.append("")

report.append("| Month | N | Mean% | WR% | PF | P |")
report.append("|-------|---|-------|-----|----|---|")
for m in range(1,13):
    r=ret[ret.index.month==m]; n=len(r)
    if n<10: continue
    m2=r.mean()*100; wr=(r>0).mean()*100
    pos=r[r>0].sum(); neg=abs(r[r<0].sum()); pf=pos/neg if neg>0 else np.inf
    _,p=stats.ttest_1samp(r,0)
    report.append(f"| {pd.Timestamp(2020,m,1).strftime('%B')} | {n} | {m2:.4f} | {wr:.1f} | {pf:.4f} | {p:.4e} |")
report.append("")

# ── PHASE 3: TREND + MEAN REVERSION ──
print("--- Phase 3: Trend & MR ---")
report.append("## 3. Trend & Mean Reversion")
report.append("")
for sl in [1,2,3,5]:
    for direction, label in [(1,'Up'),(-1,'Down')]:
        streak=(ret.shift(1)*direction>0).rolling(sl).sum()
        nxt=ret[streak==sl]
        if len(nxt)>10:
            _,p=stats.ttest_1samp(nxt,0)
            report.append(f"| {sl}-day {label} streak -> next | N={len(nxt)} | Mean={nxt.mean()*100:.4f}% | p={p:.4f} |")
report.append("")

for w in [10,20,50]:
    ma=close.rolling(w).mean(); z=(close-ma)/close.rolling(w).std()
    for th in [1.0,1.5,2.0,2.5]:
        over=ret[z.shift(1).fillna(False)>th]; under=ret[z.shift(1).fillna(False)<-th]
        for data, label in [(over,f'Overbought z>{th}'),(under,f'Oversold z<-{th}')]:
            if len(data)>10:
                _,p=stats.ttest_1samp(data,0); m=data.mean()*100; wr=(data>0).mean()*100
                pos=data[data>0].sum(); neg=abs(data[data<0].sum()); pf=pos/neg if neg>0 else np.inf
                if pf>1.20:
                    report.append(f"| {w}d {label} | N={len(data)} | Mean={m:.4f}% | WR={wr:.1f}% | PF={pf:.4f} | p={p:.4e} |")
report.append("")

# ── PHASE 4: VOLATILITY ──
print("--- Phase 4: Volatility ---")
report.append("## 4. Volatility Regimes")
report.append("")
atr=(high-low).rolling(14).mean()
com=ret.index.intersection(atr.dropna().index)
vq=pd.qcut(atr.loc[com].rank(method='first'),5,labels=['Q1_Low','Q2','Q3','Q4','Q5_High'])
rl=ret.loc[com]
report.append("| Vol Q | N | Mean% | WR% | PF | Sharpe |")
report.append("|-------|---|-------|-----|----|--------|")
for q in ['Q1_Low','Q2','Q3','Q4','Q5_High']:
    r=rl[vq==q]; n=len(r)
    m=r.mean()*100; wr=(r>0).mean()*100; s=r.mean()/r.std()*np.sqrt(252) if r.std()>0 else 0
    pos=r[r>0].sum(); neg=abs(r[r<0].sum()); pf=pos/neg if neg>0 else np.inf
    report.append(f"| {q} | {n} | {m:.4f} | {wr:.1f} | {pf:.4f} | {s:.4f} |")
report.append("")

# ── PHASE 5: SIGNAL PERSISTENCE ──
print("--- Phase 5: Signal Persistence ---")
report.append("## 5. Signal Persistence (6 Models × 9 Horizons)")
report.append("")
HP = {'1d':1,'2d':2,'3d':3,'5d':5,'10d':10,'15d':15,'20d':20,'30d':30,'60d':60}
PPY2 = {'1d':252,'2d':126,'3d':84,'5d':50.4,'10d':25.2,'15d':16.8,'20d':12.6,'30d':8.4,'60d':4.2}
fwd = {k: close.pct_change(v).shift(-v) for k,v in HP.items()}
ema50=close.rolling(50).mean(); ema200=close.rolling(200).mean()
rsi14=100-100/(1+(close.diff().clip(lower=0).rolling(14).mean()/close.diff().clip(upper=0).abs().rolling(14).mean()))
atr14=(high-low).rolling(14).mean(); atr50=(high-low).rolling(50).mean()
h20=high.rolling(20).max().shift(1); l20=low.rolling(20).min().shift(1)
macd=close.ewm(12).mean()-close.ewm(26).mean()
adx_val=(high-low).rolling(14).mean()

models={
    'A_TrendFollow': lambda: ((ema50>ema200)&(adx_val>close.rolling(50).std()*0.5)&(macd>0)).astype(float)*1,
    'B_Pullback': lambda: ((ema50>ema200)&(rsi14<40)&(rsi14>20)).astype(float)*1,
    'C_MeanRev': lambda: pd.Series(np.where(rsi14>80,-1,np.where(rsi14<20,1,0)),index=close.index),
    'D_VolExpand': lambda: ((atr14>1.5*atr50)&(close>close.shift(1))).astype(float)*1,
    'E_Breakout': lambda: pd.Series(np.where(close>h20,1,np.where(close<l20,-1,0)),index=close.index),
    'F_Consensus': None,
}
sig={}
for mn,mf in models.items():
    if mf: sig[mn]=mf()

# Consensus
agree=sum((sig[m]==1).astype(int) for m in ['A_TrendFollow','B_Pullback','C_MeanRev','D_VolExpand','E_Breakout'])
sig['F_Consensus']=pd.Series(np.where(agree>=4,1,np.where(agree<=-4,-1,0)),index=close.index)

report.append("| Model | Best Hold | Sharpe | PF | N |")
report.append("|-------|-----------|--------|----|---|")
for mn in ['A_TrendFollow','B_Pullback','C_MeanRev','D_VolExpand','E_Breakout','F_Consensus']:
    s=sig[mn]; best_sh,best_hp=0,''
    for hp_name in HP:
        common=s.dropna().index.intersection(fwd[hp_name].dropna().index)
        aligned=fwd[hp_name].loc[common]*np.sign(s.loc[common])
        if len(aligned)<10: continue
        sh=aligned.mean()/aligned.std()*np.sqrt(PPY2[hp_name]) if aligned.std()>0 else 0
        if abs(sh)>abs(best_sh): best_sh=sh; best_hp=hp_name
    if best_hp:
        common=s.dropna().index.intersection(fwd[best_hp].dropna().index)
        aligned=fwd[best_hp].loc[common]*np.sign(s.loc[common])
        pos=aligned[aligned>0].sum(); neg=abs(aligned[aligned<0].sum()); pf=pos/neg if neg>0 else np.inf
        report.append(f"| {mn} | {best_hp} | {best_sh:.4f} | {pf:.4f} | {len(aligned):,} |")
report.append("")

# ── PHASE 6: CROSS-ASSET ──
print("--- Phase 6: Cross-Asset ---")
drivers={'DXY':'DX-Y.NYB','SP500':'^GSPC','VIX':'^VIX','US10Y':'^TNX','Gold':'GC=F','Oil':'CL=F','USO':'USO'}
all_dr={}
for nm,tk in drivers.items():
    try:
        t=yf.Ticker(tk); h=t.history(period='max')
        if len(h)>0:
            if hasattr(h.index,'tz') and h.index.tz is not None: h.index=h.index.tz_localize(None)
            h.index=pd.to_datetime(h.index.date); h.index.name='Date'
            all_dr[nm]=h['Close'].dropna()
    except: pass

report.append("## 6. Cross-Asset Correlation")
report.append("")
report.append("| Driver | r (same-day) | r (predictive) |")
report.append("|--------|-------------|----------------|")
for nm,ds in all_dr.items():
    common=ret.index.intersection(ds.dropna().index)
    if len(common)<30: continue
    dr=ds.pct_change().dropna()
    common2=ret.index.intersection(dr.index)
    r_same,_=stats.pearsonr(ret.loc[common2],dr.loc[common2])
    r_pred,_=stats.pearsonr(ret.loc[common2[:-1]],dr.loc[common2[1:]]) if len(common2)>5 else (0,1)
    report.append(f"| {nm} | {r_same:.4f} | {r_pred:.4f} |")
report.append("")

# ── PHASE 7: TREND FOLLOWING (simple) ──
print("--- Phase 7: Trend Following ---")
report.append("## 7. Simple Moving Average Crossover")
report.append("")
for fast,slow,label in [(10,30,'10×30'),(20,50,'20×50'),(50,200,'50×200')]:
    ma_f=close.rolling(fast).mean(); ma_s=close.rolling(slow).mean()
    in_long=ma_f>ma_s
    r=ret[in_long.shift(1).fillna(False)]
    if len(r)>10:
        m=r.mean()*100; wr=(r>0).mean()*100; sh=r.mean()/r.std()*np.sqrt(252) if r.std()>0 else 0
        _,p=stats.ttest_1samp(r,0)
        report.append(f"| {label} MA Cross | N={len(r)} | Mean={m:.4f}% | WR={wr:.1f}% | Sharpe={sh:.4f} | p={p:.4e} |")
report.append("")

# ── PHASE 8: EXTERNAL ──
print("--- Phase 8: External ---")
report.append("## 8. External Drivers")
report.append("")
for nm,ds in all_dr.items():
    common=raw.index.intersection(ds.dropna().index)
    if len(common)<50: continue
    temp=pd.DataFrame(index=common)
    temp['Level']=ds; temp['Chg']=ds.diff()
    for h,rc in H.items():
        t=temp.join(raw[rc],how='inner')
        ALL.extend(quantile(t.dropna(subset=['Level',rc]),'Level',rc,f'{nm}_Level_{h}d',PPY[h]))
        ALL.extend(quantile(t.dropna(subset=['Chg',rc]),'Chg',rc,f'{nm}_Chg_{h}d',PPY[h]))

# Volume signal
vol_z=(vol-vol.rolling(20).mean())/vol.rolling(20).std()
temp=pd.DataFrame(index=raw.index)
temp['Vol_Z']=vol_z
for h,rc in H.items():
    t=temp.join(raw[rc],how='inner')
    ALL.extend(quantile(t.dropna(subset=['Vol_Z',rc]),'Vol_Z',rc,f'VolZ_{h}d',PPY[h]))

if ALL:
    df_a=pd.DataFrame(ALL)
    t1=df_a[(df_a.p_val<0.05)&(df_a.Sharpe>1.0)&(df_a.PF>1.30)&(df_a.N>50)]
    report.append(f"T1 Candidates: {len(t1)}")
    if len(t1)>0:
        report.append("")
        report.append("| Signal | N | Mean% | Sharpe | PF | WR% | p |")
        report.append("|--------|---|-------|--------|----|-----|---|")
        for _,r in t1.sort_values('Sharpe',ascending=False).head(15).iterrows():
            report.append(f"| {r['Signal']} | {r['N']} | {r['Mean_Ret%']:.3f} | {r['Sharpe']:.2f} | {r['PF']:.2f} | {r['WR%']:.1f} | {r['p_val']:.4f} |")
        report.append("")
        # Simple WF
        wf=0
        for _,c in t1.iterrows():
            rc=None
            for h,rc2 in H.items():
                if f'_{h}d' in c['Signal']: rc=rc2; break
            if not rc: continue
            ok=True
            for ps,pe in [('2005','2010'),('2011','2016'),('2017','2021'),('2022','2026')]:
                try:
                    pp=raw.loc[ps:pe,rc].dropna()
                    if len(pp)>5 and pp.mean()<=0: ok=False; break
                except: pass
            if ok: wf+=1
        report.append(f"Walk-Forward: {wf}/{len(t1)}")
report.append("")

# ── SAVE ──
report.append("---")
report.append(f"*Generated by research/generic_screener.py for {TICKER} ({NAME})*")
report_path=OUT/f'{TICKER.replace("=","").replace("^","")}_REPORT.md'
with open(report_path,'w',encoding='utf-8') as f: f.write('\n'.join(report))
print(f"\nReport saved: {report_path}")

# ── SAVE JSON SUMMARY ──
summary={'ticker':TICKER,'name':NAME,'bars':len(close),'start':str(close.index[0].date()),'end':str(close.index[-1].date()),
         'bh_return':f'{mu:.2f}%','bh_vol':f'{std:.2f}%','bh_sharpe':sh,'t1_candidates':len(t1) if ALL and len(df_a)>0 else 0,
         'wf_pass':wf if ALL and len(t1)>0 else 0}
with open(OUT/f'{TICKER.replace("=","").replace("^","")}_summary.json','w') as f: json.dump(summary,f,indent=2)
print(f"Summary: {json.dumps(summary,indent=2)}")
print(f"{'='*60}\n{NAME} ({TICKER}) COMPLETE\n{'='*60}")
