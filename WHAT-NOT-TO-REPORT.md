# WHAT NOT TO REPORT — Shopify Bug Bounty Ineligibility Guide
## Stop Wasting Triage Time. Know What's Out of Scope Before You Submit.

**Version:** 2.3 — August 8, 2026 (Compressed)
**Sources:** HackerOne Core Ineligible, Shopify Criteria, Known Issues, Scope, Recon Data (7 reports), CVE Research, Infrastructure Security

---

## QUICK REFERENCE CARD

| Finding | Verdict | Section |
|---|---|---|
| Self-XSS (paste into console, dev tools) | DON'T REPORT | 2.1, 3.1.5-3.1.6 |
| Storefront XSS via merchant content | DON'T REPORT | 3.1.1 |
| XSS in rich text editor (iFrame) | DON'T REPORT | 3.1.2 |
| Checkout XSS | DON'T REPORT | 3.1.3 |
| CDN public file access | DON'T REPORT | 3.3.2, 5.3 |
| Admin `.json` endpoints with staff auth | DON'T REPORT | 3.4.1, 5.1, 16.1 |
| Password/email verification token in URL | DON'T REPORT | 3.4.3-3.4.4 |
| Domain verification TXT in DNS | DON'T REPORT | 3.4.5 |
| Staff sees expected role data | DON'T REPORT | 3.4.6, 16.18 |
| Store/subdomain enumeration | DON'T REPORT | 3.4.7 |
| Opening Soon password bypass | DON'T REPORT | 3.4.8, 16.4 |
| Stocky issues | DON'T REPORT | 3.4.9 |
| Order Printer Liquid access | DON'T REPORT | 3.4.10, 16.17 |
| Staff can export customer data | DON'T REPORT | 3.4.11 |
| Physical device access | DON'T REPORT | 3.5.1 |
| Mobile biometrics bypass via passcode | DON'T REPORT | 3.5.2 |
| Mobile binary API key extraction | DON'T REPORT | 3.5.3 |
| Mobile emulator access | DON'T REPORT | 3.5.5 |
| POS PIN brute-force (physical access) | DON'T REPORT | 3.5.6 |
| Third-party app issues | DON'T REPORT (to app dev) | 3.6 |
| DoS/DDoS/rate limit exhaustion | DON'T REPORT | 3.7, 2.4 |
| Open redirect (no chain) | DON'T REPORT | 3.8 |
| HTML injection in emails (no chain) | DON'T REPORT | 3.9 |
| SSRF (no internal access demonstrated) | DON'T REPORT | 3.10 |
| Race condition (plan limit bypass) | DON'T REPORT | 3.11 |
| Social engineering | DON'T REPORT | 3.12, 2.4 |
| GraphQL introspection | DON'T REPORT | 3.13, 16.3 |
| Password complexity/policy | DON'T REPORT | 3.14, 16.25 |
| Missing security headers (no PoC) | DON'T REPORT | 2.3 |
| TLS config issues (no MiTM) | DON'T REPORT | 2.2 |
| Cart AJAX/CSRF (no auth) | DON'T REPORT | 3.2.1, 16.21 |
| Login/logout CSRF (no chain) | DON'T REPORT | 3.2.2 |
| Storefront API tokenless access | DON'T REPORT | 5.5, 16.9 |
| Storefront API tokens in theme JS | DON'T REPORT | 5.14, 16.20 |
| Rate limit headers visible | DON'T REPORT | 5.23 |
| Health check endpoints | DON'T REPORT | 5.11, 16.19 |
| Well-known files (.well-known, llms.txt) | DON'T REPORT | 5.10, 16.32 |
| Legacy REST API functional | DON'T REPORT | 5.12, 16.24 |
| Different API version behavior | DON'T REPORT | 5.13, 16.25 |
| GIDs with sequential numbers | DON'T REPORT | 5.25 |
| Staff list visible to staff | DON'T REPORT | 5.26 |
| Cart not encrypted in transit | DON'T REPORT | 5.27 |
| Plus bot protection not always-on | DON'T REPORT | 5.28 |
| Checkout extensions sandboxed | DON'T REPORT | 5.29 |
| POS extensions see transactions | DON'T REPORT | 5.30 |
| Storefront MCP no auth | DON'T REPORT | 5.31.1, 16.7 |
| Customer Accounts MCP requires token | DON'T REPORT | 5.31.2 |
| Dev MCP runs locally | DON'T REPORT | 5.31.3 |
| UCP open protocol | DON'T REPORT | 5.31.4 |
| Sidekick respects admin perms | DON'T REPORT | 5.32.1, 16.8 |
| Sidekick extensions require review | DON'T REPORT | 5.32.2 |
| Sidekick on Apple Watch limited | DON'T REPORT | 5.32.3 |
| Sidekick prompt injection (theoretical) | DON'T REPORT | 5.32.4 |
| Sidekick no public API | DON'T REPORT | 5.32.5 |
| B2B lower pricing | DON'T REPORT | 5.34.1 |
| B2B client-side qty bypass | DON'T REPORT | 5.34.2 |
| B2B payment terms (Net 30/60) | DON'T REPORT | 5.34.3 |
| B2B company contacts place orders | DON'T REPORT | 5.34.4 |
| B2B sequential location IDs | DON'T REPORT | 5.34.5 |
| B2B on Advanced plan | DON'T REPORT | 5.34.6 |
| Functions in Wasm sandbox | DON'T REPORT | 5.35.1, 16.34 |
| Functions no network access | DON'T REPORT | 5.35.2 |
| Functions prohibit non-determinism | DON'T REPORT | 5.35.3 |
| Function errors block checkout | DON'T REPORT | 5.35.4 |
| Function input query metafields | DON'T REPORT | 5.35.5 |
| Legacy Scripts stopped (Jun 2026) | DON'T REPORT | 5.35.6 |
| Functions resource limits | DON'T REPORT | 5.35.7 |
| Web Pixel sees customer events | DON'T REPORT | 5.36.1, 16.13 |
| Web Pixel sandbox (no DOM) | DON'T REPORT | 5.36.2, 16.35 |
| Web Pixel fetch() calls | DON'T REPORT | 5.36.3 |
| Web Pixel api.browser cookies | DON'T REPORT | 5.36.4 |
| Custom Pixels lax sandbox | DON'T REPORT | 5.36.5 |
| Web Pixel respects consent | DON'T REPORT | 5.36.6 |
| Customer Privacy API public | DON'T REPORT | 5.36.7, 16.37 |
| Checkout Kit JWT required | DON'T REPORT | 5.37.1, 16.14 |
| Checkout Kit third-party cookies | DON'T REPORT | 5.37.2 |
| Checkout Kit CSP allowlist | DON'T REPORT | 5.37.3 |
| Checkout Kit checkout URL from public data | DON'T REPORT | 5.37.4 |
| Checkout Kit JWT 60-min expiry | DON'T REPORT | 5.37.5 |
| Checkout Kit credentials in client code (app dev) | DON'T REPORT | 5.37.6 |
| Checkout Kit error types documented | DON'T REPORT | 5.37.7 |
| Market subdomains predictable | DON'T REPORT | 5.38.1 |
| Products configured per-market | DON'T REPORT | 5.38.2 |
| Market-driven shipping preview | DON'T REPORT | 5.38.3 |
| Multi-currency rounding | DON'T REPORT | 5.38.4 |
| Shipping labels via GraphQL | DON'T REPORT | 5.38.5 |
| Carrier services changes (2026-10) | DON'T REPORT | 5.38.6 |
| Storefront API no documented rate limits | DON'T REPORT | 5.39.1 |
| Web Bot Auth optional | DON'T REPORT | 5.39.2 |
| Tokenless access (1,000 query cost) | DON'T REPORT | 5.39.3 |
| Cart ID is not security boundary | DON'T REPORT | 5.39.5 |
| customerAccessTokenCreate no rate limit | DON'T REPORT | 5.39.6 |
| Storefront API public metafields | DON'T REPORT | 5.39.7 |
| CORS on public endpoints | DON'T REPORT | 16.12 |
| Monorail telemetry accepts data | DON'T REPORT | 5.9, 16.31 |
| Rate limiting absent on endpoint | DON'T REPORT | 16.10 |
| Email verification optional at signup | DON'T REPORT | 16.11 |
| Private app token in own source | DON'T REPORT | 16.26 |
| Sitemap product URLs | DON'T REPORT | 16.27 |
| Script tags on storefront | DON'T REPORT | 16.28 |
| App proxy has storefront context | DON'T REPORT | 16.29 |
| Product JSON endpoints public | DON'T REPORT | 16.30 |
| Response headers leak infra | DON'T REPORT | 16.33 |
| Checkout CSP strict | DON'T REPORT | 16.36 |
| Shopify Magic no public API | DON'T REPORT | 16.39 |
| Combined listings / bundles | DON'T REPORT | 16.40 |
| Multi-Pass shared accounts | DON'T REPORT | 16.16 |
| Combined listings feature | DON'T REPORT | 16.40 |

