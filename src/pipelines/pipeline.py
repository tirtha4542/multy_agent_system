import os
import re
import sys


# Add the project root directory to sys.path first
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.agents.agent import (
    build_scrape_agent,
    build_search_agent,
    critic_agent,
    writer_agent,
)

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
    research_combineed = (
        f"SEARCH RESULT:\n {state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"

    )
    state['report'] = writer_agent.invoke({
        "topic":topic,
        "research":research_combineed
    })
    print("\n Final Report\n",state["report"])

    print("\n" + "= " * 50)
    print("step 4 - critic is reviewing the report")
    print("=" * 50)

    state['feedback'] = critic_agent.invoke({
        "report":state["report"]
    })
    print("\n critic report \n",state["feedback"])

    return state

  

