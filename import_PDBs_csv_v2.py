from rcsbapi.search import AttributeQuery
import csv

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
    
