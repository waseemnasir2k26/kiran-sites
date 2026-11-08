#!/usr/bin/env python3
"""Deterministic site checker. Usage: python scripts/check-site.py <client>"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "+92 300 0000000"

def section(html, sid):
    m = re.search(r'<section id="%s">(.*?)</section>' % sid, html, re.S)
    return m.group(1) if m else ""

def items(block):
    return [re.sub(r"<[^>]+>", "", li).strip() for li in re.findall(r"<li>(.*?)</li>", block, re.S)]

def main():
    if len(sys.argv) != 2:
        print("usage: check-site.py <client>"); return 1
    client = sys.argv[1]
    page = ROOT / "sites" / client / "index.html"
    data_f = ROOT / "data" / (client + ".json")
    if not page.exists() or not data_f.exists():
        print("FAIL setup: missing %s or %s" % (page.relative_to(ROOT), data_f.relative_to(ROOT))); return 1
    html = page.read_text(encoding="utf-8")
    data = json.loads(data_f.read_text(encoding="utf-8"))
    results = []

    hours = dict(i.split(": ", 1) for i in items(section(html, "hours")) if ": " in i)
    results.append(("hours", hours == data["hours"], "match" if hours == data["hours"] else "page %s vs data %s" % (hours, data["hours"])))

    prices_html = section(html, "prices")
    prices = []
    for i in items(prices_html):
        m = re.match(r"(.+?): PKR (\d+)$", i)
        if m:
            prices.append({"item": m.group(1), "pkr": int(m.group(2))})
    diff = [ "%s: page %s, data %s" % (d["item"], next((p["pkr"] for p in prices if p["item"] == d["item"]), "missing"), d["pkr"])
             for d in data["prices"] if d not in prices ]
    extra = [p["item"] for p in prices if p["item"] not in [d["item"] for d in data["prices"]]]
    detail = "; ".join(diff + ["extra item %s" % e for e in extra]) or "match"
    results.append(("prices", not diff and not extra and len(prices) == len(data["prices"]), detail))

    want = re.sub(r"\D", "", PLACEHOLDER)
    found = re.findall(r"(?:\+|wa\.me/|tel:)\s*(\d[\d \-]{8,14}\d)", html) + re.findall(r"\b0\d{3}[ -]?\d{7}\b", html)
    bad = [f for f in found if re.sub(r"\D", "", f) != want]
    results.append(("phone", bool(found) and not bad and data["phone"] == PLACEHOLDER,
                    "only placeholder" if found and not bad else "found %s" % (bad or "no phone")))

    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", html)
    results.append(("no email", not emails, "none" if not emails else "found %d" % len(emails)))

    vp = bool(re.search(r'<meta name="viewport"', html))
    results.append(("viewport meta", vp, "present" if vp else "missing"))

    text = re.sub(r"<[^>]+>", " ", prices_html)
    m = re.search(r"Prices checked: (\S+)", text)
    pc_ok = bool(m) and m.group(1) == data["updated"]
    results.append(("prices checked", pc_ok,
                    "Prices checked: %s" % data["updated"] if pc_ok else
                    "price section needs 'Prices checked: %s' (found %s)" % (data["updated"], m.group(1) if m else "none")))

    failed = 0
    for name, ok, det in results:
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, det))
        failed += 0 if ok else 1
    print("%s %s (%d/%d checks passed)" % (client, "PASS" if not failed else "FAIL", len(results) - failed, len(results)))
    return 0 if not failed else 1

sys.exit(main())
