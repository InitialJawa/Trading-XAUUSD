"""Find actual CFTC download URLs"""
import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm'
r = requests.get(url, timeout=30)
soup = BeautifulSoup(r.text, 'html.parser')

# Find all links
links = soup.find_all('a', href=True)
print("All links:")
for link in links:
    href = link['href']
    text = link.get_text(strip=True)
    if 'disaggregated' in href.lower() or 'disaggregated' in text.lower() or 'gold' in text.lower():
        print(f"  [{text}] -> {href}")
    elif 'zip' in href.lower() or '.txt' in href.lower() or '.csv' in href.lower():
        if 'fut' in href.lower() or 'disagg' in href.lower():
            print(f"  [{text}] -> {href}")

# Also check for UUID-based URLs
print("\n\nAll hrefs containing 'dea' or 'fut':")
for link in links:
    href = link['href']
    text = link.get_text(strip=True)
    if 'dea' in href.lower() or 'fut' in href.lower() or 'cot' in href.lower():
        print(f"  [{text}] -> {href}")
