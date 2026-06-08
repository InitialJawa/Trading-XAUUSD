"""Download COT data - files are comma-separated CSV"""
import requests, zipfile, io
import pandas as pd

base = 'https://www.cftc.gov/files/dea/history/'

# Per-year files 2010-2026
years = list(range(2010, 2027))
all_gold = []

for year in years:
    fname = f'fut_disagg_txt_{year}.zip'
    url = f'{base}{fname}'
    print(f'{year}...', end=' ')
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        txt_files = [n for n in z.namelist() if n.endswith('.txt')]
        with z.open(txt_files[0]) as f:
            df = pd.read_csv(f, low_memory=False)
        gold = df[df['Market_and_Exchange_Names'].fillna('').str.contains('GOLD - COMMODITY EXCHANGE', case=False, na=False)]
        print(f'{len(gold)} rows')
        if len(gold) > 0:
            all_gold.append(gold)
    except Exception as e:
        print(f'FAIL: {e}')

# Historical bundle for 2006-2009
print('2006-2009 bundle...', end=' ')
try:
    url = f'{base}fut_disagg_txt_hist_2006_2016.zip'
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    txt_files = [n for n in z.namelist() if n.endswith('.txt')]
    with z.open(txt_files[0]) as f:
        df = pd.read_csv(f, low_memory=False)
    # The historical bundle might have different column name format
    date_col = [c for c in df.columns if 'Report_Date' in c][0]
    if date_col != 'Report_Date_as_YYYY-MM-DD':
        df.rename(columns={date_col: 'Report_Date_as_YYYY-MM-DD'}, inplace=True)
    gold = df[df['Market_and_Exchange_Names'].fillna('').str.contains('GOLD - COMMODITY EXCHANGE', case=False, na=False)]
    print(f'{len(gold)} rows')
    if len(gold) > 0:
        all_gold.append(gold)
except Exception as e:
    print(f'FAIL: {e}')

if not all_gold:
    print('NO GOLD DATA FOUND')
    exit()

# Standardize date column name
for i, df in enumerate(all_gold):
    for c in df.columns:
        if 'Report_Date' in c and c != 'Report_Date_as_YYYY-MM-DD':
            df.rename(columns={c: 'Report_Date_as_YYYY-MM-DD'}, inplace=True)

# Combine
gold = pd.concat(all_gold, ignore_index=True)
print(f'\nCombined gold: {len(gold)} rows')

# Convert date and numeric
gold['Report_Date_as_YYYY-MM-DD'] = pd.to_datetime(gold['Report_Date_as_YYYY-MM-DD'], errors='coerce')
num_cols = ['Open_Interest_All', 'Prod_Merc_Positions_Long_All', 'Prod_Merc_Positions_Short_All',
            'M_Money_Positions_Long_All', 'M_Money_Positions_Short_All',
            'Other_Rept_Positions_Long_All', 'Other_Rept_Positions_Short_All',
            'NonRept_Positions_Long_All', 'NonRept_Positions_Short_All',
            'Swap_Positions_Long_All', 'Swap__Positions_Short_All']
for col in num_cols:
    gold[col] = pd.to_numeric(gold[col].astype(str).str.strip(), errors='coerce')

# Net positions
gold['Net_Commercial'] = (gold['Prod_Merc_Positions_Long_All'] + gold['Swap_Positions_Long_All']) - \
                         (gold['Prod_Merc_Positions_Short_All'] + gold['Swap__Positions_Short_All'])
gold['Net_Managed_Money'] = gold['M_Money_Positions_Long_All'] - gold['M_Money_Positions_Short_All']
gold['Net_Large_Spec'] = gold['Other_Rept_Positions_Long_All'] - gold['Other_Rept_Positions_Short_All']
gold['Net_Small_Spec'] = gold['NonRept_Positions_Long_All'] - gold['NonRept_Positions_Short_All']

gold = gold.sort_values('Report_Date_as_YYYY-MM-DD').reset_index(drop=True)
print(f'Date range: {gold["Report_Date_as_YYYY-MM-DD"].min()} to {gold["Report_Date_as_YYYY-MM-DD"].max()}')
print(f'Total weeks: {len(gold)}')

for col in ['Net_Commercial', 'Net_Managed_Money', 'Net_Large_Spec', 'Net_Small_Spec']:
    vals = gold[col].dropna()
    print(f'  {col}: n={len(vals)}, mean={vals.mean():.0f}, std={vals.std():.0f}')

gold.to_csv('data/gold_cot.csv', index=False, date_format='%Y-%m-%d')
print('\nSaved to data/gold_cot.csv')
