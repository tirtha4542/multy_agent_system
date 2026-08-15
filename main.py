import os
import sys

# Fix Unicode output on Windows consoles (cp1252 default)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rich import print

from src.pipelines.pipeline import run_research_pipeline

if __name__ == "__main__":
    topic = input("Enter a research topic: ").strip() or "Recent advances in AI agents"
    result = run_research_pipeline(topic)

    print(f"\n[bold green]Topic:[/bold green] {result['topic']}")
    print(f"[bold green]Sources:[/bold green]")
    for url in result["sources"]:
        print(f"  - {url}")

    print(f"\n[bold cyan]Draft:[/bold cyan]\n{result['draft']}")
    print(f"\n[bold magenta]Final (after critic):[/bold magenta]\n{result['final']}")
