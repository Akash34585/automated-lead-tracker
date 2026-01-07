import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_leads(url: str, limit: int = 10):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="wikitable")

    if not tables:
        print("❌ No wikitable found")
        return []

    # On this page, the FIRST wikitable is the companies table
    table = tables[0]

    rows = table.find_all("tr")[1:limit + 1]
    leads = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        company = cols[1].get_text(strip=True)
        location = cols[5].get_text(strip=True)

        leads.append({
            "company_name": company,
            "website": "",
            "category": "Software Company",
            "location": location,
            "source": "wikipedia.org"
        })


    return leads
