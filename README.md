# 🔎 Multi-Agent Research System

An open-source, multi-agent pipeline that researches any topic for you. It
**searches the web**, **scrapes the most relevant pages**, **writes a structured
report**, and then runs it through a **critic agent** that reviews and polishes
the final article.

Built on **LangChain + Mistral AI**, with a **Streamlit** web UI and a terminal
CLI.

---

## ✨ Features

- 🧠 **Four specialized agents** working in sequence:
  1. **Search Agent** – brainstorms queries and searches the web via the Tavily
     API.
  2. **Reader / Scraper Agent** – visits top results and extracts clean,
     readable content.
  3. **Writer Agent** – drafts a structured, fact-grounded article.
  4. **Critic Agent** – reviews the draft, flags weaknesses, and produces a
     final revised article.
- 🌐 **Robust web scraping** with multiple fallback extractors (trafilatura,
  readability, BeautifulSoup).
- 🖥️ **Streamlit UI** with run history, tabs for final report / draft / sources,
  and report download.
- ⌨️ **Terminal CLI** with pretty `rich` output.
- 🔒 **Secure configuration** via environment variables (`.env`).

---

## 🧱 How It Works

```
Search Agent ──▶ Reader Agent ──▶ Writer Agent ──▶ Critic Agent ──▶ Final Report
   (web_search)    (scrape_web)     (draft)          (review & polish)
```

Each stage calls a real LangChain agent defined in `src/agents/agent.py` and
orchestrated by `src/pipelines/pipeline.py`. The pipeline returns a dict
containing the search results, scraped content, draft, and the critic's feedback
with the final article.

---

## 🛠️ Technology Used

| Area            | Technology                                                                                                     |
| --------------- | -------------------------------------------------------------------------------------------------------------- |
| Language        | Python 3.11                                                                                                    |
| Agent framework | LangChain (`langchain`, `langchain-core`, `langchain-community`, `langchain-classic`)                          |
| LLM provider    | Mistral AI via `langchain-mistralai` (`ChatMistralAI`, models: `mistral-small-latest`, `mistral-large-latest`) |
| Web search      | Tavily API (`tavily-python`)                                                                                   |
| Web scraping    | `trafilatura`, `readability-lxml`, `beautifulsoup4`, `lxml`, `requests`                                        |
| Web UI          | Streamlit                                                                                                      |
| CLI output      | `rich`                                                                                                         |
| Config          | `python-dotenv`                                                                                                |
| Observability   | `langsmith` (LangSmith tracing)                                                                                |

---

## 📁 Project Structure

```
multy_agent_system/
├── app.py                  # Streamlit web UI
├── main.py                 # Terminal CLI entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata
├── .env                    # Your API keys (create from .env.example)
├── .python-version         # Python 3.11
└── src/
    ├── agents/
    │   └── agent.py        # Agent definitions & system prompts
    ├── pipelines/
    │   └── pipeline.py     # run_research_pipeline() orchestration
    └── tools/
        └── tools.py        # web_search & scrape_web tools
```

---

## 📦 Installation

### Prerequisites

- **Python 3.11+** installed on your machine
- API keys for:
  - [Mistral AI](https://console.mistral.ai/) (LLM)
  - [Tavily](https://tavily.com/) (web search)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multy_agent_system.git
cd multy_agent_system
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> ⚠️ **Never commit your real `.env` file** – it is already in `.gitignore`.
> Only `MISTRAL_API_KEY` and `TAVILY_API_KEY` are required. The other keys
> (Google, ElevenLabs, AssemblyAI, Langsmith, Weatherstack) are optional and
> only used if you extend the project.

---

## 🚀 Usage

### Option A – Streamlit Web UI

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (defaults to `http://localhost:8501`),
enter a topic, and click **Run pipeline**. The UI shows live progress, past
runs, and tabs for the final report, draft, and sources.

### Option B – Terminal CLI

```bash
python main.py
```

You'll be prompted to enter a research topic. The pipeline prints step-by-step
progress, the sources, the draft, and the final report (after the critic's
review).

---

## 🧪 Example

```
Enter a research topic: The impact of quantum computing on cryptography
```

The pipeline will:

1. Search for recent, authoritative sources.
2. Scrape the top pages for detailed content.
3. Draft a 500–900 word structured article.
4. Critically review it and return the final polished version.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes.
4. Commit and push: `git commit -m "Add your feature"` /
   `git push origin feature/your-feature`
5. Open a Pull Request.

Please make sure your code runs without errors and keep the existing
style/patterns.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Made with ❤️ by the community. Happy researching! 🔎
