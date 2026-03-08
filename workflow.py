from __future__ import annotations

from typing import TypedDict, List, Any, Dict

from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END

from agent import get_llm, get_tools, build_planner_prompt, build_analyzer_prompt


class ResearchState(TypedDict, total=False):
    question: str
    planner_steps: str
    research_results: List[Dict[str, Any]]
    answer: str


def planner_node(state: ResearchState) -> ResearchState:
    """Use an LLM to plan research steps."""
    llm = get_llm()
    prompt = build_planner_prompt()
    chain = prompt | llm
    result = chain.invoke({"question": state["question"]})
    return {**state, "planner_steps": result.content}


def researcher_node(state: ResearchState) -> ResearchState:
    """
    Use the DuckDuckGo research tool to fetch results for each planner step.
    """
    tools = get_tools()
    research_tool = next(t for t in tools if t.name == "duckduckgo_research")

    steps_text = state.get("planner_steps", "")
    lines = [line.strip() for line in steps_text.splitlines() if line.strip()]

    results: List[Dict[str, Any]] = []
    for line in lines:
        # Strip leading numbering like "1. " or "2) "
        cleaned = line.lstrip("0123456789). ").strip()
        query = f"{state['question']} - {cleaned}"
        tool_output = research_tool.run(query)
        results.append(
            {
                "step": cleaned,
                "query": query,
                "results": tool_output,
            }
        )

    return {**state, "research_results": results}


def analyzer_node(state: ResearchState) -> ResearchState:
    """Use an LLM to synthesize research results into a structured answer."""
    llm = get_llm()
    prompt = build_analyzer_prompt()
    chain = prompt | llm

    result = chain.invoke(
        {
            "question": state["question"],
            "planner_steps": state.get("planner_steps", ""),
            "research_results": state.get("research_results", []),
        }
    )
    return {**state, "answer": result.content}


def build_workflow():
    """
    Build and return the LangGraph workflow app.

    Nodes:
        - planner
        - researcher
        - analyzer
    """
    graph = StateGraph(ResearchState)

    graph.add_node("planner", RunnableLambda(planner_node))
    graph.add_node("researcher", RunnableLambda(researcher_node))
    graph.add_node("analyzer", RunnableLambda(analyzer_node))

    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "analyzer")
    graph.add_edge("analyzer", END)

    return graph.compile()