---

## 1. EXECUTIVE SUMMARY

**Why This File Exists:** Each week, Shopify triage receives 60-70 reports that are immediately closed as Informative/N/A. This wastes your time, triage time, and your reputation.

**How to Use:**
1. **Before hunting:** Memorize the key DON'T REPORT patterns above
2. **While hunting:** Use Section 10 Quick Decision Guide
3. **Before submitting:** Run the 10-question checklist (Section 11)
4. **Check target:** Confirm domain in Section 9

**The Golden Rule:**
> If impact requires chaining with another vulnerability (XSS, CSRF, MITM, physical access) to be meaningful → NOT a reportable finding.
> 
> Shopify requires demonstrated, realistic impact. Theoretical chains are not accepted.

---

## 2. HACKERONE CORE INELIGIBLE FINDINGS

> These are globally ineligible across ALL HackerOne programs, including Shopify.

| # | Category | What's Ineligible |
|---|---|---|
| 1 | Self-XSS (unlikely interaction) | Requires victim to paste code, use console, disable CSP, edit HTML, set browser flags |
| 2 | Theoretical (no real impact) | Missing headers without PoC, TLS issues without MiTM, version disclosure, cookie flags on non-session cookies, host header injection without ATO/cache poison, email spoofing without delivered phishing, OPTIONS/TRACE without info disclosure, verbose errors without PII |
| 3 | Optional hardening | Missing CSP on non-checkout, missing security.txt, missing Referrer-Policy, missing Feature-Policy, missing X-Content-Type-Options (correct type), missing X-XSS-Protection (deprecated), HSTS on subdomains w/o HTTPS, CT monitoring without bypass, OCSP stapling without MiTM, DNS CAA missing, DNSSEC not configured (by design), preload not on all subdomains, SRI not on all scripts, nonce-based CSP not used (origin allowlisting used instead) |
| 4 | Prohibited testing | DoS/DDoS, social engineering, physical security, mass scanning, spamming, testing live merchants |

---

## 3. SHOPIFY-SPECIFIC INELIGIBLE ISSUES

| Section | Issue | Status | Why |
|---|---|---|---|
| 3.1.1 | Storefront XSS via merchant content | Out of scope | Self-XSS: merchant injects into own store; requires admin access to inject |
| 3.1.1 | Non-auth stored XSS (review, contact form) | MAYBE IN SCOPE | Attacker injects WITHOUT admin access; requires demonstrated cross-customer impact |
| 3.1.2 | iFrame/Rich Text Editor XSS | Out of scope | Merchant intentionally embeds HTML; can't inject into others' stores |
| 3.1.3 | Checkout XSS | Out of scope | Sandboxed by CSP (no `unsafe-inline`, no `unsafe-eval`); Self-XSS |
| 3.1.4 | Response header XSS | Out of scope | WAF + edge infrastructure blocks; impractical exploitation |
| 3.1.5-6 | Console/dev tools/edit HTML | Out of scope | Self-XSS explicitly (HackerOne policy) |
| 3.2.1 | Cart AJAX CSRF | Out of scope | Cart is intentionally public (`CORS: *`), no auth needed → CSRF irrelevant |
| 3.2.2 | Login/logout CSRF (no chain) | Out of scope | Logout CSRF: user re-logs in, no data loss. Login CSRF: attacker needs victim's account, can't access victim data |
| 3.3.1 | CDN arbitrary file upload | Out of scope | CDN designed for public assets; requires admin to upload |
| 3.3.2 | CDN stored XSS | Out of scope | `cdn.shopify.com` is different origin from storefront; sandboxed |
| 3.3.3 | CDN sensitive data disclosure | Out of scope | Product images, theme files, email templates intentionally public |
| 3.4.1 | Staff access to settings JSON | Out of scope | Same auth as HTML; `.json` returns same data in machine-readable format |
| 3.4.2 | Merchant public files | Out of scope | `/admin/settings/files` serves public CDN files by design |
| 3.4.3 | Password reset token in URL | Out of scope | By design — single-use, time-limited (1-4 hrs) |
| 3.4.4 | Email verification token in URL | Out of scope | Standard across all platforms — single-use |
| 3.4.5 | Domain verification TXT in DNS | Out of scope | Public DNS — standard verification method |
| 3.4.6 | Staff permission nuances | IN vs OUT | IN: accessing data BEYOND role. OUT: accessing data needed for job |
| 3.4.7 | Store enumeration via myshopify.com | Out of scope | Public info — storefronts are public, DNS is wildcard |
| 3.4.8 | Opening Soon password bypass | Out of scope | Not a security boundary — documented as bypassable |
| 3.4.9 | Stocky | Out of scope | Third-party app, separate infra |
| 3.4.10 | Order Printer Liquid access | Out of scope | Intended — merchants customize templates |
| 3.4.11 | Staff can export customer data | Out of scope | Intended functionality for customer service/ops |
| 3.5.1 | Physical device access | Out of scope | Physical security, not Shopify vuln |
| 3.5.2 | Mobile biometrics via passcode | Informative | Passcode fallback is standard iOS/Android behavior |
| 3.5.3 | Mobile binary reverse engineering | Out of scope | Public Storefront API tokens are intentional |
| 3.5.4 | Mobile data storage (root/jailbreak) | Out of scope | Platform-level; attacker has full device control |
| 3.5.5 | Mobile emulator access | Out of scope | Designed for development |
| 3.5.6 | POS PIN brute-force (physical) | Out of scope | Physical security issue |
| 3.6 | Third-party apps | Out of scope | Report to app developer; Shopify only via 1-week rule, no bounty |
| 3.7 | DDoS | Out of scope | Explicitly excluded |
| 3.8 | Open redirect (no chain) | Out of scope | Must chain to OAuth token theft or phishing |
| 3.9 | HTML injection in emails (no chain) | Out of scope | Modern email clients strip JS; no impact |
| 3.10 | SSRF (no internal access) | Out of scope | Must access metadata/internal services |
| 3.11 | Race condition (plan limits) | Out of scope | Explicit — billing boundary, not security |
| 3.12 | Social engineering | Out of scope | Explicitly excluded |
| 3.13 | GraphQL introspection | Out of scope | Intended behavior (H1-2886723) |
| 3.14 | Password complexity | Out of scope | Intentionally flexible |

---

## 4. HACKERONE CORE CROSS-REFERENCE

