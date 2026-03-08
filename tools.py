import os
from typing import List, Dict, Any

from duckduckgo_search import DDGS
from langchain.tools import tool


@tool("duckduckgo_research", return_direct=False)
def duckduckgo_research(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Research tool that uses DuckDuckGo search to fetch web results
    for a developer question.

    Args:
        query: The developer question or search query.
        max_results: Maximum number of search results to return.

    Returns:
        A list of dictionaries containing title, href, and body snippet
        for each result.
    """
    max_results = max(1, min(int(max_results), 10))

    results: List[Dict[str, Any]] = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(
                {
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body"),
                }
            )

    return results


ALL_TOOLS = [duckduckgo_research]

