"""Local dev server for the paper reading site.

Usage:
    python scripts/serve.py [--port PORT]

Serves site/ directory. Runs build_site.py first if papers.json is missing.
"""

import http.server
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"

PORT = 8080

# Parse --port
for i, arg in enumerate(sys.argv[1:], 1):
    if arg == "--port" and i + 1 < len(sys.argv):
        PORT = int(sys.argv[i + 1])

# Auto-build if papers.json missing
if not (SITE_DIR / "papers.json").exists():
    print("papers.json not found, running build_site.py...")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")], check=True)

os.chdir(SITE_DIR)

handler = http.server.SimpleHTTPRequestHandler
handler.extensions_map.update({".json": "application/json", ".woff2": "font/woff2"})

print(f"Serving {SITE_DIR} at http://localhost:{PORT}")
with http.server.HTTPServer(("", PORT), handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
