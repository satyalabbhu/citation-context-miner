import requests

def get_openalex_id_from_doi(doi):
    """Convert DOI to OpenAlex ID"""
    url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get('id')  # This is the OpenAlex ID
    else:
        return None

def get_citing_papers(doi):
    openalex_id = get_openalex_id_from_doi(doi)
    if not openalex_id:
        print("DOI not found in OpenAlex.")
        return []

    print(f"Found OpenAlex ID: {openalex_id}")
    citing_url = f"https://api.openalex.org/works?filter=cites:{openalex_id}&per-page=200"
    print("Querying:", citing_url)

    response = requests.get(citing_url)
    if response.status_code != 200:
        print("Error fetching citing works:", response.status_code)
        return []

    citing_works = response.json()
    citing_data = []

    for work in citing_works.get("results", []):
        # ✅ Safe check for missing nested keys
        primary = work.get("primary_location") or {}
        source = primary.get("source") or {}
        fulltext_url = source.get("url", None)

        citing_data.append({
            "title": work.get("title", ""),
            "doi": work.get("doi", ""),
            "abstract": work.get("abstract_inverted_index", {}),
            "fulltext_url": fulltext_url
        })

    return citing_data