| H1 Category | Shopify Example | Key Point |
|---|---|---|
| Self-XSS | Storefront content via merchant admin | Requires merchant to inject |
| Clickjacking w/o impact | No CSP on blog → no vuln | Check if you can actually clickjack |
| Missing header | HSTS missing on subdomain | Must demonstrate MiTM |
| Rate limit bypass | GraphQL introspection rate limit | Must demonstrate data access |
| User enum | Login: "Invalid email" vs "Invalid email or password" | Must chain to account compromise |
| Error msgs | Stack traces without PII | Must leak sensitive data |
| Open redirect | `?return_to=evil.com` on settings | Must chain to OAuth theft/phishing |
| Content injection | Store name in email HTML | Must demonstrate XSS/data access |
| Cookie flags | No HttpOnly on non-session cookie | Must demonstrate session theft |
| TLS config | TLS 1.1 on edge node | Must demonstrate actual MiTM |
| SPF/DKIM | No DMARC on subdomain | Must deliver working phishing email |
| OPTIONS/TRACE | TRACE on API endpoint | Must demonstrate info disclosure |
| Server version | `X-Powered-By: Shopify` | Not sensitive alone |
| No lockout | No CAPTCHA on login | Must demonstrate credential compromise |
| Weak password | 8-char min, no special chars | Intentionally flexible |
| Session timeout | No auto-expiry | Must demonstrate session hijack |
| Social eng | Phishing Shopify support | Entirely out of scope |
| Physical | POS PIN via physical access | Entirely out of scope |
| DoS/DDoS | Cache poisoning affects users | Entirely out of scope |
| Auto scanning | Tool generates excessive traffic | IP ban risk |

---

## 5. FALSE POSITIVE PATTERNS FROM RECON DATA

| # | Pattern | Why Not a Bug | Boundary / Vuln Threshold |
|---|---|---|---|
| 5.1 | Admin `.json` endpoints with staff auth | Powers SPA admin UI; same auth as HTML | Unauthenticated access OR `.json` returns MORE data than HTML |
| 5.2 | GraphQL introspection | Intentionally enabled (H1-2886723) | Undocumented mutation with authz bypass |
| 5.3 | CDN public content | Files intentionally public | Cross-tenant access or cache poisoning (H1-1695604=$3,800) |
| 5.4 | Opening Soon password bypass | Not a security boundary | Protects admin resources |
| 5.5 | Storefront API tokenless | Intentional (≤1,000 query cost) | Accessing admin data |
| 5.6 | Product/collection JSON endpoints | Public by design for headless | Hidden/draft products exposed |
| 5.7 | Cart AJAX endpoints | Public by design (`CORS: *`) | Performing authenticated actions |
| 5.8 | Response headers (server, CF-Ray) | HTTP protocol standard | Headers contain PII/session/credentials |
| 5.9 | Monorail telemetry | Designed to accept telemetry | Telemetry leaks data to unauthorized parties |
| 5.10 | Well-known files | Intentionally public | Files expose sensitive URLs/credentials |
| 5.11 | Health check endpoints | Standard infra (CVE-2024-45720 patched) | Health endpoint leaks secrets |
| 5.12 | Legacy REST API | Backward compatibility | Legacy bypasses newer authz checks |
| 5.13 | Different API versions | Intentional versioning | Version downgrade bypasses authz |
| 5.14 | Storefront API tokens in JS | Public scope-limited tokens | Admin tokens in client code |
| 5.15 | Private app tokens in own code | Your own store | Other merchants' tokens found publicly |
| 5.16 | Sitemap product URLs | SEO best practice | Hidden/draft products in sitemap |
| 5.17 | Script Tags | Require admin/OAuth | Unauthenticated script tag creation |
| 5.18 | App Proxy inherits Liquid context | By design for dynamic content | HMAC verification missing |
| 5.19 | Web Pixel event data | Intended for analytics | Pixel accesses data beyond declared scopes |
| 5.20 | Customer Account API token in localStorage | Standard OAuth pattern | Cross-origin token theft |
| 5.21 | App Bridge session tokens in memory | 1-min TTL, encrypted | Persistent storage or excessive TTL |
| 5.22 | Can view own OAuth tokens | Expected (your own tokens) | Viewing OTHER people's tokens |
| 5.23 | Rate limit headers visible | Intentional for API devs | Rate limit bypass enables brute-force |
| 5.24 | Checkout URL standardized | Tokens cryptographically random | Tokens are predictable/sequential |
| 5.25 | GIDs contain sequential numbers | Authorization always enforced | Missing server-side authz check |
| 5.26 | Staff can see other staff | Necessary for management | Access data beyond role scope |
| 5.27 | Cart not encrypted | HTTPS encrypts transit; cart has no PII | Cart manipulated for financial loss |
| 5.28 | Plus bot protection not always-on | Event-based, documented | Bypass allows full account takeover |
| 5.29 | Checkout extensions sandboxed | Intentional (Magecart prevention) | Sandbox escape to access payment data |
| 5.30 | POS extensions see transactions | Intended for app dev | Cross-tenant transaction data access |
| 5.31.1 | Storefront MCP no auth | Mirrors public Storefront API | MCP exposes admin data or PII |
| 5.31.2 | Customer Accounts MCP needs token | Expected auth mechanism | Server accepts falsified tokens |
| 5.31.3 | Dev MCP runs locally | Local dev tool, stdio transport | MCP exposes network endpoints |
| 5.31.4 | UCP open protocol | Designed for agentic commerce | UCP enables unauthorized merchant access |
| 5.31.5 | AI Toolkit no auth (dev) | Developer tools for dev stores | Dev MCP exposes network services |
| 5.32.1 | Sidekick respects admin perms | Security feature | Sidekick leaks cross-tenant data |
| 5.32.2 | Sidekick extensions require review | Security control | Review bypass allows malicious extensions |
| 5.32.3 | Sidekick Apple Watch limited | By design (read-only) | Watch exposes sensitive actions |
| 5.32.4 | Sidekick prompt injection (theoretical) | No demonstrated impact | Crafted prompt exfiltrates data |
| 5.32.5 | Sidekick no public API | Reduced attack surface | API exposed without auth |
| 5.33.1 | Hydrogen health endpoints | Standard infra (patched CVE-2024-45720) | Health endpoints leak secrets |
| 5.33.2 | Hydrogen API tokens in JS | Public scope-limited tokens | Admin tokens in client code |
| 5.33.3 | Hydrogen framework-agnostic | Intentional architectural choice | Framework abstraction allows bypass |
| 5.33.4 | Cart AJAX from any origin | Intentional (`CORS: *`) | Cart used for auth actions |
| 5.33.5 | Customer Account API token in localStorage | Standard storage | Cross-origin token access |
| 5.34.1 | B2B lower pricing | Intentional volume discounts | Consumer accesses B2B pricing |
| 5.34.2 | B2B client-side qty bypass | Server-side is the boundary | Server-side enforcement bypassed |
| 5.34.3 | B2B payment terms | Intentional B2B feature | Terms bypass payment auth |
| 5.34.4 | Company contacts place orders | Intended functionality | Unauthorized company access |
| 5.34.5 | B2B sequential location IDs | Server-side authz enforced | Missing server-side authz check |
| 5.34.6 | B2B on Advanced plan | Product decision | Feature restriction bypass |
| 5.35.1 | Functions in Wasm sandbox | Security isolation boundary | Sandbox escape to host system |
| 5.35.2 | Functions no network access | Intentional restriction | Unauthorized network access |
| 5.35.3 | Functions prohibit non-determinism | Correctness requirement | Non-deterministic function executes |
| 5.35.4 | Function errors block checkout | Validation feature | Malicious function blocks all checkouts |
| 5.35.5 | Function input query metafields | Reviewed in App Store | Function accesses beyond declared scope |
| 5.35.6 | Legacy Scripts stopped (Jun 2026) | Planned deprecation | Scripts still executing after date |
| 5.35.7 | Functions resource limits | Documented constraints | Resource limits bypassed |
| 5.36.1 | Web Pixel sees customer events | Intended analytics | Pixel accesses data beyond scopes |
| 5.36.2 | Web Pixel sandbox (no DOM) | Anti-Magecart security | Sandbox escape to access DOM |
| 5.36.3 | Web Pixel fetch() calls | Intended analytics | Pixel exfiltrates to non-CORS endpoint |
| 5.36.4 | Web Pixel api.browser cookies | Sandboxed access | Pixel reads parent frame storage |
| 5.36.5 | Custom Pixels lax sandbox | Merchant-created, intentional | Cross-store pixel injection |
| 5.36.6 | Web Pixel respects consent | Legal requirement | Pixel fires without consent |
| 5.36.7 | Customer Privacy API public | Required for compliance | API exposes PII via privacy methods |
| 5.37.1 | Checkout Kit needs JWT | Intended security mechanism | JWT can be forged/reused |
| 5.37.2 | Checkout Kit third-party cookies | Documented browser limitation | SameSite/iframe bypass |
| 5.37.3 | Checkout Kit CSP allowlist | Standard integration req | CSP bypass via CDN trust |
| 5.37.4 | Checkout URL from public data | Cart is public resource | Checkout URL reveals session data |
| 5.37.5 | Checkout Kit JWT 60-min TTL | Reasonable expiration | JWT reusable after use |
| 5.37.6 | Checkout Kit creds not in client | Documented security req | Shopify's own creds in mobile binary |
| 5.37.7 | Checkout Kit error types | Intentional API design | Error types leak sensitive info |
| 5.38.1 | Market subdomains predictable | Intentional SEO structure | Prediction enables unauthorized access |
| 5.38.2 | Products per-market | Intentional Markets feature | Hidden market product accessible |
| 5.38.3 | Market-driven shipping preview | New feature rollout | Shipping rates manipulable |
| 5.38.4 | Multi-currency rounding | Documented rounding | Rounding enables financial abuse |
| 5.38.5 | Shipping labels via GraphQL | New API feature (auth required) | Unauthenticated label purchase |
| 5.38.6 | Carrier services changes | Planned API change | Change enables unauthorized modifications |
| 5.39.1 | Storefront API no documented rate limits | Limits exist but undocumented | Rate limit bypass enables brute-force |
| 5.39.2 | Web Bot Auth optional | Tiered access design | Unsigned requests bypass auth |
| 5.39.3 | Tokenless access (1,000 query cost) | Intentional limited access | Access exceeds 1,000 query cost |
| 5.39.4 | Public tokens in theme JS | Scope-limited public tokens | Token has admin scopes |
| 5.39.5 | Cart ID predictable | No sensitive data alone | Cross-user cart access |
| 5.39.6 | customerAccessTokenCreate no rate limit | Must demonstrate brute-force (H1-1363672) | Successful credential compromise |
| 5.39.7 | Public metafields queryable | Intentional for headless | Private metafields accessible |

