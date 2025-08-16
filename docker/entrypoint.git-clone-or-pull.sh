#!/usr/bin/env sh
set -e
# Idempotent: if REPO_URL is set, keep REPO_DIR in sync with REPO_BRANCH.
# Does nothing if REPO_URL is empty or unset.
REPO_URL="${REPO_URL:-}"
REPO_BRANCH="${REPO_BRANCH:-main}"
REPO_DIR="${REPO_DIR:-/opt/repo}"
if [ -n "$REPO_URL" ]; then
  mkdir -p "$REPO_DIR"
  if [ -d "$REPO_DIR/.git" ]; then
    git -C "$REPO_DIR" fetch --all --tags --prune
    git -C "$REPO_DIR" checkout "$REPO_BRANCH"
    git -C "$REPO_DIR" reset --hard "origin/$REPO_BRANCH"
  else
    # Ensure empty dir before first clone (avoid 'already exists' issues).
    rm -rf "$REPO_DIR"/* "$REPO_DIR"/.[!.]* "$REPO_DIR"/..?* 2>/dev/null || true
    git clone --depth=1 -b "$REPO_BRANCH" "$REPO_URL" "$REPO_DIR"
  fi
fi
exec "$@"
