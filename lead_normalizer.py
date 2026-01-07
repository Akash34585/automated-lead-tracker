from datetime import datetime

def normalize_leads(leads: list[dict]) -> list[dict]:
    normalized = []

    for lead in leads:
        company = lead["company_name"].strip()

        # remove reference markers like [1], [2]
        company = company.split("[")[0].strip()

        location = lead.get("location", "").strip()

        normalized.append({
            "company_name": company,
            "website": lead.get("website", ""),
            "category": lead.get("category", "Software Company"),
            "location": location,
            "source": lead.get("source", ""),
            "status": "new",
            "fetched_at_utc": datetime.utcnow().isoformat()
        })

    return normalized
