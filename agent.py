import os
from typing import List

from langchain.tools import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from tools import ALL_TOOLS


def get_llm() -> BaseChatModel:
    """
    Return a chat model using either OpenAI or Groq based on env vars.

    Set PROVIDER=openai or PROVIDER=groq in your .env (defaults to openai).
    """
    provider = os.getenv("PROVIDER", "openai").lower()

    if provider == "groq":
        from langchain_groq import ChatGroq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")
        return ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"))

    # Default to OpenAI-compatible API
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.2,
    )


def get_tools() -> List[BaseTool]:
    """Return the list of tools available to the agent."""
    return ALL_TOOLS


def build_planner_prompt() -> ChatPromptTemplate:
    """Prompt for the planner node: break the question into research steps."""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a senior AI developer assistant. "
                "Given a developer question, break it down into 3-7 concrete research steps. "
                "Each step should be an actionable query that can be sent to a web search tool.",
            ),
            (
                "human",
                "Developer question:\n{question}\n\n"
                "Return your answer as a numbered list of research queries.",
            ),
        ]
    )


def build_analyzer_prompt() -> ChatPromptTemplate:
    """Prompt for the analyzer node: synthesize results into a structured solution."""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI Developer Research Agent. "
                "You have access to web research results and must produce a clear, "
                "step-by-step technical solution.\n\n"
                "Requirements:\n"
                "- Summarize relevant findings from the research.\n"
                "- Provide a structured, ordered list of steps to solve the problem.\n"
                "- Clearly separate 'Context', 'Proposed Solution', and 'Step-by-step Plan'.",
            ),
            (
                "human",
                "Developer question:\n{question}\n\n"
                "Planner steps:\n{planner_steps}\n\n"
                "Research results (JSON-like list):\n{research_results}\n\n"
                "Produce the final structured answer.",
            ),
        ]
    )

