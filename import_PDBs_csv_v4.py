import requests
import csv
from datetime import datetime
import time

def fetch_released_pdb_ids(since_date):
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
        print(f"Failed to fetch from RCSB ({response.status_code})")
        return []

    data = response.json()
    pdb_ids = [item["identifier"] for item in data.get("result_set", [])]
    print(f"Found {len(pdb_ids)} PDB entries since {since_date}")
    return pdb_ids


def get_uniprot_ids_from_pdb(pdb_id):
    """Fetches UniProt IDs using PDBe API"""
    url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb_id.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    if pdb_id.lower() not in data or 'UniProt' not in data[pdb_id.lower()]:
        return []

    return list(data[pdb_id.lower()]['UniProt'].keys())


def fetch_metadata(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch metadata for {pdb_id}")
        return None

    data = response.json()

    title = data.get("struct", {}).get("title", "")
    citation = data.get("rcsb_primary_citation", {})
    pubmed_id = citation.get("pdbx_database_id_pub_med", "")
    exptl = data.get("exptl", [{}])
    method = exptl[0].get("method", "") if exptl else ""
    resolution = data.get("rcsb_entry_info", {}).get("resolution_combined", [None])
    resolution_value = resolution[0] if resolution else None

    # Get UniProt IDs
    uniprot_ids = get_uniprot_ids_from_pdb(pdb_id)
    uniprot_str = ", ".join(uniprot_ids) if uniprot_ids else ""

    return {
        "PDB_ID": pdb_id,
        "Title": title,
        "PubMed_ID": pubmed_id,
        "Resolution (Å)": resolution_value,
        "Experimental Method": method,
        "UniProt_IDs": uniprot_str
    }


def save_to_csv(pdb_data_list, output_file):
    fieldnames = ["PDB_ID", "Title", "PubMed_ID", "Resolution (Å)", "Experimental Method", "UniProt_IDs"]
    with open(output_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in pdb_data_list:
            writer.writerow(row)
    print(f"📁 Metadata saved to: {output_file}")


def main():
    since_date = input("Enter a release date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(since_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    pdb_ids = fetch_released_pdb_ids(since_date)
    if not pdb_ids:
        return

    output_data = []
    for i, pdb_id in enumerate(pdb_ids, 1):
        print(f"Fetching metadata for {pdb_id} ({i}/{len(pdb_ids)})...")
        metadata = fetch_metadata(pdb_id)
        if metadata:
            output_data.append(metadata)
        time.sleep(0.1)  # Be polite to the API

    today_str = datetime.now().strftime('%Y-%m-%d')
    output_file = f"pdb_metadata_since_{since_date}_saved_{today_str}.csv"
    save_to_csv(output_data, output_file)


if __name__ == "__main__":
    main()
