"""UI shell (the 'skin' comes later). Reads outputs/results.json only - read-only by design.
Run: pip install streamlit pyyaml && python run_demo.py && streamlit run app/streamlit_app.py"""
import json
from pathlib import Path
import streamlit as st

R = json.load(open(Path(__file__).resolve().parents[1] / "outputs/results.json"))
st.set_page_config(page_title="Demo Group risk view", layout="wide")
st.title("Demo Group: bank-wide credit risk view")
st.caption("SYNTHETIC data, ASSUMED limits and scenarios, ILLUSTRATIVE grade. Not a validated model.")
t1, t2, t3, t4, t5, t6 = st.tabs(["Answer sheet", "Findings", "Decisions", "Stress", "Ask", "Not implemented"])
with t1:
    st.dataframe(R["acceptance"], use_container_width=True)
with t2:
    st.dataframe([{k: f.get(k) for k in ("finding_id", "type", "entity_id", "owner", "status", "evidence_id")} for f in R["findings"]])
with t3:
    st.bar_chart(R["decisions"])
with t4:
    st.bar_chart({k: v["total"]["expected_loss"] for k, v in R["stress"].items()})
with t5:
    for q in R["qa"]:
        with st.expander(q["question"]):
            st.write(q["answer"]); st.caption(f"{q['statement_type']} | evidence: {', '.join(q['evidence_ids']) or 'none'}")
with t6:
    st.dataframe(R["risk_register"])
