import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://ipowatch.in/ipo-grey-market-premium-latest/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
if not table:
    raise Exception("Could not find table on the page — check HTML structure.")

rows = table.find_all("tr")

data = []
for row in rows[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 4:
        name = cols[0].get_text(strip=True)
        gmp = cols[1].get_text(strip=True)
        price_band = cols[2].get_text(strip=True)
        listing_gain = cols[3].get_text(strip=True)  # corrected
        if name and gmp.lower() != "gmp":
            data.append({
                "ipo_name": name,
                "gmp": gmp,
                "price_band": price_band,
                "listing_gain": listing_gain
            })

output = {
    "last_updated": datetime.utcnow().isoformat(),
    "source": URL,
    "data": data
}

with open("gmp.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ Scraped {len(data)} IPOs from IPOWatch and saved to gmp.json")
