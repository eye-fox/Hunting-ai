---
name: browser-local
description: >-
  Local Chromium CDP automation — 100% browser-use CLI compatible.
  No cloud, no Playwright, no Puppeteer.
  Chrome DevTools Protocol langsung ke Chromium lokal dengan stealth anti-deteksi.
  Support: open, eval, screenshot, state, elements, click, type, input, scroll,
    back, tab, keys, hover, cookies, wait, solve (Turnstile), upload, select,
    intercept (dual engine: JS override + CDP Fetch domain — intercept form POST navigation),
    history, sitemap, repeater, collaborator, scope, intruder, matchreplace, compare.
license: MIT
compatibility: opencode
metadata:
  category: browser-automation
  technique: cdp-local
---

# Browser Local — Chromium via CDP

Browser automation lokal 100% gratis, tanpa cloud, tanpa Playwright, tanpa Puppeteer. Langsung ke Chromium via Chrome DevTools Protocol (CDP). CLI 100% kompatibel dengan `browser-use`.

**Tool di `/usr/local/bin/browser-local`**, Chromium di `/usr/bin/chromium`.

---

## Global Flags

```bash
# Default = FAST mode. Click langsung, input via eval (satu shot).
# Tambahkan --human untuk mode stealth (mouse easing, per-char typing, delays).
browser-local --cdp-url <URL> --session s1 <command>

--human     # Mode stealth: mouse easing, per-char typing, delays (manual flag — jika di-set, ON terus)
--json      # Output JSON
```

> **Global flags (`--cdp-url`, `--session`, `--json`, `--human`) bisa ditempatkan di mana saja — sebelum atau sesudah command. Urutan tidak penting.**

Contoh:
```bash
# Semua format ini valid:
browser-local --cdp-url ws://... --session s1 open "https://example.com"
browser-local open "https://example.com" --cdp-url ws://... --session s1
browser-local --session s1 open "https://example.com" --cdp-url ws://...
```

---

## 1. Quick Start

```bash
# Start browser
browser-local start --port=9222

# Output: ws://127.0.0.1:9222/devtools/browser/...
# Simpan CDP URL untuk command berikutnya
```

Atau tanpa port (otomatis pilih port kosong):
```bash
browser-local start
# Output: ws://127.0.0.1:38339/devtools/browser/...
```

Dengan opsi tambahan:
```bash
browser-local start --port=9222 --width=1920 --height=1080 --tz=Asia/Jakarta --locale=id-ID
browser-local start --proxy-server="http://user:pass@host:8080"
browser-local start --profile="work"   # Profile Chromium spesifik
```

---

## 2. Commands

### Start Browser
```bash
browser-local start --port=9222
browser-local start --port=0                          # Port otomatis
browser-local start --width=1920 --height=1080
browser-local start --tz="Asia/Jakarta" --locale="id-ID"
browser-local start --profile="work"
browser-local start --proxy-server="http://user:pass@host:8080"
# Semua flag start bisa dikombinasikan:
browser-local start --port=9222 --tz="Asia/Jakarta"
```

### Navigasi
```bash
browser-local --cdp-url <URL> --session s1 open "https://example.com"
browser-local --cdp-url <URL> --session s1 open "https://example.com" --wait-cf               # Tunggu Cloudflare JS challenge selesai
browser-local --cdp-url <URL> --session s1 open "https://example.com" --wait-cf --cf-timeout=60  # Timeout kustom (default 30s)
browser-local --cdp-url <URL> --session s1 open "https://example.com" --scope                    # Cek scope dulu
```

### State
```bash
browser-local --cdp-url <URL> --session s1 state
# atau JSON
browser-local --cdp-url <URL> --session s1 --json state
```

### Elements (Daftar Interaktif)
```bash
browser-local --cdp-url <URL> --session s1 elements
# Output: JSON array of {index, tag, type, text, rect, ...}
```

### JavaScript
```bash
browser-local --cdp-url <URL> --session s1 eval 'document.title'
browser-local --cdp-url <URL> --session s1 eval 'JSON.stringify({url:location.href,title:document.title})'
```

### Screenshot (optional — hanya jika saya minta)
```bash
browser-local --cdp-url <URL> --session s1 screenshot /tmp/ss.png
browser-local --cdp-url <URL> --session s1 screenshot --full /tmp/full.png
```

### Klik (FAST default — langsung mousePressed tanpa easing)
```bash
# By index (dari elements)
browser-local --cdp-url <URL> --session s1 click 0
# By koordinat
browser-local --cdp-url <URL> --session s1 click 100 200
# Click lalu tunggu navigation selesai
browser-local --cdp-url <URL> --session s1 click 0 --wait-nav
# Click lalu tunggu network idle (SPA/JS-heavy)
browser-local --cdp-url <URL> --session s1 click 0 --wait-idle
```