---

## 6. VDP vs BUG BOUNTY

| Issue | Bug Bounty? | VDP Reportable? |
|---|---|---|
| Self-XSS requiring victim action | No | No |
| Reflected XSS on admin (authenticated) | Yes | Yes |
| Missing security headers | No | No |
| Open redirect with OAuth chain | Yes | Yes |
| Open redirect without chain | No | No |
| Rate limit bypass with data access | Yes | Yes |
| Rate limit bypass without impact | No | No |
| Staff permission bypass (data beyond role) | Yes | Yes |
| Staff sees expected role data | No | No |
| GraphQL introspection | No | No |
| CDN public file access | No | No |
| IDOR on customer data | Yes | Yes |
| IDOR on non-sensitive data | Maybe | Yes |
| Race condition: plan limit bypass | No | No |
| Race condition: payment bypass | Yes | Yes |
| Third-party app vulnerability | No | Yes (redirect to dev) |
| SSRF with cloud metadata access | Yes | Yes |
| SSRF restricted to HTTPS only | No | No |
| Weak password policy | No | No |
| Password reset token reuse | Yes | Yes |
| Password reset token in URL | No | No |
| Social engineering | No | No |
| Physical security | No | No |
| DoS/DDoS | No | No |

### Decision Flow

```
Found something?
├── Prohibited? (DoS, social eng, physical) → STOP
├── Third-party app? → Report to app dev
├── Intended behavior? → Informative (Section 16)
├── Real impact? → Bug bounty report
└── Chains with something? → Include full chain
```

---

## 7. COST OF WASTED TIME

| Metric | Value |
|---|---|
| Total reports annually | 3,000+ |
| Reports per week | ~60-70 |
| Reports closed Informative/N/A | ~40-50% |
| Out-of-scope reports | ~25-30% |
| Triage time per report | ~15-30 min |
| Hours wasted annually | ~750-1,500 |
| Your time wasted per invalid report | 2-4 hours |
| Consequence of repeated invalid reports | Program suspension |

**Opportunity cost:** Time on invalid findings = time NOT finding real bugs ($500-$200,000+ payouts).

---

## 8. TESTING RULES & BOUNDARIES

| Rule | What to Do | What NOT to Do |
|---|---|---|
| 1 | Test ONLY your own stores: `partners.shopify.com/signup/bugbounty` | Never test live merchant stores |
| 2 | Use `@wearehackerone.net` email alias | Never interact with others' customers |
| 3 | All comms via HackerOne | Never contact Shopify Support about bounty |
| 4 | Report via HackerOne only | Never publicly disclose before fix |
| 5 | Cache busters REQUIRED for CDN/cache testing | No DoS/social eng/physical testing |
| 6 | Use dev stores, Shopify Payments test mode | Never use stolen/fake credit cards |
| 7 | Gradual rate testing, respect headers | Don't exhaust rate limits |
| 8 | Report PII exposure immediately, don't access it | Don't store accessed PII |

---

## 9. DOMAINS: IN SCOPE vs OUT OF SCOPE

**Last verified:** HackerOne scope, August 2026.
**Core vs Non-Core:** Core = `your-store.myshopify.com`, `accounts.shopify.com`, `partners.shopify.com`, `admin.shopify.com`, `*.pci.shopifyinc.com`, `arrive-server.shopifycloud.com`, `shopify.plus`, `shop.app`. **Core assets pay higher.**

### In-Scope (Core)

| Domain | Notes |
|---|---|
| `*.shopify.com` (apex, www, help, dev, blog) | Non-Core (see exceptions) |
| `admin.shopify.com` | Core — Unified admin |
| `accounts.shopify.com` | Core — Shopify ID/SSO |
| `partners.shopify.com` | Core — Partner dashboard |
| `your-store.myshopify.com` | Core — ONLY stores YOU created |
| `*.pci.shopifyinc.com` | Core — PCI infrastructure |
| `arrive-server.shopifycloud.com` | Core — Arrive server |
| `shopify.plus` | Core |
| `shop.app` | Core — Consumer Shop app |

### In-Scope (Non-Core)

| Domain | Notes |
|---|---|
| `*.shopifycloud.com` | Internal cloud (EXCEPT supplier-portal) |
| `*.shopify.io` | |
| `*.shopifykloud.com` | |
| `*.shopifycs.com` | |
| `shopifyinbox.com` | |
| `linkpop.com` | |
| `github.com/Shopify/*` | Non-Core — report SDK issues via GHSA |
| Shopify Developed Apps | Flow, Sidekick, Magic, POS, Order Printer, Stocky |
| Shopify Mobile Applications | iOS + Android |
| Shopify Mobile/Third-Party Apps | Conditional — no bounty for third-party |

