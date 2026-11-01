#!/usr/bin/env python3
"""
scripts/verify_dpg_urls.py
==========================
Automated health-check and verification script for the Vetted Resilient Solutions Directory.

Capabilities:
1. Pings all registered URLs with browser-realistic headers.
2. Follows redirects and detects permanent 301 domain shifts.
3. Performs content-signature verification to ensure domains are not parked or squatted.
4. Updates data/resources_registry.json with verified status, HTTP code, latency, and real timestamp.
5. Generates a structured markdown verification audit report.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'resources_registry.json')
REPORT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'last_link_verification_report.md')

PARKED_DOMAIN_INDICATORS = [
    "domain for sale",
    "buy this domain",
    "parked domain",
    "hugedomains",
    "godaddy parked",
    "namecheap parking",
    "under construction"
]

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def check_url(url, signature_keywords=None, timeout=12):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    req = urllib.request.Request(url, headers=headers)
    ctx = create_ssl_context()
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            latency_ms = int((time.time() - start_time) * 1000)
            status_code = response.status
            final_url = response.url
            
            # Read first 128KB of page to check signature / parking
            html_snippet = response.read(131072).decode('utf-8', errors='ignore').lower()
            
            # Check for domain squatter / parking indicators
            is_parked = any(indicator in html_snippet for indicator in PARKED_DOMAIN_INDICATORS)
            
            # Check for signature keywords if provided
            signature_matched = True
            if signature_keywords:
                signature_matched = any(kw.lower() in html_snippet for kw in signature_keywords)
            
            is_healthy = (status_code == 200) and not is_parked and signature_matched
            
            warning = None
            if is_parked:
                warning = "Warning: Page text matched domain parking keywords."
            elif not signature_matched and signature_keywords:
                warning = f"Warning: Content did not contain expected signature keywords ({signature_keywords})."
            elif final_url.rstrip('/') != url.rstrip('/'):
                warning = f"Notice: Permanent redirect to {final_url}"

            return {
                "accessible": is_healthy,
                "status_code": status_code,
                "latency_ms": latency_ms,
                "final_url": final_url,
                "redirected": (final_url.rstrip('/') != url.rstrip('/')),
                "warning": warning,
                "error": None
            }
    except urllib.error.HTTPError as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "accessible": False,
            "status_code": e.code,
            "latency_ms": latency_ms,
            "final_url": url,
            "redirected": False,
            "warning": None,
            "error": f"HTTP Error {e.code}: {e.reason}"
        }
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "accessible": False,
            "status_code": 0,
            "latency_ms": latency_ms,
            "final_url": url,
            "redirected": False,
            "warning": None,
            "error": str(e)
        }

def run_verification():
    if not os.path.exists(REGISTRY_PATH):
        print(f"Registry not found at {REGISTRY_PATH}")
        sys.exit(1)

    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Starting verification of {len(registry)} educational resources on {today_str}...\n")

    results = []
    has_failures = False

    for item in registry:
        name = item.get("title")
        url = item.get("url")
        sig_kw = item.get("signature_keywords", [])
        
        print(f"Testing [{item.get('id')}]: {name} -> {url}")
        res = check_url(url, signature_keywords=sig_kw)
        
        # Update registry item
        item["last_verified_date"] = today_str
        item["http_status"] = res["status_code"]
        item["latency_ms"] = res["latency_ms"]
        item["status"] = "active" if res["accessible"] else "degraded"
        
        if res["warning"]:
            item["verification_note"] = res["warning"]
        elif res["error"]:
            item["verification_note"] = res["error"]
            has_failures = True
        else:
            item["verification_note"] = "Fully verified active."

        if res["redirected"] and res["accessible"]:
            item["suggested_canonical_url"] = res["final_url"]

        results.append({
            "item": item,
            "check": res
        })
        print(f"  -> Status {res['status_code']} ({res['latency_ms']}ms) - Active: {res['accessible']}\n")

    # Save updated registry
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"Updated registry saved to {REGISTRY_PATH}")

    # Generate Markdown Report
    report_lines = [
        f"# Automated Resource Verification Audit Report",
        f"**Run Timestamp:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}",
        f"**Total Resources Tested:** {len(registry)}",
        f"**All Healthy:** {'YES' if not has_failures else 'NO - Action Required'}\n",
        f"| Resource | Scope | URL | HTTP Status | Latency | Health Status | Notes |",
        f"| :--- | :--- | :--- | :---: | :---: | :---: | :--- |"
    ]

    for r in results:
        it = r["item"]
        ch = r["check"]
        status_icon = "🟢 Active" if ch["accessible"] else "🔴 Failed"
        notes = ch["warning"] or ch["error"] or "Verified OK"
        report_lines.append(
            f"| **{it['title']}** | {it.get('scope', 'Global')} | [`{it['url']}`]({it['url']}) | `{ch['status_code']}` | `{ch['latency_ms']}ms` | {status_icon} | {notes} |"
        )

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines) + '\n')
    print(f"Audit report generated at {REPORT_PATH}\n")

    return not has_failures

if __name__ == '__main__':
    success = run_verification()
    sys.exit(0 if success else 1)
