from lead_fetcher import fetch_leads
from lead_normalizer import normalize_leads
from sheet_sync import sync_leads
from website_enrichment import enrich_websites
from sheet_service import get_sheet
from sheet_sync import auto_resize_columns

URL = "https://en.wikipedia.org/wiki/List_of_largest_software_companies"

def run():
    print("▶ Starting pipeline")

    raw = fetch_leads(URL, limit=10)
    clean = normalize_leads(raw)

    added = sync_leads(clean)
    print(f"✅ New leads added: {added}")

    enriched = enrich_websites()
    print(f"🌐 Websites enriched: {enriched}")

    # ✅ FINAL POLISH
    sheet = get_sheet()
    auto_resize_columns(sheet)
    print("📐 Columns auto-resized")

if __name__ == "__main__":
    run()