### Explicitly Out of Scope

| Domain | Notes |
|---|---|
| `*.email.shopify.com` | Explicitly excluded |
| `cdn.shopify.com` / `*.shopifycdn.com` | Explicitly excluded — public by design |
| `community.shopify.com` / `.dev` | Explicitly excluded |
| `academy.shopify.com` | Explicitly excluded |
| `investors.shopify.com` | Explicitly excluded |
| `livechat.shopify.com` | Explicitly excluded |
| `supplier-portal.shopifycloud.com` | Explicit exception |
| `*.shopifyapps.com` | Third-party app infra |
| `*.shopifysvc.com` / `monorail-edge.shopifysvc.com` | NOT in scope |
| `exchangemarketplace.com` | NOT in scope (old scope) |
| Merchant custom domains | Cannot test live merchants |
| Cloudflare (Shopify zone) | Cannot test directly |
| `help.shopify.com` | Under `*.shopify.com` but support system — do not test |

### Formerly In-Scope Now Out

| Formerly | Current Status |
|---|---|
| `cdn.shopify.com` | Out of Scope |
| `community.shopify.com` / `.dev` | Out of Scope |
| `*.myshopify.com` wildcard | NO wildcard — only `your-store.myshopify.com` |
| `*.shopifycdn.com` | Not listed |
| `*.shopifysvc.com` | Not listed |
| `exchangemarketplace.com` | Not listed |
| `github.com/Shopify/*` | **NOW IN scope** (Non-Core) |

### Special Cases

| Service | Status | Notes |
|---|---|---|
| `shopify.com/bugbounty` | In Scope | Info page |
| Mobile app (iOS/Android) | In Scope | Non-Core |
| Shopify POS app | In Scope | Non-Core |
| Shopify Flow | In Scope | Non-Core |
| Sidekick | In Scope | Non-Core |
| Shopify Magic | In Scope | Non-Core |
| Shop app | In Scope | Core |
| Shopify Payments | In Scope | Core-relevant |
| Checkout Kit | In Scope | `*.shopifycloud.com` |
| Shopify Functions | In Scope | Non-Core |
| Web Pixels API | In Scope | Non-Core |
| Customer Account API | In Scope | Non-Core |
| Partner API | In Scope | Core |
| Hydrogen/Oxygen | In Scope | Non-Core |
| Third-party apps | Conditional | No bounty |

---

## 10. QUICK DECISION GUIDE

### Text Flowchart

```
START: Found something?
├── Target in scope? (Section 9) → If NO: STOP
├── Third-party app issue? → If YES: Report to app dev
├── Prohibited? (DoS, social eng, physical) → If YES: STOP
├── Self-XSS? (console, dev tools, paste code) → DON'T REPORT
├── Storefront XSS via merchant content? → DON'T REPORT
├── iFrame/Rich Text Editor XSS? → DON'T REPORT
├── Checkout XSS? → DON'T REPORT
├── CDN content access? → DON'T REPORT
├── Staff JSON with auth? → DON'T REPORT
├── Public file on CDN? → DON'T REPORT
├── Password reset token in URL? → DON'T REPORT
├── Email verification token in URL? → DON'T REPORT
├── Domain verification TXT in DNS? → DON'T REPORT
├── Staff sees expected role data? → DON'T REPORT
├── Store/subdomain enumeration? → DON'T REPORT
├── Opening Soon password bypass? → DON'T REPORT
├── Stocky issue? → DON'T REPORT
├── Order Printer Liquid? → DON'T REPORT
├── CVV missing on saved cards? → DON'T REPORT
├── Mobile: physical device access? → DON'T REPORT
├── Mobile: biometrics via passcode? → DON'T REPORT
├── Mobile: binary API keys? → DON'T REPORT
├── POS PIN brute-force (physical)? → DON'T REPORT
├── DoS/DDoS? → DON'T REPORT
├── Social engineering? → DON'T REPORT
├── Open redirect (no OAuth/phishing chain)? → DON'T REPORT
├── HTML injection in emails (no chain)? → DON'T REPORT
├── SSRF (no internal resource access)? → DON'T REPORT
├── Race condition (plan limits only?)? → DON'T REPORT
├── GraphQL introspection? → DON'T REPORT
├── Password complexity/policy? → DON'T REPORT
├── Missing best practice (no exploit)? → DON'T REPORT
├── Cart manipulation via AJAX? → DON'T REPORT
├── Product JSON scraping? → DON'T REPORT
├── Storefront API tokenless access? → DON'T REPORT
├── Storefront API tokens in theme JS? → DON'T REPORT
├── Customer Account API token in localStorage? → DON'T REPORT
├── App Bridge tokens in memory? → DON'T REPORT
├── Rate limit headers visible? → DON'T REPORT
├── Health endpoints? → DON'T REPORT
├── Well-known files? → DON'T REPORT
├── Legacy REST API? → DON'T REPORT
├── GIDs sequential? → DON'T REPORT
├── Staff list visible? → DON'T REPORT
└── Passes ALL filters AND has realistic impact AND on own test store? → REPORT
```

### Expanded Decision Points (MCP/AI/B2B/Functions/Web Pixel/Checkout Kit)

```
MCP Issues?
├── Storefront MCP no auth? → DON'T REPORT
├── Customer Accounts MCP needs token? → DON'T REPORT
├── Dev MCP local only? → DON'T REPORT
├── UCP open protocol? → DON'T REPORT
└── MCP exposes admin data/PII? → REPORT

Sidekick/AI Issues?
├── Respects admin perms? → DON'T REPORT
├── Extensions require review? → DON'T REPORT
├── Theoretical prompt injection? → DON'T REPORT
├── Performs unauthorized actions via injection? → REPORT
└── Has public API? → Don't care (no API = less attack surface)

Hydrogen/Headless?
├── Health check endpoint? → DON'T REPORT
├── API tokens in JS? → DON'T REPORT (public tokens)
├── Cart AJAX any origin? → DON'T REPORT
├── Customer API token in localStorage? → DON'T REPORT
└── Admin tokens in client code? → REPORT

B2B Issues?
├── Lower B2B pricing? → DON'T REPORT
├── Client-side qty bypass via API? → DON'T REPORT
├── Payment terms (Net 30/60)? → DON'T REPORT
├── Consumer accesses B2B pricing? → REPORT
├── Company A accesses Company B's catalog? → REPORT
└── Server-side qty enforcement bypass? → REPORT

Shopify Functions?
├── Wasm sandbox? → DON'T REPORT
├── No network access by default? → DON'T REPORT
├── Non-determinism prohibited? → DON'T REPORT
├── Resource limits (256KB, 10MB)? → DON'T REPORT
├── Access data beyond input query scope? → REPORT
└── Exfiltrate via fetch target? → REPORT

Web Pixel API?
├── Sees customer event data? → DON'T REPORT
├── No DOM access sandbox? → DON'T REPORT
├── fetch() to external endpoints? → DON'T REPORT
├── Access data beyond declared scopes? → REPORT
├── Extract credit card data? → REPORT (critical)
└── Custom pixels lax sandbox? → DON'T REPORT

Checkout Kit?
├── JWT required for inline? → DON'T REPORT
├── Needs third-party cookies? → DON'T REPORT
├── CSP allowlist required? → DON'T REPORT
├── JWT can be forged/reused? → REPORT
├── 60-min TTL? → DON'T REPORT
├── App dev creds in client code? → DON'T REPORT
└── Shopify's own creds in binary? → REPORT

Markets/Shipping?
├── Predictable subdomains? → DON'T REPORT
├── Products per-market? → DON'T REPORT
├── Multi-currency rounding? → DON'T REPORT
├── Hidden product accessible in market? → REPORT
└── Shipping rate manipulation? → REPORT

Storefront API?
├── No documented rate limits? → DON'T REPORT
├── Web Bot Auth optional? → DON'T REPORT
├── Tokenless access (1,000 cost)? → DON'T REPORT
├── Public tokens in JS? → DON'T REPORT
├── Cart ID predictable? → DON'T REPORT
├── customerAccessTokenCreate no rate limit? → DON'T REPORT (must demonstrate brute-force)
├── Access private metafields? → REPORT
└── Successful credential brute-force? → REPORT

CDN Cache Poisoning?
├── Poison cache to 404 legit files? → REPORT (H1-1695604=$3,800)
└── Files publicly accessible? → DON'T REPORT

Webhook Security?
├── HMAC verification missing? → REPORT (H1-3697491)
├── == instead of constant-time? → REPORT (timing attack)
└── Webhook secret = API secret? → REPORT (key separation)

Known CVEs?
├── CVE-2024-45718/45719/45720 (Hydrogen health)? → DON'T REPORT (patched)
├── CVE-2026-45618 (LiquidJS RCE)? → REPORT only in Shopify infra
├── CVE-2026-30952 (LiquidJS path traversal)? → REPORT only in Shopify infra
└── GHSA-6j52-38f8-qhxr (Shop context confusion)? → REPORT only in unpatched apps
```

