import pandas as pd
import requests
import re

s = requests.Session()
h = {'User-Agent': 'Mozilla/5.0'}

r = s.get('http://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-hour-bar-quotes/XAUUSD/2022', headers=h, timeout=15)
print('Page status:', r.status_code)

links = re.findall(r'href=[\"\'](.*?)[\"\']', r.text)
for l in links:
    if 'csv' in l or 'zip' in l or 'download' in l:
        print('  Link:', l[:120])

r2 = s.get('http://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-hour-bar-quotes/XAUUSD/2022/1', headers=h, timeout=15, allow_redirects=True)
print('Final URL:', r2.url[:100])
print('Status:', r2.status_code)
print('Type:', r2.headers.get('Content-Type', ''))
print('Size:', len(r2.content))
print('First 300 chars:', r2.text[:300])
