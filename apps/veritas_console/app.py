import os, time, requests, streamlit as st
API=os.getenv("API_BASE","http://localhost:8080")
st.set_page_config(page_title="Veritas Runner", layout="wide")
st.title("Veritas Nexus — Phase 1")

with st.form("run"):
    channel = st.text_input("YouTube channel URL", "https://youtube.com/@imaginationpodcastofficial")
    max_items = st.number_input("Oldest N", 1, 20, 10)
    submitted = st.form_submit_button("Start")
    if submitted:
        payload={"target":channel,"connectors":["youtube"],"max_items":int(max_items),"gates":{"budget_usd_per_run":0.0},"order":"oldest"}
        r = requests.post(f"{API}/jobs", json=payload, timeout=10); r.raise_for_status()
        st.session_state["job_id"] = r.json()["job_id"]

job = st.session_state.get("job_id")
if job:
    st.subheader(f"Job: {job}")
    ph=st.empty()
    while True:
        s = requests.get(f"{API}/jobs/{job}", timeout=10).json()
        ph.json(s)
        if s["state"] in ("done","error"): break
        time.sleep(1.0)
    if s["state"]=="done":
        res = requests.get(f"{API}/jobs/{job}/results", timeout=10).json()
        st.subheader("Results"); st.json(res)