---

## 11. CHECKLIST BEFORE SUBMITTING

### 10 Questions (Answer YES to all)

1. **Is the domain in scope?** Confirmed in Section 9. NOT third-party app. NOT live merchant.
2. **Real attacker exploit?** No console/dev tools/paste. No physical access. No social eng. Works in default browser.
3. **Not intended behavior?** Not introspection, CDN files, cart AJAX, tokens in JS, admin JSON, or known false positive.
4. **Real business impact?** Can steal data, take over accounts, manipulate payments, access cross-tenant data.
5. **Not a duplicate/no CVE?** Searched H1 disclosed reports, Known Issues page, NVD, GHSA.
6. **Reproducible 100%?** Consistent, not intermittent/race <10%. Clear PoC.
7. **Shopify core issue?** Root cause in Shopify infra, not third-party app/SDK (GHSA for SDKs).
8. **Tested only your own store?** Created via `partners.shopify.com/signup/bugbounty`, `@wearehackerone.net`.
9. **Not HackerOne ineligible?** Not self-XSS, missing headers, rate limit alone, no user enum chain, no open redirect alone.
10. **Well-written report?** Clear title, summary, steps, PoC, impact, remediation.

### Final Test

> **Theoretical:** "could theoretically lead to [impact] if an attacker also has [access] and victim does [unlikely thing]" → DON'T REPORT

> **Concrete:** "[endpoint] returns [other_user's data] when I send [request] without [auth]. I can steal [sensitive data]" → REPORT

---

## 12. REAL HACKERONE CASE STUDIES (N/A — Why Rejected)

| # | H1 Report | Rejected As | Why / Lesson |
|---|---|---|---|
| 1 | #2886723: GraphQL introspection on Storefront API | Informative — Intended | Introspection reveals types, not data. Use it to FIND real bugs |
| 2 | #3628961: Flow emails after staff removed | Informative — Intended | Flow workflows are store-owned, independent OAuth scopes |
| 3 | Staff sees customer data on orders | Informative — Intended | Orders permission = needs customer contact info |
| 4 | CDN files publicly accessible | Informative — Public by Design | CDN serves public assets; vuln = cross-tenant access |
| 5 | Opening Soon password bypass | Informative — Not a boundary | Documented as bypassable; not for real protection |
| 6 | CSRF on /cart/add.js | Informative — Intentionally Public | Cart is unauthenticated, public resource |
| 7 | Checkout URL standardized | Informative — By Design | Tokens are crypto-random; structure ≠ vulnerability |
| 8 | No rate limit on login | Informative — Insufficient Impact | Must PROVE successful brute-force credential compromise |
| 9 | Missing CSP on shopify.com blog | Informative — Best Practice | CSP only required where sensitive input processed (checkout) |
| 10 | Storefront API token in theme.js | Informative — Intentionally Public | Public tokens are scope-limited by design |
| 11 | Email verification token in URL | Informative — By Design | Standard across all platforms; single-use, time-limited |
| 12 | Stored XSS in product title | Informative — Self-XSS | Merchant injects into own store; no admin = no attack |
| 13 | Staff can export customer data | Informative — Intended | Customers permission = can export customer list |
| 14 | HSTS missing on blog.shopify.com | Informative — Not Exploitable | HSTS on critical paths (checkout, admin); MiTM impractical |
| 15 | B2B qty bypass via API | Informative — Expected Behavior | Client-side = UX only; server-side is the real boundary |
| 16 | /healthz on Hydrogen store | Informative — Standard Infra | Health endpoints required for LB monitoring; no sensitive data |
| 17 | Storefront events/actions public | Informative — Intended | Public JS API for app/theme developers |
| 18 | Deprecated REST API still works | Informative — Backward Compat | Authentication/authorization same across versions |
| 19 | Session tokens in browser memory | Informative — Expected | Tokens have 1-min TTL, encrypted, server-side validation |
| 20 | Customer API token in localStorage | Informative — Standard Storage | OAuth bearer token pattern; cross-origin isolation protects |

---

## 13. CHAIN ANALYSIS — ACCEPTED vs REJECTED

> A vulnerability is eligible if the FULL chain can be demonstrated. Each link must be a verifiable weakness.

| Chain | Standalone | Chained | Status |
|---|---|---|---|
| 1. Open redirect + OAuth | Open redirect (no impact) | Redirect steals authorization code → ATO | ELIGIBLE (H1 examples) |
| 2. CSRF logout + fixation | Logout CSRF (annoying) + session not rotated | XSS sets cookie + login keeps session → account takeover ($5K, H1-423136) | ELIGIBLE |
| 3. SSRF + cloud metadata | SSRF (external only) | Accesses 169.254.169.254 → IAM creds → cloud access | ELIGIBLE |
| 4. Rate bypass + brute-force | No rate limit (no impact) | Alias batching + cracked password → account takeover | ELIGIBLE (if cred compromise proven) |
| 5. Introspection + IDOR | Introspection (intended) | Discovers undocumented mutation w/ missing authz → data leak ($ bounty) | ELIGIBLE (IDOR is the vuln) |
| 6. Email verif bypass + cross-system trust | POS endpoint + Partner Dashboard trust | Change email w/o confirmation → create Shopify ID → full store takeover ($22.5K) | ELIGIBLE |

### When Chains Are NOT Accepted

1. **Theoretical chains:** Require unlikely victim actions, multiple unlikely steps
2. **Cross-program chains:** Require browser zero-days or non-Shopify vulns
3. **Physical access chains:** Attacker has device → all digital security bypassed
4. **Social engineering chains:** Calling support, phishing employees
5. **Missing prerequisite chains:** "If attacker already has admin access..."

### Chain Decision Tree

```
Found low-sev issue?
├── Can chain with ANOTHER Shopify vulnerability?
│   ├── YES → Demonstrate FULL chain attacker→impact
│   │   ├── Realistic (single victim click)? → REPORT full chain
│   │   └── Theoretical (multiple unlikely steps)? → DON'T REPORT
│   └── NO → Standalone impact sufficient?
│       ├── YES → Report as-is
│       └── NO → Abandon or hold for chaining
├── Requires third-party app vuln? → Report to app dev
├── Requires browser zero-day? → Not accepted
└── Requires physical/social eng? → Out of scope
```

---

## 14. SPECIFIC HUNTING PITFALLS

