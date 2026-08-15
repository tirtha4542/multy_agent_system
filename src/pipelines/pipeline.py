import os
import re
import sys

from rich import print

# Add the project root directory to sys.path first
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.agents.agent import (
    build_scrape_agent,
    build_search_agent,
    critic_agent,
    writer_agent,
)


def _extract_urls(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"https?://[^\s\)\]\"']+", text)))


def run_research_pipeline(topic: str) -> dict:
    state = {}

    print("\n" + "= " * 50)
    print("step 1 - search agent is working")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content
    print("\nsearch result:", state["search_results"])

    print("\n" + "= " * 50)
    print("step 2 - reader agent is scraping top resources")
    print("=" * 50)

    reader_agent = build_scrape_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            ("user", f"Based on these search results about '{topic}', find URLs or references and scrape detailed content: {state['search_results'][:800]}")
        ]
    })

    state["scraped_content"] = reader_result['messages'][-1].content
    print("\nscraped content:", state["scraped_content"])

    print("\n" + "= " * 50)
    print("step 3 - writer is drafting the report....")
    print("=" * 50)
    research_combined = (
        f"SEARCH RESULT:\n {state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    writer_result = writer_agent.invoke({
        "messages": [
            ("user", f"Write a well-structured article about the following topic.\n\nTopic: {topic}\n\nResearch material:\n{research_combined}")
        ]
    })
    state["draft"] = writer_result['messages'][-1].content
    print("\n Final Draft\n", state["draft"])

    print("\n" + "= " * 50)
    print("step 4 - critic is reviewing the report")
    print("=" * 50)

    critic_result = critic_agent.invoke({
        "messages": [
            ("user", f"Review and improve the following article:\n\n{state['draft']}")
        ]
    })
    state["feedback"] = critic_result['messages'][-1].content

    final = state["feedback"]
    marker = "--- FINAL ARTICLE ---"
    if marker in final:
        final = final.split(marker, 1)[1]
    state["final"] = final.strip()

    print("\n critic report \n", state["feedback"])

    return {
        "topic": topic,
        "sources": _extract_urls(state["search_results"]),
        "draft": state["draft"],
        "final": state["final"],
    }


if __name__ == "__main__":
    res = run_research_pipeline("AI revaluation in 2026")
    print(res)
