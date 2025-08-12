from fastapi import APIRouter

router = APIRouter()

# canonical envelope specimen the UI validates against
CONTRACT = {
  "envelope": {"status": "ok", "data": {}, "error": None},
  "endpoints": {
    "/api/health": {"status": "ok", "data": {"service": "unified_dashboard"}},
    "/api/health/full": {"status": "ok", "data": {"service": "unified_dashboard", "gates": {}, "all_gates_passed": True}},
    "/api/runs": {"status": "ok", "data": [{"run_id": "string"}]},
    "/api/analyze/summary": {"status": "ok", "data": {"summary": "string"}},
    "/api/analyze/claims": {"status": "ok", "data": {"claims": []}},
    "/api/tools": {"status": "ok", "data": {"categories": {}}}
  }
}

@router.get("/api/contract")
def get_contract():
    return {"status": "ok", "data": CONTRACT, "error": None}