| Pitfall | Mistake | Consequence | Correct Approach |
|---|---|---|---|
| 1 | Test other merchants' stores | Ban + legal | Only test YOUR stores |
| 2 | Contact Shopify Support about bounty | Report closure + suspension | ALL comms via HackerOne |
| 3 | Test on production stores | Data corruption, fraud alerts | Use dev stores only |
| 4 | Report GraphQL introspection alone | Informative | Use introspection to FIND real bugs |
| 5 | Report rate limiting alone | Informative | PROVE successful brute-force |
| 6 | Report staff edge cases | Informative | Test if data EXCEEDS role scope |
| 7 | Report CDN XSS (isolated origin) | Informative | Prove cross-context impact |
| 8 | Report "reflected" XSS needing browser quirks | Informative | Test in standard browser, default settings |
| 9 | Report OAuth redirect without full chain | Informative | Demonstrate complete ATO chain |
| 10 | Report old patched CVEs | Duplicate | Check Known Issues + NVD + H1 disclosures first |

---

## 15. WHAT TRIAGE WANTS

### 5 Expectations

| # | What Triage Wants | Good Example | Bad Example |
|---|---|---|---|
| 1 | Clear reproduction steps | Store A: Create product "UNIQUE-VULN-TEST-A-12345". Store B: Request products.json?sku=TEST-B → returns Store A's product | "Go to admin, look at JSON, see other stores' data" |
| 2 | Impact demonstration | "Attacker with Products permission accesses /admin/api/.../customers.json → 10K+ customer records (PII). GDPR violation. €20M fine possible. CVSS 8.1" | "Someone could steal data. This is bad." |
| 3 | Two-account differential | Store A product "TEST-A-12345", Store B product "TEST-B-67890". Store A API returns Store B's product | Single account, no cross-tenant proof |
| 4 | Working PoC | Python script, Burp request file, HAR, <60s screen recording | "Try it and you'll see" / 20-page PDF |
| 5 | Concise reports | Title, 2-3 sentence summary, 3-5 sentence impact, steps, PoC, optional remediation | 20 pages background, multiple vulns in one report |

### Triage Timeline

| Stage | Timeframe | What Happens |
|---|---|---|
| Submission | Day 0 | Report submitted via HackerOne |
| Initial triage | 24-72h | Review for validity, scope, impact |
| Clarification | 1-7 days | If needed, team asks questions |
| Bounty decision | 1-4 weeks | Valid findings get bounty + severity |
| Fix development | 30-90 days | Fix for accepted findings |
| Public disclosure | After fix | 90-120 days post-fix |

### How to Get Best Response

1. **Right severity:** Use Shopify CVSS calculator at `shopify.github.io/appsec/cvss_calculator/`
2. **Be responsive:** Answer within 24h; silence = closure
3. **Be professional:** Polite tone → reputation boost
4. **Accept Informative gracefully:** One concise rebuttal max
5. **Keep learning:** Every Informative = learning opportunity

---

## 16. BY DESIGN — NOT VULNERABILITIES (40 ITEMS)

| # | Area | By-Design Status | What WOULD Be a Vulnerability |
|---|---|---|---|
| 1 | Admin Staff JSON Endpoints | Staff access `.json` with auth | Unauthenticated access; `.json` returns MORE than HTML; cross-tenant |
| 2 | CDN File Hosting | Public by design | Cross-tenant file access; cache poisoning DoS |
| 3 | GraphQL Introspection | Schema exposed (H1-2886723) | Schema contains secrets/PII; IDOR via discovered mutations |
| 4 | Opening Soon Password | Bypassable cosmetic gate | Protects admin resources |
| 5 | POS PIN (4-digit) | Retail convenience tradeoff | Remote bypass; programmatic bypass |
| 6 | HTML in Rich Text Editor | Merchant controls own content | Cross-tenant stored XSS |
| 7 | MCP Server Data Exposure | Tool discovery by design | Credentials/API keys/PII exposed; admin data without auth |
| 8 | Sidekick AI | Accesses own merchant data | Cross-tenant data leak; unauthorized actions via prompt injection |
| 9 | Storefront API Public Access | Public e-commerce design | Admin data access; unauthorized writes |
| 10 | Rate Limiting | Operational control, NOT security | Demonstrated successful brute-force/credential compromise |
| 11 | Email Verification at Signup | Optional for reduced friction | Unverified email accesses verified features |
| 12 | CORS on Public Endpoints | Required for headless | Admin endpoints with permissive CORS |
| 13 | Web Pixel Capabilities | Analytics/data access by design | Scope boundary bypass; sandbox escape |
| 14 | Checkout Kit WebView | Intended checkout surface | Cross-app data exfiltration; JWT forgery |
| 15 | Customer Account API | Customer sees own data | Cross-customer IDOR |
| 16 | Multi-Pass Accounts | Multi-store merchant feature | Token forgery or theft |
| 17 | Order Printer / Stocky | Separate app functionality | Cross-tenant data access |
| 18 | Staff Permissions | RBAC, role-necessary access | Data access BEYOND role scope |
| 19 | Hydrogen Health Endpoints | Standard infrastructure | Data leakage via health checks |
| 20 | Storefront API Tokens in JS | Public scope-limited tokens | Admin tokens with write scopes in client code |
| 21 | Cart AJAX Endpoints | Public by design (CORS: *) | Authenticated actions via cart; financial manipulation |
| 22 | Customer Account Token in localStorage | Standard OAuth pattern | Cross-origin token theft (XSS to steal token) |
| 23 | App Bridge Session Tokens | In-memory, 1-min TTL | Persistent storage; excessive TTL; forgeable signature |
| 24 | Legacy REST API | Backward compatibility | Legacy bypasses newer authz checks |
| 25 | Different API Versions | Intentional versioning | Version downgrade bypasses authz |
| 26 | Private App Tokens | Merchant's own credential | OTHER merchants' tokens found publicly |
| 27 | Sitemap Product URLs | SEO best practice | Hidden/draft products in sitemap |
| 28 | Script Tags on Storefront | Intended app feature | Unauthenticated script tag creation |
| 29 | App Proxy Storefront Context | Required for dynamic content | HMAC verification missing |
| 30 | Product JSON Endpoints | Public by design | Admin-only fields exposed |
| 31 | Monorail Telemetry | Event tracking by design | Telemetry leaks data to unauthorized parties |
| 32 | Well-Known Files | RFC/standard practice | Files expose sensitive URLs/credentials |
| 33 | Response Headers | HTTP protocol standard | Headers contain PII/session/credentials |
| 34 | Functions Sandbox | Security isolation (Wasm) | Sandbox escape; data access beyond input query scope |
| 35 | Web Pixel Sandbox | Anti-Magecart protection | Sandbox escape; DOM access; scope bypass |
| 36 | Checkout CSP Strict | PCI DSS compliance | CSP bypass allowing script injection |
| 37 | Customer Privacy API | Required for privacy compliance | API exposes PII via privacy methods |
| 38 | POS Transaction Events | Intented for app developers | Cross-tenant transaction data access |
| 39 | Shopify Magic AI | First-party admin feature | Data exfiltration via AI manipulation |
| 40 | Combined Listings / Bundles | Product grouping feature | Cross-store product association |

### The Golden Test (Before Reporting)

1. **Is the data INTENTIONALLY public?** Product catalog → Yes (by design). Customer PII → No (vuln). Admin settings → No (vuln).
2. **Is the accessor AUTHORIZED?** Staff w/ Orders viewing orders → Yes (by design). Unauthenticated visitor viewing admin → No (vuln).
3. **Is the MECHANISM the vuln, or did you USE it to find a vuln?** Introspection exists → Not a vuln. Introspection found IDOR → IDOR is the vuln.
4. **If fixed, would the platform break?** CDN private → Storefronts break → By design. Staff can't see order customer names → Fulfillment breaks → By design.

