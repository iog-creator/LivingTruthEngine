from __future__ import annotations

import os, json, subprocess, structlog
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi as YT

log = structlog.get_logger(__name__)
RUNS = Path(os.getenv("RUNS_ROOT","/app/data/runs"))


def _yt_oldest_ids(channel_url:str, limit:int=10)->list[str]:
    try:
        out = subprocess.check_output(["yt-dlp","-J","--flat-playlist",channel_url], stderr=subprocess.STDOUT, timeout=60)
        info = json.loads(out.decode("utf-8", errors="ignore"))
        entries = info.get("entries", [])
        vids=[]
        for e in entries:
            vid=(e.get("id") or "").strip()
            up=(e.get("upload_date") or "")
            if vid: vids.append((up,vid))
        vids.sort(key=lambda x: x[0] or "")
        return [v for _,v in vids[:limit]]
    except Exception as e:
        log.error("ytdlp.error", err=str(e))
        return []


def _transcript(video_id:str):
    try:
        return YT.get_transcript(video_id), None
    except Exception as e:
        return [], str(e)


def _canonicalize(items:list[dict], out_path:Path):
    with open(out_path, "w", encoding="utf-8") as f:
        for it in items:
            rec = {
                "doc_id": it["id"],
                "url": it["url"],
                "sentences":[{"text": it["text"]}],
                "meta": it.get("meta",{})
            }
            f.write(json.dumps(rec)+"\n")


def _provenance(in_path:Path, out_path:Path):
    import hashlib
    def h(s: str) -> str:
        return hashlib.sha256(s.encode()).hexdigest()
    out: list[dict] = []
    for line in open(in_path,"r",encoding="utf-8"):
        d=json.loads(line)
        hs=[h(s["text"]) for s in d["sentences"]]
        layer=hs[:]
        if not layer:
            root=h("")
        else:
            while len(layer)>1:
                if len(layer)%2==1: layer.append(layer[-1])
                layer=[h(layer[i]+layer[i+1]) for i in range(0,len(layer),2)]
            root=layer[0]
        d["prov"]={"sentence_hashes":hs,"merkle_root":root}
        out.append(d)
    open(out_path,"w",encoding="utf-8").write("\n".join(json.dumps(x) for x in out))


def run_job(job_id:str):
    req = json.loads((RUNS/job_id/"request.json").read_text())
    def upd(state: str, stage: str, prog: float, **kw):
        (RUNS/job_id/"status.json").write_text(json.dumps({"state":state,"stage":stage,"progress":prog} | (kw.get("extra") or {})), encoding="utf-8")

    upd("running","discover",0.05)
    channel=req.get("target","")
    limit=int(req.get("max_items",10))
    vids = req.get("video_ids") or _yt_oldest_ids(channel, limit)
    if not vids:
        upd("error","discover",0.1, extra={"message":"No videos found"})
        return

    items: list[dict] = []
    missing: list[dict] = []
    for vid in vids:
        url=f"https://www.youtube.com/watch?v={vid}"
        tr, err = _transcript(vid)
        if err:
            missing.append({"video_id":vid,"error":err}); continue
        for seg in tr:
            t=(seg.get("text") or "").strip()
            if not t: continue
            items.append({"id": f"{vid}-{int(seg['start']*1000)}","url": url,"text": t, "meta":{"video_id":vid,"timestamp_ms": int(seg["start"]*1000)}})

    upd("running","canonicalize",0.35, extra={"metrics":{"videos":len(vids),"segments":len(items),"missing":len(missing)}})
    canon = RUNS/job_id/"corpus.jsonl"; _canonicalize(items, canon)

    upd("running","provenance",0.55)
    prov = RUNS/job_id/"corpus_prov.jsonl"; _provenance(canon, prov)

    upd("running","analyze",0.8)
    results={"claims":[],"fracture_score":0.0,"unity_bridges":[],"run_folder": str(RUNS/job_id)}
    if missing: results["notes"]={"missing_transcripts": missing}
    (RUNS/job_id/"results.json").write_text(json.dumps(results), encoding="utf-8")

    upd("done","done",1.0)

