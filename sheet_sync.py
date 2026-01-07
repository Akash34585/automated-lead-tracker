from sheet_service import get_sheet
import unicodedata

def normalize(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().strip().lower()

def auto_resize_columns(sheet):
    sheet_id = sheet._properties["sheetId"]

    body = {
        "requests": [
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 7  # adjust if you add more columns
                    }
                }
            }
        ]
    }

    sheet.spreadsheet.batch_update(body)

def sync_leads(leads):
    print("▶ Connecting to Google Sheet")
    sheet = get_sheet()

    all_values = sheet.get_all_values()

    if not all_values:
        existing_companies = set()
    else:
        header = [h.strip().lower() for h in all_values[0]]
        rows = all_values[1:]

        try:
            name_idx = header.index("company_name")
        except ValueError:
            raise RuntimeError("❌ 'company_name' column not found in sheet header")

        existing_companies = set(
            normalize(row[name_idx])
            for row in rows
            if len(row) > name_idx and row[name_idx]
        )

    print(f"▶ Existing rows in sheet: {len(existing_companies)}")

    new_rows = []

    for lead in leads:
        key = normalize(lead["company_name"])
        if key in existing_companies:
            continue

        new_rows.append([
            lead["company_name"],
            lead["website"],
            lead["category"],
            lead["location"],
            lead["source"],
            lead["status"],
            lead["fetched_at_utc"]
        ])

    print(f"▶ New rows prepared: {len(new_rows)}")

    if new_rows:
        sheet.append_rows(new_rows, value_input_option="USER_ENTERED")

    return len(new_rows)
