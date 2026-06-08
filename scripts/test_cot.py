"""Test CFTC COT data download"""
from cftc_cot import cot_download_year, cot_download_year_range
import pandas as pd

# Try downloading 2026 disaggregated futures data
try:
    df = cot_download_year(
        year=2026,
        cot_report_type='disaggregated_fut',
        store_zip=False
    )
    print(f'2026 disaggregated: {df.shape}')
    
    # Find gold
    names = df['Market_and_Exchange_Names'].unique()
    gold_matches = [n for n in names if 'GOLD' in str(n).upper()]
    print(f'Gold matching names: {gold_matches}')
    
    # Check Commodity Code
    codes = df['CFTC_Commodity_Code'].unique()
    gold_codes = [c for c in codes if 'GOLD' in str(c).upper()]
    print(f'Gold commodity codes: {gold_codes}')
    
    # Check numeric commodity code for gold
    print(f'\nCommodity code sample: {sorted(codes)[:20]}')
    
    # Show gold rows
    for name in gold_matches:
        subset = df[df['Market_and_Exchange_Names'] == name]
        print(f'\n{name}: {len(subset)} rows')
        print(f'Date range: {subset["Report_Date_as_YYYY-MM-DD"].min()} to {subset["Report_Date_as_YYYY-MM-DD"].max()}')
        print(f'Columns with values: {[c for c in subset.columns if subset[c].notna().sum() > 0]}')
        
except Exception as e:
    import traceback
    print(f'Error: {e}')
    traceback.print_exc()