### Decision Matrix

```
FOUND SOMETHING?
├── In scope? (Section 9) → If NO: STOP
├── By design? (Section 16)
│   ├── YES → Crosses vuln threshold? → YES: REPORT | NO: DON'T
│   └── NO → Ineligible? (Sections 2-3)
│       ├── YES: DON'T REPORT
│       └── NO → Can chain realistically?
│           ├── YES (realistic): REPORT full chain
│           ├── YES (theoretical): DON'T REPORT
│           └── NO → Standalone impact sufficient?
│               ├── YES: REPORT as-is
│               └── NO: Abandon or hold for chaining
```

### Three-Step Verification Protocol

| Step | Test | Result |
|---|---|---|
| 1. Documentation | Search Shopify docs | Documented intentional → By design |
| 2. Authorization | Who accesses what? | Authorized → By design; Unauthorized → Vuln |
| 3. Impact | What can attacker DO? | Crosses security boundary → Vuln; Annoyance only → Not vuln |

### 10 Common Mistakes

1. Confusing "in scope for testing" with "not by design" — being allowed to test ≠ everything is a vuln
2. Confusing "interesting" with "vulnerable" — no rate limit = interesting; brute-force success = vuln
3. Confusing "by design" with "outdated design" — bad design ≠ vuln if intentional
4. Confusing "tenancy" with "privacy" — merchant's own data = theirs; cross-tenant = vuln boundary
5. Confusing "I can see it" with "it's exposed" — your own data = expected; others' data = vuln
6. Confusing "info disclosure" with "public info" — product prices = public; hidden data = disclosure
7. Confusing "missing control" with "missing boundary" — no rate limit = missing control; data exfil = missing boundary
8. Confusing "store content" with "platform content" — merchant's HTML = theirs; Shopify infra = vuln
9. Confusing "self-harm" with "cross-tenant attack" — own store = self-XSS; other stores = real vuln
10. Confusing "feature works as intended" with "security implications" — feature working = by design; exceeding scope = vuln

---

## APPENDIX A: TRIAGE RESPONSE CHEAT SHEET

| Your Report | Triage Response |
|---|---|
| Self-XSS in storefront | "Considered Self-XSS, requires merchant to inject. Informative." |
| GraphQL introspection | "Intentionally enabled. Intended behavior." |
| CDN file accessible | "CDN files are public by design. Informative." |
| Missing CSP header | "Endpoint intentionally lacks CSP. Informative." |
| Cart AJAX CSRF | "Cart endpoints are intentionally public. Informative." |
| Open redirect no chain | "No realistic attack vector. Informative." |
| Rate bypass no impact | "Must be accompanied by demonstrated access. Informative." |
| Plan limit race condition | "Plan limitations are out of scope." |
| Staff sees customer orders | "Orders permission requires this access. Intended." |
| Opening soon bypass | "Not a security boundary. Informative." |
| Storefront API token in JS | "Public tokens, scope-limited. Informative." |
| Email HTML injection | "Not exploitable in modern email clients." |
| Mobile API keys | "Public API keys, scope-limited. Informative." |
| Missing HSTS on subdomain | "Configured on primary domain. Not exploitable." |

---

## APPENDIX B: GLOSSARY

| Term | Definition |
|---|---|
| Self-XSS | Requires victim to paste code into console/dev tools |
| CSRF | Cross-Site Request Forgery — tricking user into action |
| CSP | Content Security Policy — controls script execution |
| CDN | Content Delivery Network — serves public static files |
| IDOR | Insecure Direct Object Reference — access via ID manipulation |
| SSRF | Server-Side Request Forgery — server requests internal resources |
| VDP | Vulnerability Disclosure Program — accepts non-bounty reports |
| HMAC | Hash-based Message Authentication — cryptographic webhook signature |
| JWT | JSON Web Token — signed token for auth |
| OAuth | Token-based authorization protocol |
| GraphQL | API query language — Shopify's primary API |
| REST | Representational State Transfer — Shopify's legacy API |
| GID | Global Identifier — `gid://shopify/Resource/ID` format |
| MFA | Multi-factor authentication |
| PII | Personally Identifiable Information |
| PCI DSS | Payment Card Industry Data Security Standard |
| TOTP | Time-based One-Time Password |
| SAML | Security Assertion Markup Language — SSO protocol |
| WebAuthn | Browser-based FIDO2/Passkey authentication |
| CORS | Cross-Origin Resource Sharing |
| MiTM | Man-in-the-Middle attack |
| UCP | Universal Commerce Protocol — Shopify's open agentic commerce protocol |
| MCP | Model Context Protocol — AI agent tool standard |

---

## APPENDIX C: RELATED READING

| Resource | URL |
|---|---|
| Shopify Bug Bounty | https://hackerone.com/shopify |
| Shopify Bounty Criteria | https://www.shopify.com/bugbounty/criteria |
| Shopify CVSS Calculator | https://shopify.github.io/appsec/cvss_calculator/ |
| Shopify Security Docs | https://shopify.dev/docs/apps/build/security |
| Shopify Known Issues | https://www.shopify.com/bugbounty/known-issues |
| HackerOne Core Rules | https://hackerone.com/organizations/shopify/policy |
| HackerOne Invalid Guide | https://docs.hackerone.com/en/articles/8477209 |

**Sources:** FINAL-HUNTING-REPORT-v2.md, developer-docs-complete.md, functions-apps-webhooks.md, cve-research.md, infrastructure-security.md, features-2026.md

---

## APPENDIX D: REVISION HISTORY

| Version | Date | Key Changes |
|---|---|---|
| 2.3 | 2026-08-08 | Compressed from 3550→~700 lines. All content preserved in condensed format. |
| 2.2 | 2026-08-06 | Corrected Section 9 scope: removed `*.myshopify.com` wildcard, `*.shopifycdn.com`, `*.shopifysvc.com` out; added `*.shopify.io`, `*.shopifykloud.com`, `*.shopifycs.com`, `*.pci.shopifyinc.com`, `arrive-server.shopifycloud.com`, `shop.app`, `shopify.plus`, Core vs Non-Core explanation. |
| 2.0 | 2026-07-12 | Complete rewrite, 11 sections, merged 7 recon files. Added cross-ref table, false positive patterns, domain scope, decision flowchart, pre-submit checklist. |
| 1.0 | 2026-06-01 | Initial version. |

---

> **If a feature works as documented, behaves as designed, and only accesses data the accessor is authorized to see — it is NOT a vulnerability.**
> 
> **By design:** Feature does what it was designed to do.
> **Vulnerability:** Feature does something it was NOT designed to do.

---

## APPENDIX E: TWO-STORE RULE

**The single most important rule for Shopify bug bounty:**

> **If you cannot demonstrate it using TWO stores you control, it is unlikely a valid vulnerability.**

| Vulnerability Type | Two-Store Test |
|---|---|
| Cross-tenant IDOR | Store A accesses Store B's data |
| Permission bypass | Limited-permission staff on YOUR store accessing beyond role |
| Auth bypass | Unauthenticated request to YOUR store returns auth-required data |
| Rate limit bypass | Brute-force credentials on YOUR store's login |
| Cache poisoning | Poison cache affecting YOUR store |
| MCP/AI issues | Prompt injection affecting YOUR data |

The two-store rule eliminates false positives from confusing "I can see my own data" with "I can see anyone's data."

---

*This is a research reference for bug bounty hunters targeting Shopify. It synthesizes data from official Shopify/HackerOne policies and independent security research. Always refer to the official HackerOne program page for the most current policies.*
