import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs and snippets."""
    try:
        results = tavily.search(query=query, max_results=5)
    except Exception as e:
        return f"Web search failed: {e}"

    out = []
    for r in results.get("results", []):
        snippet = (r.get("content") or "")[:300]
        out.append(
            f"Title: {r.get('title', 'N/A')}\n"
            f"URL: {r.get('url', 'N/A')}\n"
            f"Snippet: {snippet}\n"
        )

    if not out:
        return "No results found."

    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:4000]
    except Exception as e:
        return f"Could not scrape URL: {e}"
    
print(scrape_url.invoke("https://en.wikipedia.org/wiki/Large_language_model"))