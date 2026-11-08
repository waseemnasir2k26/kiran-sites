#!/usr/bin/env python3
"""Local preview. Usage: python scripts/preview.py <client>  (needs config/local.json, gitignored)"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    print("usage: preview.py <client>"); sys.exit(1)
cfg = ROOT / "config" / "local.json"
if not cfg.exists():
    print("ERROR: config/local.json not found (it is gitignored, so a fresh checkout does not have it)")
    sys.exit(1)
c = json.loads(cfg.read_text(encoding="utf-8"))
page = ROOT / "sites" / sys.argv[1] / "index.html"
if not page.exists():
    print("ERROR: no page for %s" % sys.argv[1]); sys.exit(1)
print("Preview OK: %s at http://localhost:%d/ (analytics %s)" % (sys.argv[1], c["preview_port"], c["analytics_id"]))
