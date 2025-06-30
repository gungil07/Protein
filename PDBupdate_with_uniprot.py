import requests
import csv
from rcsbapi.search import AttributeQuery


# Construct a query searching for structures from humans
query = AttributeQuery(
    attribute="rcsb_accession_info.initial_release_date",
    operator="greater_or_equal",  # Other operators include "contains_phrase", "exists", and more
    value="2025-06-22"
)

# Execute query and construct a list from results
results = list(query())
#print(results)

with open('PDB_update.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
   # writer.writerows ([results])
    for result in results:
        writer.writerow([result])
    

def get_uniprot_ids_from_pdb(pdb_id):
    pdb_id = pdb_id.lower()
    url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    if pdb_id not in data or 'UniProt' not in data[pdb_id]:
        return []

    return list(data[pdb_id]['UniProt'].keys())

def read_pdb_ids_from_file(filename):
    pdb_ids = []
    with open(filename, 'r') as file:
        for line in file:
            clean = line.strip()
            if clean:
                pdb_ids.append(clean)
    return pdb_ids

def process_pdb_ids(pdb_ids, output_file='pdb_to_uniprot.csv'):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PDB_ID', 'UniProt_IDs'])

        for pdb_id in pdb_ids:
            uniprot_ids = get_uniprot_ids_from_pdb(pdb_id)
            writer.writerow([pdb_id.upper(), ','.join(uniprot_ids) if uniprot_ids else 'N/A'])

    print(f"✅ Results saved to {output_file}")

# ---- Main Execution ----
input_file = 'pdb_update.csv'  # or 'pdb_update.txt'
pdb_ids = read_pdb_ids_from_file(input_file)
process_pdb_ids(pdb_ids)
