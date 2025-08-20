
import os, json, requests

HYGRAPH_ENDPOINT = os.getenv("HYGRAPH_ENDPOINT")
HYGRAPH_TOKEN = os.getenv("HYGRAPH_TOKEN")

QUERY_BY_SLUG = '''
query SacredDoc($slug: String!) {
  sacredDoc(where: {slug: $slug}) {
    title
    slug
    body
    updatedAt
  }
}
'''

def fetch_doc(slug: str):
    if not HYGRAPH_ENDPOINT or not HYGRAPH_TOKEN:
        return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HYGRAPH_TOKEN}"
    }
    payload = {"query": QUERY_BY_SLUG, "variables": {"slug": slug}}
    r = requests.post(HYGRAPH_ENDPOINT, headers=headers, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()
    return (data.get("data") or {}).get("sacredDoc")
