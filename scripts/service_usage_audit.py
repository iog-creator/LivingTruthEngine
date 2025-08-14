#!/usr/bin/env python
import json, os, glob, yaml, sys, re

CORE = {"dashboard","postgres","mcp-solver","redis","living-truth-engine"}  # 9.5.7 required set

compose = yaml.safe_load(open("docker/docker-compose.yml"))
svcs = set((compose.get("services") or {}).keys())

missing = sorted(list(CORE - svcs))
if missing:
    print(f"ERROR: required services missing from compose: {missing}")
    sys.exit(1)

# health URLs/commands via compose healthcheck (our convention)
bad = []
for name in CORE:
    healthcheck = compose["services"][name].get("healthcheck")
    if not healthcheck:
        bad.append(name)

if bad:
    print(f"ERROR: missing healthcheck for: {bad}")
    sys.exit(1)

print("Service usage audit: PASS (core present with healthcheck).")
