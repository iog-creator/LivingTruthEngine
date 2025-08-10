import os, redis, structlog
from tasks import run_job

log = structlog.get_logger(__name__)
r = redis.from_url(os.getenv("REDIS_URL","redis://living-truth-redis:6379/0"))

if __name__ == "__main__":
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(20))
    log.info("worker.start")
    while True:
        item = r.brpop("veritas:jobs", timeout=5)
        if not item: continue
        _, job_id = item
        job_id = job_id.decode()
        try:
            run_job(job_id)
        except Exception as e:
            log.error("job.fail", job_id=job_id, err=str(e))

