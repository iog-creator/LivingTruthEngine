# PHASE_9_4_0_PLAN.md — DevOps Cutover Skeleton (Single Origin)

## 🎯 Objectives
1) Serve everything from a **single origin**:
   - `/api/**` → FastAPI (port :8050, existing server)
   - `/` (all non-`/api`) → **new UI shell** (static SPA placeholder now; real UI later)
2) Put a thin **reverse proxy** in front (Caddy or Nginx) for clean routing, compression, and HSTS.
3) Decouple old Dash templates from app startup; keep API unchanged.
4) Provide **smoke + tests** to validate the cutover and envelope guarantees.
5) Prepare for **Phase 9.5.0 Real Adapters** and the **UI rebuild** to plug in cleanly.

---

## 🏗 Architecture (after cutover)

```
Browser ──▶ :80/443 reverse proxy (Caddy/Nginx)
├── /api/**  ──▶ http://api:8050 (FastAPI: existing endpoints)
└── /*       ──▶ http://ui:4173  (static SPA shell)
```

- We keep `unified_dashboard.py` running FastAPI on **:8050** strictly for APIs.
- New **UI shell** is a minimal, production‑built static site (Vite/React placeholder) served by a tiny HTTP server (or `vite preview`) on **:4173**.
- Reverse proxy terminates TLS (later) and routes paths.

---

## 🔩 Changes (files to add/modify)

### 1) Reverse proxy (choose one; default **Caddy**)

**`deploy/Caddyfile` (new)**
```caddy
:80 {
  @api path /api/* /docs /openapi.json
  handle @api {
    reverse_proxy api:8050
  }

  handle {
    reverse_proxy ui:4173
  }

  encode zstd gzip
  header {
    # tighten later; keep skeleton permissive for local
    Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" {env.HSTS?0}
  }

  log {
    output stdout
    format console
    level INFO
  }
}
```

**Docker alternative (Nginx)**: if you prefer Nginx, drop `deploy/nginx.conf` with similar `location /api/` → `api:8050`, `location /` → `ui:4173`.

---

### 2) UI shell (static, minimal – replace later with real UI)

**`ui/` (new)**

* `package.json` (scripts: `dev`, `build`, `preview`)
* `index.html`, `src/main.tsx`, `src/App.tsx`
* The shell calls **no real APIs yet**; it just proves routing, error screen, and a placeholder "Graph" link.

**`ui/package.json` (new)**

```json
{
  "name": "lte-ui-shell",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview --port 4173 --strictPort"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vite": "^5.4.0",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.4.0"
  }
}
```

**`ui/index.html` (new)**

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Living Truth Engine</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**`ui/src/main.tsx` (new)**

```ts
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")!).render(<App />);
```

**`ui/src/App.tsx` (new)**

```tsx
import React from "react";

export default function App() {
  return (
    <div style={{fontFamily:"system-ui, sans-serif", padding: 24}}>
      <h1>Living Truth Engine</h1>
      <p>Phase 9.4.0 UI Shell (placeholder). Static app served behind single origin.</p>
      <ul>
        <li><a href="/api/health" target="_blank" rel="noreferrer">/api/health</a></li>
        <li><a href="/api/health/full" target="_blank" rel="noreferrer">/api/health/full</a></li>
        <li><a href="/api/models" target="_blank" rel="noreferrer">/api/models</a></li>
      </ul>
      <p>Graph and analysis pages will be plugged in during the UI rebuild phase.</p>
    </div>
  );
}
```

---

### 3) API service hardening (no UI coupling)

**`src/dashboard/unified_dashboard.py` (modify minimally)**

* Ensure startup does **not** require Dash/Jinja templates.
* Keep FastAPI + routers only.
* Confirm `/api/**` unchanged and envelope consistent.

*No template edits here; legacy HTML stays but is no longer served from root.*

---

### 4) Docker Compose (wire services)

**`docker/compose.v2.yml` (new or modify existing)**
(Use service names `api`, `ui`, `proxy`)

```yaml
version: "3.9"
services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    environment:
      - PORT=8050
    expose:
      - "8050"
    # depends_on: [db, redis, ...]  # existing deps
  ui:
    working_dir: /app/ui
    image: node:20-alpine
    command: sh -c "npm ci && npm run build && npm run preview"
    volumes:
      - ./:/app
    expose:
      - "4173"
  proxy:
    image: caddy:2.7
    ports:
      - "80:80"
    volumes:
      - ./deploy/Caddyfile:/etc/caddy/Caddyfile:ro
    depends_on:
      - api
      - ui
```

> If you don't use Docker locally, you can run `ui` via `npm run preview` and run `caddy run --config deploy/Caddyfile` directly.

---

### 5) Env / config

* No new mandatory envs.
* Optional: `HSTS=1` later in prod to enforce strict transport security via Caddy header.

---

## 🧪 Tests & Smoke

**`scripts/p9_4_0_smoke.sh` (new)**

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "== Phase 9.4.0 Smoke =="
# 1) Root serves UI shell (HTML)
curl -sS http://localhost/ | grep -qi "Living Truth Engine" && echo "UI shell OK"

# 2) API routes still reachable via same origin
for ep in /api/health /api/health/full /api/models; do
  status=$(curl -sS "http://localhost${ep}" | jq -r .status || true)
  test "$status" = "ok" && echo "API $ep OK" || (echo "API $ep FAILED"; exit 1)
done

echo "All good."
```

**`tests/test_phase_9_4_0_routing.py` (new)**

```python
import requests as r

BASE = "http://localhost"

def test_ui_shell_root():
    html = r.get(f"{BASE}/").text
    assert "Living Truth Engine" in html

def test_api_health_ok():
    j = r.get(f"{BASE}/api/health").json()
    assert j["status"] == "ok"

def test_api_models_ok():
    j = r.get(f"{BASE}/api/models").json()
    assert j["status"] == "ok"
    assert "data" in j
```

---

## ✅ Acceptance Criteria

* Reverse proxy routes `/api/**` to FastAPI (:8050) and everything else to UI shell (:4173).
* Hitting `http://localhost/` serves the shell HTML with "Living Truth Engine".
* `http://localhost/api/health`, `/api/health/full`, `/api/models` return `{status:"ok", ...}`.
* `scripts/p9_4_0_smoke.sh` passes locally (non‑Docker or Docker).
* No regression to API envelope or error‑code policy.
* Legacy server no longer auto‑mounts or serves legacy HTML at `/`.

---

## 🧭 Notes / Rationale

* This phase **unblocks the UI rebuild** by giving us a stable single‑origin envelope with clean path routing. The current 8050 "dashboard" coupling is what caused inconsistent UI edits; we remove that risk.
* We keep the **API contract stable** (no churn for 9.5).
* The placeholder UI is deliberately minimal—only to validate wiring. The real UI (new stack) lands in the UI rebuild phase on top of this skeleton.

---

## 🧾 Completion Summary Instructions

Create `PHASE_9_4_0_COMPLETION_SUMMARY.md` after merge, including:

* Reverse proxy config (Caddyfile or Nginx) and route map.
* Smoke output + `pytest` results.
* Confirmation that `/` is static shell, `/api/**` unchanged.
* Any deployment notes (Docker and local).

Commit message:

```
phase9.4.0: single-origin devops cutover skeleton [api stable]
```
