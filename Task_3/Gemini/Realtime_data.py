from serpapi import GoogleSearch
import os

SERP_API_KEY = os.getenv("63fe57f3b583cd2dbd871fa26ca61df76f111e4573164df676efa8e46c4daddf")

if not SERP_API_KEY:
    raise Exception("SERP_API_KEY Missing. Set it before running.")

def google_search(query):
    """
    Fetch latest web information using SerpAPI (Google Results)
    """

    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    result = search.get_dict()

    if "organic_results" in result:
        snippets = [item["snippet"] for item in result["organic_results"][:4]]
        return "\n".join(snippets)

    return "No real-time data found on web."
