import os
import sys

# Adds the project root directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI

from src.tools.tools import scrape_web, web_search

load_dotenv()


def _get_llm(model: str, temperature: float) -> ChatMistralAI:
    return ChatMistralAI(model=model, temperature=temperature, max_retries=5)


SEARCH_SYSTEM_PROMPT = """You are an expert research agent. You answer the user's research
request by running the `web_search` tool. Work in two steps:

1. Brainstorm 3-5 high-quality, distinct search queries that would surface authoritative and
   recent sources for the user's topic.
2. Call `web_search` for the most promising queries (you may call it multiple times).

Report your findings as a concise list, with each entry on its own line formatted as:
- Title: <title> | URL: <full url>
After the list, add a one-paragraph summary of the most relevant findings. Always include the
full URLs so another agent can visit them."""


def build_search_agent():
    return create_agent(
        model=_get_llm("mistral-small-latest", temperature=0),
        tools=[web_search],
        system_prompt=SEARCH_SYSTEM_PROMPT,
        name="search_agent",
    )


SCRAPE_SYSTEM_PROMPT = """You are a web content extraction agent. You use the `scrape_web`
tool to fetch and extract the main text content of a web page. The tool takes a full URL.

Return only the essential informative content of the page (its main body text), cleaned and
summarized. Drop navigation, ads, boilerplate and metadata. If the tool reports an error,
report the error and do not fabricate content."""


def build_scrape_agent():
    return create_agent(
        model=_get_llm("mistral-small-latest", temperature=0),
        tools=[scrape_web],
        system_prompt=SCRAPE_SYSTEM_PROMPT,
        name="scrape_agent",
    )


WRITER_SYSTEM_PROMPT = """You are a professional writer agent. You write well-structured,
engaging, factual articles (with an introduction, body sections with subheadings, and a
conclusion) based exclusively on the research material given to you by the user.

Rules:
- Ground every claim in the provided source material; do not invent facts, numbers or quotes.
- Cite sources inline in plain text using (Source: <name or domain>).
- Keep the article between 500 and 900 words.
- Write clear, ready-to-publish prose with no meta-commentary."""


def build_writer_agent():
    return create_agent(
        model=_get_llm("mistral-large-latest", temperature=0.3),
        system_prompt=WRITER_SYSTEM_PROMPT,
        name="writer_agent",
    )


CRITIC_SYSTEM_PROMPT = """You are a demanding editor and critic agent. You review an article
and improve it.

Structure your response exactly as follows:
- First, a short critique: 3-5 bullet points listing strengths and weaknesses (accuracy,
  structure, clarity, tone, evidence).
- Then a line containing exactly: --- FINAL ARTICLE ---
- After that line, the complete revised article, fixing every issue you identified while
  preserving the author's voice and all accurate facts."""


def build_critic_agent():
    return create_agent(
        model=_get_llm("mistral-large-latest", temperature=0.2),
        system_prompt=CRITIC_SYSTEM_PROMPT,
        name="critic_agent",
    )


writer_agent = build_writer_agent()
critic_agent = build_critic_agent()
