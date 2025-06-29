from rcsbapi.search import AttributeQuery

# Construct a query searching for structures from humans
query = AttributeQuery(
    attribute="rcsb_accession_info.initial_release_date",
    operator="greater_or_equal",  # Other operators include "contains_phrase", "exists", and more
    value="2025-06-22"
)

# Execute query and construct a list from results
results = list(query())
print(results)