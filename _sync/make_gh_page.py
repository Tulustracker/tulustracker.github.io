"""Build the GitHub Pages copy of TULUS TRACKER from the published artifact page.
Only the pemaju view can run there (no Claude runtime), and the page carries only the PIN-locked pemaju data."""
import re, sys, json
src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()
css = re.search(r'<style id="css">(.*?)</style>', h, re.S).group(1)
pub = re.search(r'<script id="pub" type="application/json">(.*?)</script>', h, re.S).group(1)
main = re.search(r'<script id="main">(.*?)</script>', h, re.S).group(1)
d = json.loads(pub)
if not (isinstance(d, dict) and isinstance(d.get('b'), list) and d['b'] and isinstance(d.get('salt'), str) and int(d.get('it', 0)) >= 100000):
    sys.exit('Data pemaju tiada atau tidak sah: laman GitHub tidak diubah.')
if '<script' in pub.lower():
    sys.exit('Data pemaju mengandungi kandungan tidak dijangka: laman GitHub tidak diubah.')
csp = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'"
fav = "data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M3 17a13 11 0 0 1 26 0z' fill='%23f8c010'/%3E%3Crect x='15' y='16' width='2.4' height='14' fill='%2314584a'/%3E%3C/svg%3E"
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<meta http-equiv="Content-Security-Policy" content="{csp}">'
        '<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">'
        '<title>TULUS TRACKER</title>'
        '<meta name="description" content="Penjejak proses perumahan sektor awam">'
        f'<link rel="icon" href="{fav}">'
        f'<style id="css">{css}</style></head><body>'
        '<div id="app"><noscript><p style="padding:24px;text-align:center">Sila hidupkan JavaScript.</p></noscript></div>'
        '<div id="sheet" class="sheet" hidden></div><div id="toast" role="status" aria-live="polite"></div>'
        f'<script id="pub" type="application/json">{pub}</script>'
        f'<script id="main">{main}</script></body></html>\n')
open(out, 'w', encoding='utf-8').write(page)
print('built', out, len(page), 'bytes; pemaju blobs:', len(d.get('b', [])))
