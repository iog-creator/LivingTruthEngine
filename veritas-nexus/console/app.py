import os, time, json, requests, streamlit as st
API=os.getenv("API_BASE","http://api:8080")
st.set_page_config(page_title="Veritas Nexus", layout="wide")
st.title("Veritas Nexus — Phase 1 Runner")

with st.form("run"):
    channel = st.text_input("YouTube channel URL", "https://youtube.com/@imaginationpodcastofficial")
    video_ids = st.text_area("Video IDs (comma-separated; Phase 1)", "")
    submitted = st.form_submit_button("Start")
    if submitted:
        vids = [v.strip() for v in video_ids.split(",") if v.strip()]
        payload = {"target": channel, "connectors":["youtube","web","pdf"], "max_items": 10, "crawl_depth": 1, "gates": {"budget_usd_per_run": 0.0}, "video_ids": vids}
        r = requests.post(f"{API}/jobs", json=payload)
        st.session_state["job_id"]=r.json()["job_id"]

job_id = st.session_state.get("job_id")
if job_id:
    st.subheader(f"Job: {job_id}")
    ph = st.empty()
    while True:
        s = requests.get(f"{API}/jobs/{job_id}").json()
        ph.json(s)
        if s["state"] in ("done","error"): break
        time.sleep(1.0)
    if s["state"]=="done":
        res = requests.get(f"{API}/jobs/{job_id}/results").json()
        st.subheader("Results")
        st.json(res)
