"""Download all COT data for gold"""
from cftc_cot import cot_download_year_range
import pandas as pd
import numpy as np

# Download all disaggregated data 2009-2026
print("Downloading COT data 2009-2026...")
df = cot_download_year_range(
    start_year=2009,
    end_year=2026,
    cot_report_type='disaggregated_fut',
    store_zip=True,
    path="./data"
)
print(f"Total rows: {len(df)}")

# Filter for Gold
gold = df[df['Market_and_Exchange_Names'] == 'GOLD - COMMODITY EXCHANGE INC.'].copy()
print(f"Gold rows: {len(gold)}")
print(f"Date range: {gold['Report_Date_as_YYYY-MM-DD'].min()} to {gold['Report_Date_as_YYYY-MM-DD'].max()}")
print(f"Date range by year:")
for yr in range(2009, 2027):
    yr_data = gold[gold['Report_Date_as_YYYY-MM-DD'].str.startswith(str(yr))]
    if len(yr_data) > 0:
        print(f"  {yr}: {len(yr_data)} rows")

# Show key columns sample
key_cols = [
    'Report_Date_as_YYYY-MM-DD', 'Open_Interest_All',
    'Prod_Merc_Positions_Long_All', 'Prod_Merc_Positions_Short_All',
    'Swap_Positions_Long_All', 'Swap__Positions_Short_All',
    'M_Money_Positions_Long_All', 'M_Money_Positions_Short_All',
    'Other_Rept_Positions_Long_All', 'Other_Rept_Positions_Short_All',
    'NonRept_Positions_Long_All', 'NonRept_Positions_Short_All',
]
print(f"\nSample rows:")
print(gold[key_cols].tail(5).to_string())

# Check CFTC codes
print(f"\nMarket code: {gold['CFTC_Market_Code'].iloc[0]}")
print(f"Commodity code: {gold['CFTC_Commodity_Code'].iloc[0]}")
print(f"Contract units: {gold['Contract_Units'].iloc[0]}")

# Compute net positions
gold['Net_Commercial'] = (gold['Prod_Merc_Positions_Long_All'] + gold['Swap_Positions_Long_All']) - \
                         (gold['Prod_Merc_Positions_Short_All'] + gold['Swap__Positions_Short_All'])
gold['Net_Managed_Money'] = gold['M_Money_Positions_Long_All'] - gold['M_Money_Positions_Short_All']
gold['Net_Large_Spec'] = gold['Other_Rept_Positions_Long_All'] - gold['Other_Rept_Positions_Short_All']
gold['Net_Small_Spec'] = gold['NonRept_Positions_Long_All'] - gold['NonRept_Positions_Short_All']

print(f"\nNet position statistics:")
for col in ['Net_Commercial', 'Net_Managed_Money', 'Net_Large_Spec', 'Net_Small_Spec']:
    print(f"  {col}: mean={gold[col].mean():.0f}, std={gold[col].std():.0f}, min={gold[col].min():.0f}, max={gold[col].max():.0f}")

# Save to file
gold.to_csv("data/gold_cot_disaggregated.csv", index=False)
print(f"\nSaved to data/gold_cot_disaggregated.csv")
