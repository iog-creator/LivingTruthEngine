## Summary
(what changed + why)

## SSOT & Health
**Note**: SSOT refers to Single Source of Truth - the core documentation system that ensures project consistency.
- [ ] Ran `python scripts/verify_ssot_bundle.py` and it **passed**
- [ ] No SSOT duplicates under `docs/` or `archive/docs/`
- [ ] `SERVICES_MANIFEST.md` has Role / Ports / Environment / Healthcheck / Code Paths / Tests
- [ ] Commit message includes **[SSOT Verified]**

## Tests & CI
- [ ] Playwright/UI tests updated (if UI touched) and green locally
- [ ] Repo Health/SSOT guards are green on CI
