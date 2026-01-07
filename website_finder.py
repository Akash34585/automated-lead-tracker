import requests
from urllib.parse import urlparse

WIKI_API = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "AutomatedLeadTracker/1.0 (contact: akash@example.com)"
}

BLACKLIST = (
    "wikipedia.org",
    "wikimedia.org",
    "about.com",
    "pcmag.com",
    "bloomberg.com",
    "forbes.com",
    "bizjournals.com",
    "destinationcrm.com",
    "windowsitpro.com",
    "gov2expo.com",
    "news.",
    "blogs.",
    "usatoday.com",
    "earth-auroville.com",
    "mazzaroth.com",
    "tibet.com"

)

def normalize(text):
    return text.lower().replace(" ", "").replace(".", "")

def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ""

def find_website(company):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extlinks",
        "titles": company,
        "ellimit": "max"
    }

    try:
        r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"WIKI ERROR for {company}: {e}")
        return ""

    pages = r.json().get("query", {}).get("pages", {})

    company_key = normalize(company)

    candidates = []

    for page in pages.values():
        for link_obj in page.get("extlinks", []):
            for url in link_obj.values():
                domain = extract_domain(url)

                if not domain:
                    continue
                if any(bad in domain for bad in BLACKLIST):
                    continue

                candidates.append((domain, url))

    # 1️⃣ Prefer domains that match company name
    for domain, url in candidates:
        if company_key in normalize(domain):
            return f"https://{domain}"

    # ❌ No fallback guessing
    return ""


    return ""