### Input / Type (FAST default — set value via eval langsung)
```bash
browser-local --cdp-url <URL> --session s1 type "hello world"
browser-local --cdp-url <URL> --session s1 input 3 "value baru"
```

### Scroll
```bash
browser-local --cdp-url <URL> --session s1 scroll down --amount 500
browser-local --cdp-url <URL> --session s1 scroll up
```

### Back
```bash
browser-local --cdp-url <URL> --session s1 back
```

### Keys
```bash
browser-local --cdp-url <URL> --session s1 keys Enter
browser-local --cdp-url <URL> --session s1 keys Tab
browser-local --cdp-url <URL> --session s1 keys Escape
```

### Hover / Double Click / Right Click
```bash
browser-local --cdp-url <URL> --session s1 hover 0
browser-local --cdp-url <URL> --session s1 dblclick 2
browser-local --cdp-url <URL> --session s1 rightclick 1
```

### Wait
```bash
browser-local --cdp-url <URL> --session s1 wait selector "#login"
browser-local --cdp-url <URL> --session s1 wait text "Welcome"
browser-local --cdp-url <URL> --session s1 wait navigation
browser-local --cdp-url <URL> --session s1 wait navigation --timeout 5
browser-local --cdp-url <URL> --session s1 wait networkidle
browser-local --cdp-url <URL> --session s1 wait networkidle --timeout 20 --quiet 1
browser-local --cdp-url <URL> --session s1 wait element 0    # Tunggu element index 0 muncul
browser-local --cdp-url <URL> --session s1 wait element 5 --timeout 10
# Semua wait support --timeout (default 15s untuk selector/text/element, 10s untuk navigation, 15s untuk networkidle)
```

### Network Interceptor (Seperti Burp Proxy)

> **Gunakan seperti bug hunter real:** Aktifkan hanya saat kamu sudah tahu persis endpoint mana yang perlu di-intercept. Jangan hidupkan untuk crawling buta — itu bukan fungsinya. Flow yang benar: eksplorasi dulu → paham alurnya → aktifkan intercept di momen spesifik → modify → lanjutkan.

**Dual Engine:**
- **JS Override** — intercept `fetch()` dan `XMLHttpRequest` (JS-level)
- **CDP Fetch Domain** — intercept **semua request** termasuk **form POST navigation**, image, CSS, dll (network-level, seperti Burp Suite)

Saat `intercept start`, kedua engine aktif. Request dari JS override muncul dengan `type: fetch`/`xhr`, request dari CDP Fetch muncul dengan `type: fetch-cdp`.

```bash
# Start intercept — request cocok pattern akan di-pause
browser-local --cdp-url <URL> --session s1 intercept start --pattern ".*api.*"

# Lihat request yang tertahan (JS override + CDP Fetch)
browser-local --cdp-url <URL> --session s1 intercept list

# Modify request — ganti body, method, header
browser-local --cdp-url <URL> --session s1 intercept modify 0 --body '{"admin":true}' --method POST --header "X-Inject: yes"

# Lepas request yang sudah dimodifikasi
browser-local --cdp-url <URL> --session s1 intercept continue 0

# Fulfill (CDP Fetch only) — langsung kirim response palsu, request TIDAK sampai ke server
# Cocok untuk bypass OTP, bypass verifikasi, dll
browser-local --cdp-url <URL> --session s1 intercept fulfill 0 --status 200 --body '{"success":true}'

# Drop request
browser-local --cdp-url <URL> --session s1 intercept drop 0

# Stop interceptor — semua pending request langsung dilepas
browser-local --cdp-url <URL> --session s1 intercept stop
```

#### Response Intercept (JS Override only)

```bash
browser-local --cdp-url <URL> --session s1 intercept res list
browser-local --cdp-url <URL> --session s1 intercept res modify 0 --body '{"hacked":true}' --status 200
browser-local --cdp-url <URL> --session s1 intercept res continue 0
browser-local --cdp-url <URL> --session s1 intercept res drop 0
```

### Cookies
```bash
browser-local --cdp-url <URL> --session s1 cookies get
browser-local --cdp-url <URL> --session s1 cookies clear
```

### Cloudflare Turnstile Solver
```bash
browser-local --cdp-url <URL> --session s1 solve
```

### Tab Management
```bash
browser-local --cdp-url <URL> --session s1 tab list
browser-local --cdp-url <URL> --session s1 tab new
```

### Select / Upload
```bash
browser-local --cdp-url <URL> --session s1 select 2 "option_value"
browser-local --cdp-url <URL> --session s1 upload 0 "/path/file.pdf"
```

---

## 3. HTTP History (Auto-Log seperti Burp Proxy History)

