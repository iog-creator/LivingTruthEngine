import os, json, time, re, requests, pathlib
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi as YT
from api import store

DATA = Path(os.getenv("DATA_ROOT","/app/data"))
RUNS = Path(os.getenv("RUNS_ROOT","/app/runs"))

def _yt_latest_10_oldest(channel_url:str)->list[str]:
    # Simple scraping of RSS (uploads) or yt-dlp json would be better; MVP: instruct user to provide 10 IDs later.
    # For now, return empty; user can replace with actual fetch in Phase 2.
    return []

def _transcript(video_id:str):
    try:
        tr = YT.get_transcript(video_id)
        return tr
    except Exception:
        return []

def _canonicalize(items:list[dict], out_path:Path):
    with open(out_path, "w", encoding="utf-8") as f:
        for it in items:
            line = {"doc_id": it["id"], "url": it["url"], "created_at": it.get("created_at"), "sentences":[{"text": it["text"]}]}
            f.write(json.dumps(line)+"\n")

def _provenance(in_jsonl:Path, out_jsonl:Path):
    from hashlib import sha256
    def h(s): return sha256(s.encode()).hexdigest()
    import math
    lines=[]
    for line in open(in_jsonl,"r",encoding="utf-8"):
        d=json.loads(line)
        hs=[h(s["text"]) for s in d["sentences"]]
        # simple merkle
        layer=hs[:]
        if not layer: root=h("")
        else:
            while len(layer)>1:
                if len(layer)%2==1: layer.append(layer[-1])
                layer=[h(layer[i]+layer[i+1]) for i in range(0,len(layer),2)]
            root=layer[0]
        d["prov"]={"sentence_hashes":hs,"merkle_root":root}
        lines.append(d)
    open(out_jsonl,"w",encoding="utf-8").write("\n".join(json.dumps(x) for x in lines))

def run_job(job_id: str):
    req = json.loads((RUNS/job_id/"request.json").read_text())
    store.update_status(job_id, {"state":"running","stage":"discover","progress":0.05})

    # 1) YouTube oldest 10 — placeholder: require user to supply IDs Phase 1 test
    vids = req.get("video_ids") or []
    items=[]
    for vid in vids:
        url=f"https://www.youtube.com/watch?v={vid}"
        tr=_transcript(vid)
        for seg in tr:
            if not seg.get("text"): continue
            items.append({"id": f"{vid}-{int(seg['start']*1000)}", "url": url, "text": seg["text"].strip()})

    # 2) TODO web/pdf crawl from descriptions (Phase 1 minimal)

    store.update_status(job_id, {"state":"running","stage":"canonicalize","progress":0.3})
    canon = RUNS/job_id/"corpus.jsonl"
    _canonicalize(items, canon)

    store.update_status(job_id, {"state":"running","stage":"provenance","progress":0.5})
    prov = RUNS/job_id/"corpus_prov.jsonl"
    _provenance(canon, prov)

    # 3) Retrieval→Rerank→Validate (Phase 1: stub results)
    store.update_status(job_id, {"state":"running","stage":"analyze","progress":0.8})
    results = {"claims": [], "fracture_score": 0.0, "unity_bridges": [], "run_folder": str(RUNS/job_id)}
    store.write_results(job_id, results)

    store.update_status(job_id, {"state":"done","stage":"done","progress":1.0})
