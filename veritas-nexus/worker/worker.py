import os, redis, time
from tasks import run_job

r = redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"))

if __name__ == "__main__":
    while True:
        item = r.brpop("veritas:jobs", timeout=5)
        if not item: continue
        _, job_id = item
        job_id = job_id.decode()
        try:
            run_job(job_id)
        except Exception as e:
            print("Job failed", job_id, e)