**Semua request/responses yang lewat browser dicatat otomatis** — baik lewat fetch(), XHR, maupun form navigation. Tidak perlu intercept aktif.

```bash
# List history (50 terakhir)
browser-local --cdp-url <URL> --session s1 history list
browser-local --cdp-url <URL> --session s1 history list --limit 100
browser-local --cdp-url <URL> --session s1 history list --scope       # Hanya dalam scope

# Lihat detail request/response entry
browser-local --cdp-url <URL> --session s1 history get 0

# Cari di semua history (case-insensitive)
browser-local --cdp-url <URL> --session s1 history search "token"
browser-local --cdp-url <URL> --session s1 history search "admin"

# Simpan entry ke file JSON
browser-local --cdp-url <URL> --session s1 history save 3 request.json

# Hapus semua history
browser-local --cdp-url <URL> --session s1 history clear
```

History disimpan di `/tmp/browser-local-history.json`.

---

## 4. Sitemap (Tree URL dari History)

Menampilkan struktur semua host/path yang pernah dikunjungi, di-extract dari history.

```bash
browser-local --cdp-url <URL> --session s1 sitemap
# Output: { "example.com": { "total": 10, "paths": ["/", "/api/login", ...] }, ... }
```

---

## 5. Repeater (Kirim Ulang Request via HTTP Client)

Seperti Burp Repeater — kirim ulang request dari history, dari file, atau manual. Tidak menggunakan browser — request dikirim langsung via Python HTTP client.

### Dari HTTP History
```bash
# Re-send entry index 3 dari history
browser-local --cdp-url <URL> --session s1 repeater history 3
browser-local --cdp-url <URL> --session s1 repeater history 3 --timeout 30
```

### Manual (send arbitrary request)
```bash
browser-local --cdp-url <URL> --session s1 repeater send "https://api.target.com/login" \
  --method POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer xxx" \
  --body '{"username":"admin","password":"test"}'
```

### Dari Saved Request File
```bash
browser-local --cdp-url <URL> --session s1 repeater load request.json
```

---

## 6. Collaborator (Out-of-Band Detection via interactsh)

