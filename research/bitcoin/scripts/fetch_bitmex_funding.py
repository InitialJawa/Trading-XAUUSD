"""Fetch full BitMEX XBTUSD funding rate history."""
import requests, json, time
from pathlib import Path

DATA_DIR = Path('data/bitcoin')
OUTPUT = DATA_DIR / 'XBTUSD_funding_rates_bitmex.json'

symbol = 'XBTUSD'
base_url = f'https://www.bitmex.com/api/v1/funding'
all_records = []
start = 0
count = 500
total = None

while True:
    url = f'{base_url}?symbol={symbol}&count={count}&start={start}&reverse=true'
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        print(f'Error at start={start}: HTTP {r.status_code}')
        break
    data = r.json()
    if len(data) == 0:
        print(f'No more records at start={start}')
        break
    all_records.extend(data)
    print(f'start={start}: got {len(data)} records, total so far: {len(all_records)}, range: {data[-1]["timestamp"]} to {data[0]["timestamp"]}')
    start += count
    if len(data) < count:
        break
    time.sleep(0.5)

print(f'\nTotal records: {len(all_records)}')
print(f'Date range: {all_records[-1]["timestamp"]} to {all_records[0]["timestamp"]}')

DATA_DIR.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, 'w') as f:
    json.dump(all_records, f, default=str)
print(f'Saved to {OUTPUT}')
