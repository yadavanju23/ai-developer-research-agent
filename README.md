## AI Developer Research Agent
## Demo

![AI Developer Research Agent UI](screenshots/)
A beginner-friendly Python project that demonstrates how to build an **AI Developer Research Agent** using:
- **LangChain** for LLM orchestration
- **LangGraph** for multi-step workflows
- **DuckDuckGo Search** for web research
- **Streamlit** for a simple UI
- **OpenAI or Groq** as the LLM provider

The agent accepts a developer question, performs internet research, analyzes the results, and returns a **structured, step-by-step solution**.

---

### Problem Statement

Developers often ask complex technical questions that require:
- Understanding the problem context
- Searching multiple web sources
- Comparing and synthesizing information
- Producing a clear plan of action

Raw LLM answers can be:
- Inconsistent in structure
- Weak on explicit research steps
- Hard to evaluate or compare

This project provides an **opinionated template** for a research-focused agent that:
- Uses the web via DuckDuckGo
- Follows a clear **planner → researcher → analyzer** workflow
- Produces **structured, evaluable** answers

---

### Architecture Overview

The project is organized as follows:

- **`app.py`**: Streamlit UI for interacting with the agent.
- **`agent.py`**: Core LLM configuration (OpenAI / Groq) and reusable prompts.
- **`workflow.py`**: LangGraph workflow with `planner`, `researcher`, and `analyzer` nodes.
- **`tools.py`**: DuckDuckGo-based research tool exposed as a LangChain tool.
- **`metrics.py`**: Lightweight evaluation of the agent's responses.
- **`.cursorrules`**: Behavior rules for the AI Developer Research Agent inside Cursor.
- **`.env.example`**: Template for environment variables.
- **`requirements.txt`**: Python dependencies.

High-level flow:

1. **Planner node**: Takes the user's question and breaks it into several **concrete research steps**.
2. **Researcher node**: Uses the **DuckDuckGo research tool** for each step and aggregates results.
3. **Analyzer node**: Uses an LLM to synthesize a **structured solution** from the planner steps and research results.
4. **Metrics**: The final answer is scored for accuracy, research quality, speed, and usefulness.

---

### Installation

1. **Clone the repository**

```bash
git clone <https://github.com/yadavanju23/ai-developer-research-agent.git> ai-developer-research-agent
cd ai-developer-research-agent
```

2. **Create and activate a virtual environment (recommended)**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Copy the example file and fill in your API keys:

```bash
cp .env.example .env
```

Then edit `.env` and set **one** of:
- `PROVIDER=openai` and `OPENAI_API_KEY=...`
- `PROVIDER=groq` and `GROQ_API_KEY=...`

---

### Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

In the UI:
1. Enter a **developer question**, for example:
   - "How can I design a resilient LangGraph workflow with retries?"
   - "What are best practices for structuring a FastAPI project?"
2. Click **“Run research”**.
3. The app will:
   - Plan research steps
   - Perform web searches via DuckDuckGo
   - Analyze and synthesize a structured answer
   - Show intermediate planning and raw research data
   - Display **metrics** for the response

---

### Agent Workflow Details

#### 1. Planner Node (`planner`)

- Implemented in `workflow.py` using a LangChain prompt from `agent.py`.
- Input: the user’s raw question.
- Output: a **numbered list** of focused research queries.

This step encourages the agent to think explicitly before searching.

#### 2. Researcher Node (`researcher`)

- Uses the DuckDuckGo tool defined in `tools.py`.
- For each planner step:
  - Cleans the line (removes numbering)
  - Forms a composite query with the original question + step text
  - Calls DuckDuckGo search and stores:
    - Step description
    - Query used
    - Raw search results (title, URL, snippet)

This produces a **structured research trace** that can be inspected.

#### 3. Analyzer Node (`analyzer`)

- Uses an LLM with a prompt from `agent.py`.
- Input:
  - Original question
  - Planner steps
  - Research results
- Output:
  - A final answer with clear sections for:
    - Context
    - Proposed solution
    - Step-by-step plan

This explicitly separates **explanation** from the **action plan**.

---

### Performance Metrics

Defined in `metrics.py` as simple heuristics (range **1–10,000**):

- **Accuracy**:
  - Penalizes explicit uncertainty (e.g. “I don’t know”).
  - Defaults to a high score when the answer is confident.
- **Research quality**:
  - Uses response length as a proxy for depth and coverage.
- **Speed**:
  - Faster responses get higher scores.
- **Usefulness**:
  - Rewards structured answers with steps and headings.
- **Overall**:
  - Weighted combination of the above.

These metrics are **not rigorous**; they are intentionally simple and transparent, designed for:
- Quick comparison between answers
- Easy customization by beginners

---

### Comparison with Standard LLM Answers

Compared to a single-call LLM chat completion, this agent:

- **Pros**
  - Forces an explicit **planning phase**, which often improves coverage.
  - Uses real web search via DuckDuckGo to ground answers.
  - Produces **consistently structured** outputs (context, findings, plan).
  - Exposes intermediate artifacts (planner steps and raw results) for inspection.
  - Provides basic, numeric metrics you can track or visualize.

- **Cons**
  - Slower than a single LLM call (due to multiple steps + web search).
  - Requires API keys and more dependencies.
  - Metrics are heuristic rather than statistically rigorous.

You can also extend this project to:
- Add more specialized tools (e.g. GitHub search, documentation scrapers).
- Integrate more advanced evaluation frameworks.
- Persist conversations and research traces.

---

### Customization Ideas

- **Prompts**: Tweak the planner and analyzer prompts in `agent.py` to fit your team’s style.
- **Tools**: Add new tools to `tools.py` (e.g. codebase search) and call them from the workflow.
- **Graph**: Use LangGraph features (branches, retries, memory) to handle more complex tasks.
- **Metrics**: Replace the heuristic scores with more robust evaluation methods when needed.

This repository is meant as a **starting point** for building richer AI research agents tailored to your development workflow.

# ai-developer-research-agent