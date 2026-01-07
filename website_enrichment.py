from sheet_service import get_sheet
from website_finder import find_website

def enrich_websites():
    sheet = get_sheet()
    values = sheet.get_all_values()

    headers = values[0]
    print("DEBUG HEADERS:", headers)
    rows = values[1:]

    headers_norm = [h.strip().lower() for h in headers]

    try:
        company_col = headers_norm.index("company_name")
        website_col = headers_norm.index("website")
    except ValueError:
        raise RuntimeError(f"Required columns not found. Headers = {headers}")


    updated = 0

    for i, row in enumerate(rows, start=2):
        website = row[website_col].strip() if len(row) > website_col else ""
        company = row[company_col].strip() if len(row) > company_col else ""

        if website or not company:
            continue

        found = find_website(company)
        print(f"DEBUG | {company} → {found}")

        if found:
            sheet.update_cell(i, website_col + 1, found)
            updated += 1

    return updated
