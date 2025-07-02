import requests
import csv
from datetime import datetime
import os

def fetch_released_pdb_ids(since_date, output_csv):
    url = "https://search.rcsb.org/rcsbsearch/v2/query"
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_accession_info.initial_release_date",
                "operator": "greater_or_equal",
                "value": since_date
            }
        },
        "return_type": "entry",
        "request_options": {
            "return_all_hits": True
        }
    }

    response = requests.post(url, json=query)
    if response.status_code != 200:
        print(f"❌ Failed to fetch from RCSB ({response.status_code})")
        return []

    data = response.json()
    pdb_ids = [item["identifier"] for item in data.get("result_set", [])]

    with open(output_csv, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["PDB_ID"])
        for pid in pdb_ids:
            writer.writerow([pid])

    print(f"✅ {len(pdb_ids)} newly released PDB entries saved to '{output_csv}'")
    return pdb_ids

def main():
    since_date = input("📅 Enter a release date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(since_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    today_str = datetime.now().strftime('%Y-%m-%d')
    output_file = f"released_pdbs_since_{since_date}_saved_{today_str}.csv"
    fetch_released_pdb_ids(since_date, output_file)

if __name__ == "__main__":
    main()
