import time

import streamlit as st
from dotenv import load_dotenv

from workflow import build_workflow
from metrics import evaluate_response


def main() -> None:
    st.set_page_config(
        page_title="AI Developer Research Agent",
        page_icon="🔍",
        layout="wide",
    )

    st.title("AI Developer Research Agent")
    st.write(
        "Ask a technical question and the agent will research the web, "
        "analyze the findings, and produce a structured solution."
    )

    load_dotenv()  # Load environment variables from .env if present

    question = st.text_area(
        "Developer question",
        placeholder="e.g. How can I design a LangGraph workflow for multi-step API debugging?",
        height=150,
    )

    if st.button("Run research") and question.strip():
        with st.spinner("Researching and analyzing..."):
            app = build_workflow()
            start = time.time()
            final_state = app.invoke({"question": question.strip()})
            elapsed = time.time() - start

        answer = final_state.get("answer", "No answer generated.")

        st.subheader("📚 Agent Answer")
        st.markdown(answer)

        # Show intermediate steps in an expander
        with st.expander("Show planning and raw research data"):
            st.markdown("**Planner steps**")
            st.code(final_state.get("planner_steps", ""), language="markdown")

            st.markdown("**Raw research results**")
            st.json(final_state.get("research_results", []))

        # Evaluate and show simple metrics
        eval_result = evaluate_response(question, answer, elapsed)

        st.subheader("📊 Response Metrics (1–10,000)")
        cols = st.columns(5)
        cols[0].metric("Accuracy", eval_result.accuracy)
        cols[1].metric("Research quality", eval_result.research_quality)
        cols[2].metric("Speed", eval_result.speed)
        cols[3].metric("Usefulness", eval_result.usefulness)
        cols[4].metric("Overall", eval_result.overall)

        st.caption(f"Response time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()