Integrasi dengan [interactsh](https://github.com/projectdiscovery/interactsh) — open-source Burp Collaborator alternative. Untuk deteksi SSRF, Blind XSS, DNS exfiltration, dll.

### Start Collaborator
```bash
# Start interactsh-client di background, dapatkan payload URL
browser-local --cdp-url <URL> --session s1 collaborator start
# Output: { "collaborator": "started", "payload": "xxxx.oast.pro", "server": "oast.pro" }
```

### Inject Payload ke Halaman
```bash
# Inject sebagai header request (fetch ke collaborator URL)
browser-local --cdp-url <URL> --session s1 collaborator inject --where header
# Inject sebagai image/param
browser-local --cdp-url <URL> --session s1 collaborator inject --where param
# Pakai payload spesifik (tanpa perlu start)
browser-local --cdp-url <URL> --session s1 collaborator inject --payload "custom.oast.pro"
```

### Poll / Status
```bash
# Cek status + interactions terbaru
browser-local --cdp-url <URL> --session s1 collaborator status
# Poll saja
browser-local --cdp-url <URL> --session s1 collaborator poll
```

### Stop
```bash
browser-local --cdp-url <URL> --session s1 collaborator stop
```

---

## 7. Scope (Seperti Burp Target Scope)

Filter aktivitas hanya untuk domain/path tertentu.

```bash
# Lihat scope saat ini
browser-local --cdp-url <URL> --session s1 scope status

# Include pattern
browser-local --cdp-url <URL> --session s1 scope include "target.com"
browser-local --cdp-url <URL> --session s1 scope include "api.target.com"

# Exclude pattern
browser-local --cdp-url <URL> --session s1 scope exclude "cdn.target.com"

# Enable/disable filtering
browser-local --cdp-url <URL> --session s1 scope enable
browser-local --cdp-url <URL> --session s1 scope disable

# Gunakan dengan open (cek scope dulu)
browser-local --cdp-url <URL> --session s1 open "https://target.com" --scope
```

---

## 8. Match and Replace (Auto-modify Request)

Seperti Burp Match and Replace — otomatis modifikasi request/response berdasarkan regex rule.

```bash
# Tambah rule: replace semua "Bearer .*" dengan "Bearer HACKED"
browser-local --cdp-url <URL> --session s1 matchreplace add \
  --target request --where header \
  --match "Bearer .*" --replace "Bearer HACKED"

# Tambah rule: replace body
browser-local --cdp-url <URL> --session s1 matchreplace add \
  --target request --where body \
  --match "\"admin\":false" --replace "\"admin\":true"

# List rules
browser-local --cdp-url <URL> --session s1 matchreplace list

# Hapus rule
browser-local --cdp-url <URL> --session s1 matchreplace delete 1

# Clear semua
browser-local --cdp-url <URL> --session s1 matchreplace clear
```

---

## 9. Intruder (Payload Fuzzing via Wordlist)

Basic Intruder — kirim banyak request dengan payload dari wordlist. Seperti Burp Intruder (Sniper mode).

### Dari Template File
```bash
# Simpan request template dulu:
# { "url": "https://api.target.com/user/FUZZ", "method": "GET" }

# Run intruder
browser-local --cdp-url <URL> --session s1 intruder run \
  --template request.json \
  --wordlist usernames.txt
```

### Inline (Sniper)
```bash
browser-local --cdp-url <URL> --session s1 intruder sniper \
  --url "https://api.target.com/api/user/FUZZ" \
  --wordlist payloads.txt

browser-local --cdp-url <URL> --session s1 intruder sniper \
  --url "https://api.target.com/login" \
  --method POST \
  --body '{"user":"FUZZ","pass":"FUZZ"}' \
  --wordlist creds.txt \
  --header "Content-Type: application/json"
```

---

## 10. Compare (Seperti Burp Comparer)

Bandingkan dua response — dari history atau dari file saved.

### Dari History
```bash
browser-local --cdp-url <URL> --session s1 compare history 0 1
```

### Dari File
```bash
browser-local --cdp-url <URL> --session s1 compare files --path1 resp1.json --path2 resp2.json
```

---

## 11. Session Management

Tiap `--session` adalah 1 tab terpisah. Session disimpan di `/tmp/browser-local-sessions.json`.

```bash
# Lihat semua session aktif
browser-local sessions

# Multiple tabs = multiple sessions
browser-local --cdp-url <URL> --session tab1 open "https://a.com"
browser-local --cdp-url <URL> --session tab2 open "https://b.com"
```

---

## 12. Stealth & Anti-Deteksi

Inject otomatis via `Page.addScriptToEvaluateOnNewDocument` + re-inject tiap command.

**Typing (default — FAST):** `type` dan `input` set value langsung via `js_eval` + dispatch `input`/`change` events. Satu shot, tanpa per-char keyboard events.

**Typing (`--human`):** Per-karakter dengan event keyboard asli (`keyDown` → `char` → `keyUp`) + delay acak 30-80ms per karakter.

**Click (default — FAST):** Langsung `mousePressed` + `mouseReleased` tanpa easing, tanpa delay.

**Click (`--human`):** Menggerakkan mouse gradual dengan easing curve (ease-out quad) + random micro-delay antar steps.

| Proteksi | Status |
|----------|--------|
| `navigator.webdriver` → `undefined` | ✅ |
| User-Agent tanpa "HeadlessChrome" | ✅ via `--user-agent` |
| `navigator.plugins` sebagai PluginArray asli (3 plugin) | ✅ |
| `navigator.languages` → `['en-US','en']` | ✅ |
| `chrome.runtime` + `chrome.*` properties | ✅ |
| WebGL vendor/renderer spoof (Intel Arc A770 modern) | ✅ |
| Screen 1920×1080 via `--ozone-override-screen-size` | ✅ |
| Permission query override | ✅ |
| `--disable-blink-features=AutomationControlled` | ✅ |
| `navigator.userAgentData` (UA Client Hints) — brands, mobile, platform, getHighEntropyValues | ✅ |
| `navigator.platform` → `Linux x86_64` | ✅ |
| `navigator.pdfViewerEnabled` → `true` | ✅ |
| `navigator.cookieEnabled` → `true` | ✅ |
| `window.outerWidth/outerHeight` sinkron dengan screen (1920×1080) | ✅ |
| `screen.availWidth/availHeight/availTop/availLeft` realistik | ✅ |
| `screen.colorDepth/pixelDepth` → 24 | ✅ |
| `document.hidden` → `false`, `visibilityState` → `visible` | ✅ |
| `performance.memory` — jsHeapSizeLimit, total/used JS heap | ✅ |
| `navigator.connection` — effectiveType 4g, downlink 10, rtt 50 | ✅ |
| AudioContext fingerprint spoof — OfflineAudioContext output dimodifikasi | ✅ |
| `navigator.bluetooth` — getAvailability false | ✅ |
| `navigator.credentials` — mock lengkap | ✅ |
| CDP injection globals (`cdc_*`) dibersihkan | ✅ |
| WebGL update ke Intel Arc A770 (bukan UHD 620 lawas) | ✅ |

---

## 13. Utility Commands

```bash
browser-local doctor          # Cek dependency
browser-local install         # Cek Chromium binary
browser-local init            # Generate template
browser-local connect         # Connect ke running browser
browser-local close           # Stop browser + cleanup
browser-local config          # Info konfigurasi (via env / CLI flags)
```
