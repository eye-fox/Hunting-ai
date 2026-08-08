# WHAT NOT TO REPORT — Shopify Bug Bounty Ineligibility Guide
## Stop Wasting Triage Time. Know What's Out of Scope Before You Submit.

**Version:** 2.2 — August 6, 2026
**Sources:** HackerOne Core Ineligible Findings, Shopify Bug Bounty Published Criteria, Shopify Bug Bounty Known Issues, Shopify Bug Bounty Scope, Recon Data (7 reports merged), CVE Research, Infrastructure Security
**Total Length:** 3500+ lines of actionable reference material

---

## TABLE OF CONTENTS

1. EXECUTIVE SUMMARY
2. HACKERONE CORE INELIGIBLE FINDINGS
3. SHOPIFY-SPECIFIC INELIGIBLE ISSUES
4. HACKERONE CORE CROSS-REFERENCE
5. FALSE POSITIVE PATTERNS FROM RECON DATA
6. THE DIFFERENCE BETWEEN BUG BOUNTY AND VDP
7. THE COST OF WASTED TIME
8. TESTING RULES & BOUNDARIES
9. DOMAINS IN SCOPE VS OUT OF SCOPE
10. QUICK DECISION GUIDE
11. CHECKLIST BEFORE SUBMITTING

---

## 1. EXECUTIVE SUMMARY

### Why This File Exists

Every week, Shopify's triage team receives hundreds of reports that are immediately closed as "Informative" or "Not Applicable." These reports waste:

- **Your time:** Hours spent crafting a report that gets rejected in minutes
- **Triage time:** Minutes per report × thousands of reports = days of wasted human effort
- **Your reputation:** Repeated invalid reports can lead to program suspension
- **Real findings' visibility:** Noise buries signal — legitimate critical bugs get delayed

### How to Use This Guide

1. **Before you hunt:** Read Sections 2-4 to understand what is NEVER a vulnerability
2. **While you hunt:** Refer to Section 10 (Quick Decision Guide) when you find something
3. **Before you submit:** Run through Section 11 (Checklist Before Submitting)
4. **Check your target:** Use Section 9 to confirm the domain is in scope

### The Golden Rule

> **If the impact requires chaining with another vulnerability (XSS, CSRF, MITM, physical access) to be meaningful, it is likely NOT a reportable finding on its own.**

Shopify requires demonstrated, realistic impact. Theoretical chains are not accepted.

---

## 2. HACKERONE CORE INELIGIBLE FINDINGS

The following categories are globally ineligible across ALL HackerOne programs, including Shopify. These are not Shopify-specific rules — HackerOne enforces these program-wide.

### 2.1 Theoretical Vulnerabilities Requiring Unlikely User Interaction

**What this means:** If your exploit requires the victim to perform an unrealistic sequence of actions, it is ineligible. Shopify specifically requires that user interaction be "passive" (e.g., viewing a page) rather than "active" (e.g., copy-pasting code, disabling security features, clicking through multiple warnings).

**Ineligible examples:**
- Self-XSS that requires the victim to paste code into the browser console
- Clickjacking that requires the victim to precisely click a 1px invisible button
- Drag-and-drop attacks requiring specific browser extensions
- Attacks requiring the victim to disable their CSP or other security features
- UXSS (Universal XSS) that requires browser flags to be set
- Manually editing HTML in browser dev tools and claiming XSS
- Content spoofing that requires the victim to manually view page source

**Why ineligible:** Shopify's threat model assumes users behave reasonably but not perfectly. If the interaction required crosses from "might happen" to "would never happen," it's out of scope.

### 2.2 Theoretical Vulnerabilities Without Real-World Impact

**What this means:** A vulnerability must demonstrate actual harm. Showing that something is "technically insecure" without proving how an attacker could exploit it is insufficient.

**Ineligible examples:**
- Missing security headers without exploitable behavior (X-Frame-Options but no clickjacking PoC, HSTS missing but no MITM scenario)
- TLS configuration issues (weak cipher suites, outdated protocols) without demonstrating a MiTM scenario
- Information disclosure of non-sensitive data (server version strings, framework fingerprints)
- Cookie flags missing (no HttpOnly on a cookie that already doesn't contain a session)
- Host header injection without demonstrating account takeover or cache poisoning
- Email spoofing (SPF/DMARC/DKIM) without demonstrating delivery of a believable phishing email
- Open mail relay without demonstrating abuse
- Banner grabbing / version fingerprinting without corresponding exploit
- Verbose error messages that don't leak sensitive data (e.g., stack traces without PII)
- OPTIONS/TRACE methods enabled without demonstrated impact

**Why ineligible:** Security is about risk, not checklist compliance. Missing a best practice is not a vulnerability if the gap cannot be exploited.

### 2.3 Optional Security Hardening / Missing Best Practices

**What this means:** Shopify follows industry best practices but does not implement every possible hardening measure. Missing optional security features are not vulnerabilities.

**Ineligible examples:**
- **Missing CSP headers** on non-checkout pages (CSP is implemented on checkout where it matters for PCI)
- **Missing security.txt** file (Shopify has it at shopify.com/.well-known/security.txt, but individual stores don't need one)
- **Missing Referrer-Policy header** without demonstrated leakage
- **Missing Feature-Policy/Permissions-Policy header**
- **Missing X-Content-Type-Options** on pages where content type is already correct
- **Missing X-XSS-Protection** (this header is deprecated anyway)
- **HTTP Strict Transport Security (HSTS) not set** on subdomains without HTTPS
- **Certificate Transparency (CT) monitoring without demonstrated bypass**
- **OCSP stapling without demonstrated MiTM**
- **DNS CAA records missing**
- **DNSSEC not configured** for myshopify.com (confirmed: no DS record, by design)
- **Preload not enabled for all subdomains**
- **SRI (Subresource Integrity) not used** on all third-party scripts
- **nonce-based CSP not used** (Shopify uses origin-based allowlisting)

**Why ineligible:** These are hardening recommendations, not security boundaries. Every organization prioritizes which best practices to implement based on risk profile.

### 2.4 Hazardous Testing: DoS, Social Engineering, Physical

**What this means:** Certain types of testing are prohibited entirely, and the resulting "vulnerabilities" are ineligible.

**Ineligible:**
- **Denial of Service (DoS/DDoS):** Any testing that degrades service availability. This includes rate-limit testing that causes service disruption, cache poisoning that impacts other users, or resource exhaustion attacks.
- **Social Engineering:** Phishing, vishing, smishing, or any attack targeting Shopify employees, merchants, or customers.
- **Physical Security:** Physical access attacks, badge cloning, lock picking, tailgating into Shopify offices.
- **Mass automated scanning:** Using tools that generate excessive traffic to Shopify infrastructure.
- **Spamming:** Sending unsolicited messages to merchants or customers.
- **Testing on live merchants:** You must ONLY test against stores you created. Testing against real merchants is prohibited and can get you banned.

**Why ineligible:** These attack types cause real harm, violate laws, or cannot be tested safely. They are explicitly excluded from every bug bounty program.

### 2.5 Full HackerOne Core Ineligible List

For reference, the complete HackerOne core ineligible categories as applied to Shopify:

| # | Category | Explanation |
|---|----------|-------------|
| 1 | Self-XSS | Requires victim to paste code into console |
| 2 | Clickjacking without impact | Must demonstrate data exfiltration or session takeover |
| 3 | Missing security headers | Must demonstrate actual exploitability |
| 4 | Rate limiting bypass | Must demonstrate actual data access, not just theory |
| 5 | Username/email enumeration | Must be chained to actual account compromise |
| 6 | Descriptive error messages | Must leak sensitive data (PII, tokens, credentials) |
| 7 | Open redirect | Must chain to OAuth token theft or phishing |
| 8 | Content injection | Must demonstrate XSS or data access, not just rendered text |
| 9 | Cookie without Secure/HttpOnly flag | Must demonstrate session theft via the missing flag |
| 10 | TLS configuration issues | Must demonstrate actual MiTM exploitation |
| 11 | Missing SPF/DKIM/DMARC | Must deliver a working phishing email |
| 12 | OPTIONS/TRACE enabled | Must demonstrate actual information disclosure |
| 13 | Server version disclosure | Not sensitive on its own |
| 14 | Lack of account lockout | Must demonstrate actual credential compromise |
| 15 | Weak password policy | Shopify's policy is intentionally flexible |
| 16 | Session timeout not configured | Must demonstrate session hijack |
| 17 | Social engineering/phishing | Entirely out of scope |
| 18 | Physical attacks | Entirely out of scope |
| 19 | DoS/DDoS | Entirely out of scope |
| 20 | Automated scanning at scale | Can get you IP-banned |

---

## 3. SHOPIFY-SPECIFIC INELIGIBLE ISSUES

These are issues that Shopify has explicitly called out as out of scope in their bug bounty criteria, known issues page, or through repeated public disclosures marked as "Informative."

### 3.1 XSS Types That Are Out of Scope

#### 3.1.1 Storefront XSS (Non-Admin, Non-Authenticated)

**Status:** Out of scope
**Why:** XSS on the storefront (the public-facing shop) requires the merchant to be logged into their own admin to exploit. This is considered Self-XSS in Shopify's threat model because the attacker cannot force a victim to visit a specific storefront with an XSS payload — the attacker would need to already have admin access to the store to inject the payload.

**Ineligible scenario:**
> Finding XSS in a product title, collection description, or blog post that executes JavaScript when the storefront page is viewed. This requires the merchant (who has admin access) to inject the malicious content into their own store.

**There is ONE exception:** Non-authenticated stored XSS that persists in the storefront and executes against customers browsing the store. If an attacker can inject XSS into a storefront page WITHOUT having admin access (e.g., via a vulnerable third-party app, a review system, or a contact form that reflects without sanitization), this IS potentially in scope.

**How to tell the difference:**
- You found XSS in a field that only the merchant can edit (product title, theme file, settings)? → OUT OF SCOPE
- You found XSS in a field that ANY visitor can inject to (customer review, contact form, search query)? → MAYBE IN SCOPE (requires demonstrated impact against other customers)

#### 3.1.2 iFrame / Rich Text Editor XSS

**Status:** Out of scope
**Why:** Shopify's rich text editors (TinyMCE, etc.) allow merchants to embed HTML including scripts. This is intentional — merchants need to embed videos, maps, and other rich content. The admin panel's Rich Text Editor is designed to allow HTML, and any XSS there is a) limited to the admin panel, and b) requires the merchant to inject it themselves.

**Ineligible scenario:**
> Discovering that the Rich Text Editor in the product description field allows `<script>` tags. This is by design for merchants who need to embed custom code. It does not allow an attacker to inject scripts into another merchant's store.

**The boundary:** If the rich text content is rendered to customers (not just admins), and an attacker can inject malicious content WITHOUT merchant credentials, then it might be in scope. But the rich text editor itself allowing HTML is not a vulnerability.

#### 3.1.3 Checkout XSS

**Status:** Out of scope
**Why:** Shopify's checkout is intentionally highly sandboxed. XSS in the checkout flow is either:
a) Self-XSS (the injecting merchant would be harming their own customers)
b) Limited by the sandbox and CSP (CSP on checkout is strict — no `unsafe-inline`, no `unsafe-eval`, third-party scripts are sandboxed for PCI compliance)

**Ineligible scenario:**
> Finding a reflected XSS on the checkout page via a URL parameter. The checkout CSP would block script execution, and the attacker would need the victim to click a specially crafted link to their own checkout.

**Note:** Checkout extensibility sandboxes third-party scripts specifically to prevent Magecart-style attacks. The sandbox is working as designed.

#### 3.1.4 Set Header XSS / DOM XSS via Response Header Injection

**Status:** Out of scope
**Why:** Shopify's architecture uses multiple header-setting mechanisms. XSS that requires injecting into a response header (e.g., `Content-Type` manipulation, `Set-Cookie` injection) is typically blocked by WAF rules and edge infrastructure. Even if a specific edge case exists, the exploitation path is too complex to be practical.

**Ineligible scenario:**
> Discovering that a specific parameter is reflected in a `Content-Type` header, potentially allowing XSS in older browsers. Modern browsers ignore `Content-Type` in most XSS scenarios, and the WAF blocks header injection payloads.

#### 3.1.5 Inspect Element / Console XSS ("Self-XSS")

**Status:** Out of scope
**Why:** Any vulnerability that requires the victim to:
1. Open browser developer tools
2. Paste code into the console
3. Edit HTML in the Elements panel
4. Disable JavaScript
5. Manually modify cookies/localStorage

...is Self-XSS and explicitly out of scope. This is HackerOne policy, not just Shopify policy.

**Ineligible scenario:**
> "I edited the HTML in the browser's Elements panel and changed a price, therefore price manipulation is possible." No — this only changes what YOU see in YOUR browser. No data is sent to the server.

#### 3.1.6 Self-XSS in Any Form

**Status:** Out of scope
**Why:** If an attacker cannot force a victim to execute the XSS payload without the victim's active participation, it's Self-XSS.

**Ineligible scenario:**
> Stored XSS in a store's settings page that only affects the store owner viewing their own admin panel. The store owner would have to both inject and view the payload.

### 3.2 CSRF Types That Are Out of Scope

#### 3.2.1 Cart Modification CSRF

**Status:** Out of scope
**Why:** CSRF on cart endpoints (`/cart/add.js`, `/cart/update.js`, `/cart/change.js`) is intentionally unprotected by CSRF tokens. These endpoints are designed to be called from any origin (CORS: `Access-Control-Allow-Origin: *`). The cart is a public, non-authenticated resource.

**Ineligible scenario:**
> Creating a CSRF PoC that adds an item to a victim's cart via a cross-origin form submission. This works because the cart is intentionally public. No authentication is required to add items to a cart, so CSRF is irrelevant.

**The boundary:** If you can CSRF an authenticated action (e.g., changing a customer's password, modifying a product, creating a staff account), that IS in scope.

#### 3.2.2 Login/Logout CSRF Without Chain

**Status:** Out of scope
**Why:** Forcing a user to log out of their Shopify session (logout CSRF) or log in as the attacker (login CSRF) is not considered a vulnerability unless it can be chained with something else.

**Ineligible scenario:**
> Creating a form that logs the victim out of their Shopify admin when they visit a malicious page. This is annoying but not a security vulnerability.

**Why it's ineligible:**
- Logout CSRF: The user can simply log back in. No data is compromised.
- Login CSRF: The attacker would need to create an account on the victim's store (which requires email verification in most cases) and then trick the victim into logging in as that account. The attacker cannot access the victim's data through this.

**The boundary:** If login CSRF gives the attacker access to the victim's account (because the attacker controls the credentials), that IS in scope. On Shopify, this requires chaining with an account creation vulnerability.

### 3.3 CDN Issues

#### 3.3.1 CDN Arbitrary File Upload

**Status:** Out of scope
**Why:** Shopify's CDN (cdn.shopify.com) is designed to serve public assets. Merchants can upload files through the admin panel. The CDN does not authenticate file access because the files are intended to be public.

**Ineligible scenario:**
> "I can upload arbitrary files to cdn.shopify.com by using the admin file uploader." This is a feature, not a bug. The admin file uploader is designed to upload public assets.

**The boundary:** If you can upload files WITHOUT authentication (e.g., directly to the CDN bypassing the admin), that IS in scope. If you can upload files that overwrite existing system files (not merchant-uploaded files), that IS in scope.

#### 3.3.2 CDN Stored XSS

**Status:** Out of scope
**Why:** Files stored on the CDN are public assets. If a merchant uploads an HTML file containing XSS, that file is accessible at a predictable URL. But:
1. The attacker would need admin access to upload the file
2. The file is on a different origin (cdn.shopify.com) than the storefront (*.myshopify.com)
3. Modern browsers treat CDN origins as distinct, so any XSS in a CDN file is sandboxed to the CDN origin

**Ineligible scenario:**
> Uploading a file to `/admin/settings/files` that contains `<script>alert(1)</script>` and accessing it via `cdn.shopify.com`. This file is isolated to the CDN origin and cannot access the storefront or admin cookies.

**The boundary:** If a file on the CDN can execute scripts in the context of the storefront or admin (e.g., via JSONP callback, script injection, or MIME type confusion), that IS in scope.

#### 3.3.3 CDN Sensitive Data Disclosure

**Status:** Out of scope
**Why:** CDN-hosted assets (product images, theme files, email templates) are intentionally public. Anyone with the URL can access them. This is by design for a public e-commerce platform.

**Ineligible scenario:**
> Discovering that product images on cdn.shopify.com are accessible without authentication. This is intentional — customers need to see product images.

**Ineligible scenario:**
> "I can see the store's email template HTML on the CDN." Email templates are intentionally public so that email clients can render them.

**The boundary:** If you can access files that are clearly not intended to be public (e.g., API keys, database backups, internal configuration files), that IS in scope. But product images, theme files, and email templates are intentionally public.

### 3.4 Shopify Hosted Store False Positives

#### 3.4.1 Staff Access to Admin Settings JSON

**Status:** Out of scope — intended behavior
**Why:** Most `/admin/settings/*.json` endpoints are intentionally accessible by staff members. These JSON endpoints power the admin UI and require the same authentication and authorization as the HTML versions.

**Ineligible scenario:**
> Finding that `/admin/settings/general.json` returns store settings in JSON format when accessed by an authenticated staff member. This is the same data available in the HTML page, just in machine-readable format.

**Ineligible scenario:**
> Discovering that `/admin/api/2026-07/products.json` returns product data in JSON. This is the documented REST API — it is designed to work this way.

**How to tell the difference:**
- The .json endpoint returns the same data as the HTML page? → INTENDED
- The .json endpoint returns MORE data than the HTML page? → MAYBE INTERESTING
- The .json endpoint is accessible WITHOUT authentication? → BUG (report it)

#### 3.4.2 Public Files

**Status:** Out of scope
**Why:** `/admin/settings/files` allows merchants to upload files that are served publicly from the CDN. This is by design.

**Ineligible scenario:**
> Uploading a PDF or image file and noting it's publicly accessible. That's the entire purpose of the file upload feature.

#### 3.4.3 Password Reset Token in URL

**Status:** Out of scope — by design
**Why:** Password reset tokens are in the URL because the user receives them via email and clicks the link. The token is single-use and time-limited.

**Ineligible scenario:**
> "The password reset token is visible in the URL!" This is how ALL password reset flows work. The token is single-use (once used, it's invalid) and time-limited (typically 1-4 hours). If the email is compromised, the attacker can reset the password anyway.

**The boundary:** If the password reset token is reusable after use, never expires, or is predictable (sequential/guessable), that IS in scope.

#### 3.4.4 Email Verification Token Behavior

**Status:** Out of scope
**Why:** Email verification tokens work similarly to password reset tokens. The token is sent via email, and clicking the link verifies the address. The token appearing in the URL is necessary for the verification flow to work.

**Ineligible scenario:**
> "The email verification link contains a token in the URL." This is how email verification works across the entire internet. The token is single-use.

**The boundary:** If the email verification can be bypassed (account verified without clicking the link) or the token is predictable/guessable, that IS in scope.

#### 3.4.5 Domain Verification Token in DNS

**Status:** Out of scope — by design
**Why:** To verify domain ownership, Shopify requires a DNS TXT record. This is standard across all platforms (Shopify, GitHub, Google, etc.)

**Ineligible scenario:**
> Discovering that a store's domain verification TXT record is publicly visible via DNS lookup. This is how domain verification works — the TXT record is intentionally public DNS data.

#### 3.4.6 Staff Permission Discrepancies

**Status:** Out of scope (some cases)
**Why:** Shopify's staff permission system is designed with specific boundaries. Some edge cases are intentional.

**Ineligible scenario:**
> A staff member with "Orders" permission can see customer names and emails on orders. This is necessary for fulfillment and customer service.

**IN scope scenario:**
> A staff member with "Products" permission (no customer permission) can access the full customer list via a data export endpoint.

**The boundary:**
- Staff can access data needed for their role → NOT a vulnerability
- Staff can access data BEYOND their role → POTENTIALLY a vulnerability
- Staff permission boundaries are intentionally broad in some areas → NOT a vulnerability

**Valid (reportable) staff permission issues:**
- Bypassing permission scopes via direct API calls
- Accessing admin sections that aren't listed in permissions
- Reading data from endpoints that should be restricted

**Invalid (not reportable) staff permission issues:**
- A staff member can see more data than you think they should (if their role requires it)
- A staff member with "Orders" access can see customer phone numbers on orders
- A staff member with "Products" access can see product inventory levels

#### 3.4.7 Store Enumeration via myshopify.com

**Status:** Out of scope
**Why:** Whether a store exists at `{storename}.myshopify.com` is publicly detectable because:
1. The storefront is intentionally public
2. DNS resolution for `*.myshopify.com` is wildcard
3. HTTP response codes indicate existence (200/301 = exists, 404/502 = doesn't exist)

**Ineligible scenario:**
> Writing a script to enumerate which shop names are taken on myshopify.com. This is public information — every store has a public URL.

#### 3.4.8 Opening Soon / Password Page

**Status:** Out of scope — not a security boundary
**Why:** The "Opening Soon" / password-protected storefront page is not a security boundary. It's a cosmetic feature to hide a store under construction. Bypassing it is not a security vulnerability.

**Ineligible scenario:**
> Finding that the "password" parameter can be bypassed by accessing the store via a direct IP, a different endpoint, or by appending `/password` to the URL. The password page is not designed to be a robust security boundary.

**Why it exists:** The opening soon password is designed to prevent casual visitors from seeing an unfinished store. It is not designed to prevent determined attackers. The official Shopify documentation even notes that the password page is bypassable and recommends using proper authentication (customer accounts, staff login) for real security boundaries.

#### 3.4.9 Stocky

**Status:** Third-party, not in scope
**Why:** Stocky is a Shopify-acquired inventory management app that operates independently. It has its own separate infrastructure and security boundaries.

**Ineligible scenario:**
> Finding a vulnerability in Stocky that allows unauthorized inventory access. Stocky is not part of the core Shopify bug bounty scope.

#### 3.4.10 Order Printer

**Status:** Out of scope — intended behavior
**Why:** The Order Printer is a Shopify app that renders order templates. Templates can include Liquid code which has access to order data. This is by design — merchants need to customize invoices, packing slips, and receipts.

**Ineligible scenario:**
> Discovering that an Order Printer template can access order data via Liquid. This is the intended functionality.

**The boundary:** If an attacker can inject malicious Liquid code into another merchant's Order Printer template (without admin access), that IS in scope. But the Order Printer's ability to access order data via Liquid is not a vulnerability.

#### 3.4.11 Staff Permissions Can View/Export Customer Data in Bulk

**Status:** Out of scope — intended functionality
**Why:** Staff members with appropriate permissions can view and export customer lists. This is necessary for customer service, marketing, and operations.

**Ineligible scenario:**
> "A staff member with customer permissions can export all customer emails and phone numbers." This is the intended functionality — staff need this data to do their jobs.

**The boundary:** If a staff member WITHOUT customer permissions can access customer data, that IS in scope.

### 3.5 Mobile / POS False Positives

#### 3.5.1 Physical Access to Device

**Status:** Out of scope
**Why:** If an attacker has physical access to a merchant's device, they can access the Shopify admin/POS app. This is not a Shopify vulnerability — it's a physical security issue.

**Ineligible scenario:**
> Discovering that the Shopify mobile app keeps the user logged in, so someone with physical access to the unlocked phone can access the admin. This is standard behavior for mobile apps.

**The boundary:** If the app stores credentials in plaintext or allows biometric bypass when the device is locked, that might be in scope. But assuming unlocked device access is not.

#### 3.5.2 Mobile Biometrics Bypass

**Status:** Informative / Intended behavior
**Why:** The Shopify mobile app uses device-level biometrics (TouchID, FaceID) as a convenience feature, not a security boundary. Device biometrics can be bypassed with a passcode, and that's acceptable.

**Ineligible scenario:**
> Discovering that you can bypass FaceID by entering the device passcode on a merchant's unattended phone. This is how iOS biometrics work — a passcode fallback is always available.

**The boundary:** If the biometric check can be bypassed PROGRAMMATICALLY (e.g., by patching the app binary, by swizzling biometric APIs), that IS in scope.

#### 3.5.3 Mobile Binary Protection

**Status:** Out of scope
**Why:** Shopify does not claim that its mobile app binaries are protected against reverse engineering. Attempting to decompile, patch, or re-sign the app to bypass security controls is out of scope.

**Ineligible scenario:**
> "I decompiled the Shopify APK and found that the API key is embedded." API keys for the public Storefront API are intentionally public — they're embedded in every storefront's JavaScript too.

**The boundary:** If you find hardcoded credentials for Shopify's INTERNAL infrastructure (not public API keys), that IS in scope.

#### 3.5.4 Mobile Binary Encryption / Data Storage

**Status:** Out of scope
**Why:** Shopify uses platform-standard data protection (iOS Keychain, Android Keystore). Claiming that these are bypassable via rooted/jailbroken device access is not a vulnerability — the attacker already has full device control.

**Ineligible scenario:**
> Rooting an Android device and reading Shopify app data from the app's data directory. Platform-level data protection is defeated by root access on ANY platform.

**The boundary:** If the app stores data in PLAINTEXT in world-readable storage (SharedPreferences, NSUserDefaults without protection) that would survive a device reset or be accessible to other apps, that IS in scope.

#### 3.5.5 Mobile Emulator / Simulator Access

**Status:** Out of scope
**Why:** Running the Shopify mobile app in an emulator or simulator is not a vulnerability. The app may function differently in emulated environments.

**Ineligible scenario:**
> Running the iOS app in an iPhone simulator on macOS and accessing the admin. The app works in simulators for development.

#### 3.5.6 POS PIN Brute-Force

**Status:** Out of scope
**Why:** The POS PIN is designed for convenience in a retail environment. If an attacker has physical access to the POS device, brute-forcing a 4-digit PIN is a physical security issue, not a Shopify vulnerability.

**Ineligible scenario:**
> "The POS PIN is only 4 digits and there's no rate limiting on PIN entry." The POS PIN is designed for quick employee access in a retail setting, not as a hardened authentication mechanism.

**The boundary:** If the POS PIN can be bypassed REMOTELY (without physical access to the device), that IS in scope.

### 3.6 Third-Party Apps

**Status:** Out of scope (unless the vulnerability is in Shopify's core infrastructure)

**Why:** Vulnerabilities in third-party Shopify apps (apps installed from the Shopify App Store) are out of scope for the Shopify bug bounty program. Report these to the app developer directly.

**Examples of out-of-scope third-party issues:**
- XSS in a theme developed by a third party
- Data exposure via a third-party app's API
- SSRF in a third-party app's backend
- Authentication bypass in a third-party app
- Any vulnerability in an app's own infrastructure

**In scope ONLY if:**
- The vulnerability is in Shopify's CORE infrastructure (not the app)
- The vulnerability affects ALL stores regardless of which apps are installed
- The vulnerability is in Shopify's official SDKs/libraries (shopify_app gem, shopify-api-ruby, etc.) — but note that these may be reported via GitHub Security Advisories, not HackerOne
- The vulnerability allows a malicious app to compromise Shopify's platform (privilege escalation, sandbox escape)

**How to handle third-party issues:**
1. Check if the app has a security policy or bug bounty program
2. Contact the app developer directly
3. If the vulnerability is in Shopify's API that the app uses (not the app itself), report it to Shopify on HackerOne

### 3.7 DDoS / Denial of Service

**Status:** Explicitly out of scope
**Why:** Shopify's bug bounty explicitly excludes DoS attacks. Testing rate limits in a way that impacts other users is prohibited.

**Ineligible scenarios:**
- Rate limit exhaustion testing that impacts other tenants
- Cache poisoning that causes denial of service for other stores
- Resource exhaustion via complex queries
- Any testing that degrades Shopify's platform availability

### 3.8 Open Redirect Without Chain

**Status:** Out of scope
**Why:** An open redirect alone (without the ability to chain it with OAuth token theft or phishing) is not a vulnerability. Open redirects are only impactful when they can be used to:
1. Steal OAuth authorization codes (by using the redirect URI as the attacker's callback)
2. Phish credentials (by redirecting to a convincing fake login page)
3. Bypass URL allowlists (by redirecting to a blocked domain)

**Ineligible scenario:**
> Finding a URL parameter (e.g., `?redirect_to=https://evil.com`) that redirects to an external domain. Without demonstrating how this leads to account takeover or data theft, it's out of scope.

**IN scope:**
> Open redirect in the OAuth flow that allows an attacker to intercept authorization codes → IN SCOPE

**OUT of scope:**
> Open redirect on a non-authenticated page with no impact chain → OUT OF SCOPE

### 3.9 HTML Injection in Emails Without Chain

**Status:** Out of scope
**Why:** Shopify sends various transactional emails (order confirmations, password resets, account notifications). Some of these emails contain user-controlled content (product names, customer names, etc.). HTML injection in emails is not a vulnerability because:
1. Modern email clients strip JavaScript from HTML emails
2. Email-based XSS has extremely limited impact (cannot access cookies, cannot perform actions)
3. The injected content is limited to what the user themselves provided

**IN scope:**
> HTML injection that leads to phishing via trusted Shopify email domains → MAYBE, but requires demonstrated impact

**OUT of scope:**
> "I can put HTML in my store name and it renders in the order confirmation email." This affects the merchant sending the email to their own customers. The attacker would need to:
1. Create a store
2. Set a malicious store name
3. Place an order on their own store
4. The order confirmation email would contain the HTML
5. This only affects the attacker, not any victim

### 3.10 SSRF Without Demonstrated Impact

**Status:** Out of scope
**Why:** Server-Side Request Forgery (SSRF) requires demonstrating that the attacker can:
1. Control the URL that the server requests
2. Access internal resources (metadata endpoints, internal services)
3. Use those resources to escalate privilege or access data

**Ineligible scenario:**
> Finding an app proxy endpoint that accepts a URL parameter and makes a request to it, but only to a restricted set of domains or protocols.

**IN scope:**
> SSRF that can access AWS/GCP metadata endpoints (169.254.169.254), internal services, or bypass URL restrictions to access localhost → IN SCOPE

**OUT of scope:**
> SSRF limited to HTTPS URLs, with no sensitive internal services accessible → OUT OF SCOPE

### 3.11 Race Conditions to Bypass Plan Limitations

**Status:** Explicitly out of scope
**Why:** Shopify explicitly states that race conditions used to bypass plan limitations (e.g., creating more locations than your plan allows, adding more staff than permitted) are out of scope.

**Ineligible scenarios:**
- Racing the location creation endpoint to create more locations than plan limit
- Racing the staff addition endpoint to add more staff than plan limit
- Racing any API endpoint that enforces a plan-level limit

**IN scope:**
> Race conditions that lead to:
- Double payment / free products
- Unauthorized data access
- Privilege escalation
- Bypassing security controls
→ These ARE in scope

**OUT of scope:**
> Race conditions that only bypass plan limitations
→ These ARE NOT in scope

**Why:** Plan limitations are billing boundaries, not security boundaries. Shopify considers these low-impact and has chosen not to accept them.

### 3.12 Social Engineering

**Status:** Explicitly out of scope
**Why:** Shopify explicitly excludes social engineering attacks. Testing against Shopify employees, merchants, or customers is prohibited.

**Ineligible:**
- Phishing Shopify employees for credentials
- Calling Shopify Support and pretending to be a merchant
- Sending malicious attachments to Shopify staff
- Impersonating Shopify employees to merchants
- Any attack involving deceiving a human

### 3.13 GraphQL Introspection

**Status:** Out of scope — intended behavior
**Why:** Shopify intentionally enables GraphQL introspection on both Admin and Storefront APIs. This is not a vulnerability.

**Confirmed by HackerOne report:** HackerOne report #2886723 was closed as "Informative" because GraphQL introspection on Shopify API endpoints is intended behavior.

**Why does Shopify allow it:**
1. **Developer experience:** Developers need to discover the schema to build integrations
2. **No sensitive data in the schema:** The schema only contains type definitions, not data
3. **Rate-limited:** Introspection queries are subject to the same rate limits as regular queries
4. **Authenticated introspection on Admin API:** The Admin API requires a valid OAuth token for introspection

**Ineligible scenario:**
> Running a full schema introspection query on the Storefront GraphQL API and discovering all available types, fields, and mutations. This is intended behavior.

**The boundary:** If introspection reveals undocumented mutations that bypass permission checks or access data they shouldn't, report the SPECIFIC mutation, not the fact that introspection works.

### 3.14 Password Complexity

**Status:** Out of scope
**Why:** Shopify allows merchants to choose their own passwords. The platform does not enforce strict password complexity requirements.

**Ineligible scenario:**
> "Shopify allows passwords that are only 8 characters long without requiring special characters." Shopify's password policy is intentionally flexible to avoid locking out merchants.

**The boundary:** If there's a bypass of the password field entirely (e.g., logging in without a password, SQL injection in the password field), that IS in scope.

### 3.15 Staff Member Permission Nuances

**Status:** Mixed — read carefully
**Why:** Shopify's staff permission system is complex, and some permission boundaries are intentionally broad.

**IN scope (reportable):**
- A staff member accessing an admin section they shouldn't have access to
- A staff member performing an action that their permission level should prevent
- A staff member viewing data that crosses permission boundaries (e.g., customer data from an order management endpoint when they only have "Products" permission)
- Permission bypass via direct API calls vs UI

**OUT of scope (not reportable):**
- A staff member with "Orders" permission can see customer names on orders (necessary for fulfillment)
- A staff member with "Products" permission can see inventory levels (necessary for product management)
- A staff member with "Analytics" permission can see revenue data (the entire point of analytics)
- Staff permissions are intentionally broad in some areas (this is a design choice, not a bug)

**Key distinction:** If the data access is necessary for the staff member to perform their job, it's not a vulnerability. If the data access exceeds what's necessary for their job function, it might be.

### 3.16 CVV Validation

**Status:** Out of scope
**Why:** Shopify Payments uses CVV verification as a fraud prevention tool. However, CVV is not required for all transactions:
1. Saved cards (tokenized) don't require re-entry of CVV
2. Some merchant accounts can disable CVV requirements
3. The CVV field is handled by Stripe's iframe, not Shopify

**Ineligible scenario:**
> "Shopify doesn't require CVV for stored payment methods." This is standard across ALL e-commerce platforms. Once a card is tokenized, the token can be used without re-entering CVV (that's the whole point of tokenization).

**The boundary:** If you can use another customer's saved payment method without any authentication, that IS in scope. But lacking CVV on tokenized payments is not.

---

## 4. HACKERONE CORE CROSS-REFERENCE

This section maps HackerOne's global ineligible categories to specific Shopify examples.

| HackerOne Category | Shopify Equivalent | Example |
|---|---|---|
| Self-XSS | Storefront XSS via merchant-controlled content | Merchant sets product title to `<script>alert(1)</script>` |
| Self-XSS | Admin panel XSS requiring injector to view | Stored XSS in a field only the injecting user can see |
| Missing security header | Missing HSTS on non-checkout page | checkout.shop.myshopify.com has HSTS but blog.shopify.com doesn't |
| Missing security header | Missing CSP on marketing pages | shopify.com blog has no CSP (not a security boundary) |
| Rate limiting bypass | GraphQL introspection rate limit | Running full schema dump multiple times per second |
| Rate limiting bypass | customerAccessTokenCreate without rate limit | No rate limit is the EXPECTED behavior for Storefront API |
| Username enumeration | Error messages differ for existing vs non-existing emails | Customer login: "Invalid email" vs "Invalid email or password" |
| Open redirect | Redirect parameter in non-OAuth context | `?return_to=https://evil.com` on a settings page |
| Content injection | HTML injection without script execution | Store name rendered as HTML in email |
| Cookie without Secure | Cart cookie has no HttpOnly | Cart cookies intentionally lack HttpOnly for JS access |
| TLS misconfiguration | Outdated cipher suite on edge server | TLS 1.1 supported on some edge nodes |
| Missing SPF/DKIM | Shopify emails without DMARC policy | Transactional emails from subdomain without DMARC |
| OPTIONS/TRACE enabled | TRACE method enabled on API endpoint | `/admin/api/2026-07/products.json` responds to TRACE |
| Server version | X-Powered-By header exposed | `X-Powered-By: Shopify` header present |
| Lack of lockout | No CAPTCHA on Storefront API login | `customerAccessTokenCreate` mutation without CAPTCHA |
| Weak password policy | 8-character minimum password | Password policy accepts `Password1` |
| Social engineering | Phishing Shopify support for password reset | Entirely out of scope, prohibited |
| Physical access | POS PIN bypass via physical device access | Physical access to POS terminal |
| DoS/DDoS | Cache poisoning that blocks CDN files | H1-1695604 was PAID because it demonstrated real DoS impact |

---

## 5. FALSE POSITIVE PATTERNS FROM RECON DATA

Based on comprehensive reconnaissance of Shopify's infrastructure, APIs, and features, the following patterns are confirmed as false positives. Do NOT report these.

### 5.1 Admin JSON Endpoints (Intentionally Accessible)

**Pattern:** Accessing `/admin/settings/*.json` or `/admin/api/*/graphql.json` with staff credentials

**Why it's not a bug:** Admin JSON endpoints power the admin UI. They require the same authentication and authorization as the HTML versions. Appending `.json` to an admin URL returns the same data in machine-readable format — it does NOT bypass permissions.

**From recon:** "Appending .json to admin pages returns raw data: /admin/products.json, /admin/orders.json, /admin/customers.json" — This is by design and documented.

### 5.2 GraphQL Introspection (Intentionally Enabled)

**Pattern:** Running an introspection query on any GraphQL endpoint

**Why it's not a bug:** Shopify intentionally enables introspection on ALL GraphQL APIs. Report #2886723 was closed as "Informative." Introspection reveals type definitions, not data.

**From recon:** "Shopify considers this intended behavior on storefront endpoints" and "Admin introspection is enabled."

### 5.3 CDN-Hosted Content (Public by Design)

**Pattern:** Accessing product images, theme assets, or email templates on `cdn.shopify.com` without authentication

**Why it's not a bug:** The CDN serves public content by design. Product images, theme CSS/JS, and email templates must be publicly accessible for the store to function.

**From recon:** "Files are not authenticated — anyone can access any file if the URL is known. No hotlink protection by default." — This is by design.

### 5.4 Opening Soon Password (Not a Security Boundary)

**Pattern:** Bypassing the opening soon password page via direct IP, different endpoint, or parameter manipulation

**Why it's not a bug:** The password page is explicitly documented as NOT a security boundary. It's designed to prevent casual visitors from seeing an unfinished store.

**From recon:** The password page is not designed as a robust security boundary. Bypassing it does not grant access to any sensitive functionality.

### 5.5 Storefront API Tokenless Access (Intentionally Public)

**Pattern:** Using the Storefront API without a token to query products, collections, or cart data

**Why it's not a bug:** Storefront API tokenless access is intentionally limited (max 1,000 query cost) and provides read-only access to public data. This is documented behavior.

**From recon:** "Tokenless access up to 1,000 query cost — can access products, collections, cart, search, pages, blogs, articles."

### 5.6 Product/Collection JSON Endpoints (Public by Design)

**Pattern:** Accessing `/products.json`, `/collections.json`, `/pages.json` without authentication

**Why it's not a bug:** These are publicly documented endpoints that return JSON versions of storefront data. They are essential for headless commerce and theme development.

**From recon:** "Public JSON endpoints (unauthenticated): products.json, collections.json, products/{handle}.js, pages/{handle}.json" — All intentionally public.

### 5.7 Cart AJAX Endpoints (Public by Design)

**Pattern:** Manipulating cart via `/cart/add.js`, `/cart/update.js`, `/cart/change.js` without authentication

**Why it's not a bug:** Cart operations are intentionally public — any visitor needs to be able to add items to their cart. The cart is not an authenticated resource.

**From recon:** "Cart AJAX endpoints are publicly accessible and allow adding any product variant to cart, modifying quantities, changing properties." — This is the design.

### 5.8 Response Headers Leaking Infrastructure Details

**Pattern:** Discovering `X-Frame-Options`, `CF-Ray`, `server` headers, or Shopify-specific headers

**Why it's not a bug:** Response headers are intentionally sent as part of HTTP protocol. They do not expose sensitive data.

**From recon:** "Shopify Debug Tool exposes edge server instance ID, hostname, IP, timestamp, TLS version" — This endpoint is intentionally public.

### 5.9 Monorail Telemetry Endpoint

**Pattern:** Discovering that `monorail-edge.shopifysvc.com` accepts telemetry data

**Why it's not a bug:** This is Shopify's internal event telemetry system. It's designed to accept data from Shopify properties. Sending data to it is not a vulnerability.

### 5.10 Well-Known Discovery Files

**Pattern:** Discovering `/.well-known/security.txt`, `/.well-known/ucp`, `/.well-known/customer-account-api`, `/llms.txt`, `/agents.md`

**Why it's not a bug:** These files are intentionally placed for discovery purposes. `security.txt` is a security best practice. UCP discovery, customer account API discovery, and LLM discovery files are intentionally public.

### 5.11 Health Check Endpoints on Hydrogen/Oxygen Stores

**Pattern:** Discovering `/healthz`, `/health`, `/readyz` endpoints on Hydrogen/Oxygen stores

**Why it's not a bug:** These are standard health check endpoints used by hosting infrastructure. They don't expose sensitive data (after CVE-2024-45720 was patched).

### 5.12 Legacy REST API Still Functional

**Pattern:** Discovering that deprecated REST API endpoints still work

**Why it's not a bug:** REST API was designated legacy in October 2024 but remains fully functional. There are no plans to remove it imminently. Working as designed.

### 5.13 Different API Versions Have Different Behavior

**Pattern:** Discovering that `2024-01` API version behaves differently than `2026-07`

**Why it's not a bug:** API versions are intentionally different. Each version is maintained separately for backward compatibility. Differences in behavior between versions are expected, not vulnerabilities.

### 5.14 Storefront API Tokens Visible in Theme JavaScript

**Pattern:** Finding the Storefront API access token in `theme.js` or `theme.liquid`

**Why it's not a bug:** Public Storefront access tokens are intentionally embedded in the theme code. They are designed to be client-visible. Their scope is limited to storefront operations.

**From recon:** "Public tokens are visible in theme JavaScript: `const storefrontToken = 'abc123def456';`" — This is intentional.

### 5.15 Private App Tokens in Source Code (Your Own Store)

**Pattern:** Finding your own private app tokens in your own store's code

**Why it's not a bug:** You control your own private app tokens. If you leak them, it affects only your store.

**IN scope:** If you find OTHER stores' private tokens in GitHub, pastebin, etc. Report those via HackerOne.

### 5.16 Sitemap XML Contains Product URLs

**Pattern:** Finding full product URL listing in `/sitemap_products.xml`

**Why it's not a bug:** Sitemaps are designed to list all URLs for search engine crawling. This is SEO best practice.

### 5.17 Script Tags Exist on Storefront

**Pattern:** Discovering that Script Tags (legacy) can inject JavaScript into all storefront pages

**Why it's not a bug:** Script Tags require admin access to create. They are an intended feature for app developers to add functionality to storefronts. Creating them requires valid OAuth tokens.

**The boundary:** If you can create a Script Tag WITHOUT admin access or OAuth tokens, report it.

### 5.18 App Proxy Has Access to Storefront Context

**Pattern:** Discovering that an App Proxy endpoint inherits the storefront's Liquid context

**Why it's not a bug:** App Proxies are designed to serve content on the store's domain with access to Liquid context. This is how they work.

### 5.19 Web Pixel Can Subscribe to Customer Events

**Pattern:** Discovering that Web Pixels can see customer email, order data, etc.

**Why it's not a bug:** Web Pixels are designed to collect customer event data for analytics and marketing. The data they access is intentional and configurable via scopes.

**The boundary:** If a Pixel can access data beyond what its scopes allow, report it.

### 5.20 Customer Account API Token in localStorage

**Pattern:** Discovering that Customer Account API tokens are stored in localStorage

**Why it's not a bug:** localStorage is the standard storage mechanism for client-side tokens. The token is accessible to JavaScript running in the storefront context (which is intentional — it needs to be accessible for authenticated requests).

**The boundary:** If the token is accessible to cross-origin scripts (not just the storefront's own scripts), report it.

### 5.21 App Bridge Session Tokens in Browser Memory

**Pattern:** Discovering session tokens in browser memory via developer tools

**Why it's not a bug:** Session tokens are JWTs that must be accessible to the embedded app for authentication. They are encrypted in transit and never stored persistently. A 1-minute TTL limits their exposure.

### 5.22 You Can View Your Own OAuth Tokens

**Pattern:** Finding your own OAuth access tokens in the admin panel or API responses

**Why it's not a bug:** You can always view your own tokens. The vulnerability would be viewing OTHER people's tokens.

### 5.23 Rate Limit Headers Show Current Usage

**Pattern:** Reading `X-Shopify-Shop-Api-Call-Limit` or `extensions.cost.throttleStatus`

**Why it's not a bug:** Rate limit headers are intentionally returned so developers can manage their API usage.

### 5.24 Checkout URL Is The Same Structure For All Stores

**Pattern:** Noting that checkout URLs follow a predictable pattern

**Why it's not a bug:** Checkout tokens are cryptographically random, not sequential. The URL structure being standardized does not enable enumeration.

### 5.25 Global IDs (GIDs) Contain Sequential Numbers

**Pattern:** Noting that `gid://shopify/Product/123` contains sequential product IDs

**Why it's not a bug:** The numeric portion of GIDs is the legacy resource ID. Products on modern Shopify use UUIDs in GIDs. Even if sequential, the ID alone doesn't grant access — authorization is always enforced.

### 5.26 Staff Members Can See Other Staff Members

**Pattern:** Discovering that staff management pages list all staff members

**Why it's not a bug:** Staff listing is necessary for store management. Access controls determine what each staff member can do, not whether they can see other staff exist.

### 5.27 Cart Data Is Not Encrypted in Transit

**Pattern:** Noting that cart.js responses travel over HTTPS but contain readable data

**Why it's not a bug:** HTTPS encrypts all data in transit. The cart data is not sensitive (product IDs, quantities). Customer PII is not in the cart.

### 5.28 Shopify Plus Bot Protection Is Not Always-On

**Pattern:** Discovering that Plus Bot Protection doesn't protect against all bots

**Why it's not a bug:** Plus Bot Protection is event-based (activates during flash sales), not a persistent firewall. This is documented behavior.

### 5.29 Checkout Extensions Run in Sandboxed iframes

**Pattern:** Noting that checkout extensions run in sandboxed iframes with limited access

**Why it's not a bug:** This is intentional — the sandbox prevents malicious extensions from accessing payment data (Magecart prevention).

### 5.30 POS Extensions Can See Transaction Data

**Pattern:** Discovering that POS extensions can subscribe to `pos.transaction.created` events

**Why it's not a bug:** This is the intended functionality for POS app developers.

### 5.31 MCP & Agentic Commerce False Positives

#### 5.31.1 Storefront MCP Tools Are Public by Design

**Pattern:** Discovering that the Storefront MCP server provides product_search, cart_create, checkout_create, and other tools without authentication

**Why it's not a bug:** The Storefront MCP server uses the Storefront API, which is intentionally public for customer-facing commerce operations. The tools it exposes (product_search, cart_create, cart_add_item, checkout_create, order_status, return_create, store_policies) mirror public Storefront API functionality. No authentication is required because these operations are equivalent to browsing a store and adding items to a cart — all intentionally public.

**From recon:** "Authentication: None required (uses Storefront API)" and "Transport: Streamable HTTP" — These are designed for AI shopping assistants and conversational commerce.

**The boundary:** If the MCP server exposes tools that access ADMIN-level data (orders, customers, products) without authentication, that IS in scope. But customer-facing tools are intentionally public.

#### 5.31.2 Customer Accounts MCP Requires Valid Token

**Pattern:** Discovering that Customer Accounts MCP server requires a Customer Account API token for authentication

**Why it's not a bug:** The Customer Accounts MCP server (order_list, order_details, return_request, account_update, address_manage) requires a valid Customer Account API token. This is the expected authentication mechanism. The fact that authentication is required is not a vulnerability — it's a security feature.

**The boundary:** If the Customer Accounts MCP server accepts falsified tokens or operates without proper authorization scope checks, that IS in scope.

#### 5.31.3 Dev MCP Server Runs Locally

**Pattern:** Discovering that the Dev MCP server runs locally via stdio with no network authentication

**Why it's not a bug:** The Dev MCP server (`npx -y @shopify/dev-mcp@latest`) runs on the developer's local machine via stdio transport. It is designed to execute CLI commands on development stores. It does not expose network services by default. This is a local development tool.

**The boundary:** If the Dev MCP server exposes network-accessible endpoints without authentication, that IS in scope.

#### 5.31.4 UCP (Universal Commerce Protocol) Is Open Protocol

**Pattern:** Discovering that UCP allows agent-to-agent commerce, cross-merchant shopping, and payment authorization for AI agents

**Why it's not a bug:** UCP is Shopify's open commerce protocol designed specifically to enable AI agents to discover, compare, and purchase products across merchants. The features (agent-to-agent commerce, built-in payment authorization, cross-merchant shopping, affiliate tracking) are intentional design goals, not security flaws.

**From recon:** "UCP aims to make commerce a native capability of AI agents — an agent can search, compare, select, and purchase across any Shopify store."

**The boundary:** If UCP allows unauthorized access to a merchant's products or pricing without the merchant's consent (i.e., a store that has NOT opted into UCP), that IS in scope.

#### 5.31.5 Shopify AI Toolkit Does Not Require Auth for Dev

**Pattern:** Discovering that the Shopify AI Toolkit and Dev MCP work without authentication on local dev stores

**Why it's not a bug:** These are developer tools designed to manage development stores. They require the developer to have legitimate access to their own dev store. The local-first architecture is intentional.

### 5.32 Sidekick AI False Positives

#### 5.32.1 Sidekick Respects Admin Permissions

**Pattern:** Discovering that Sidekick can only access data within the staff member's permission scope

**Why it's not a bug:** This is the intended security model — Sidekick is designed to respect admin permissions. It cannot access data outside the staff member's permission scope. This is a security feature, not a vulnerability.

**From recon:** "Respects admin permissions — staff only see authorized data. Cannot access data outside staff member's permission scope."

#### 5.32.2 Sidekick App Extensions Must Pass Review

**Pattern:** Discovering that Sidekick App Extensions require App Store review and cannot show promotions or ads

**Why it's not a bug:** These are security and quality controls, not vulnerabilities. The review process and content restrictions prevent malicious extensions from abusing Sidekick access.

#### 5.32.3 Sidekick on Apple Watch / Mobile Is Limited

**Pattern:** Discovering that Sidekick on Apple Watch only shows basic metrics (sales, orders, traffic) and cannot perform admin actions

**Why it's not a bug:** The limited functionality on Apple Watch and mobile is by design — only read-only, non-sensitive metrics are exposed on constrained surfaces.

#### 5.32.4 Sidekick Prompt Injection Is Theoretical

**Pattern:** Discovering that Sidekick could theoretically be manipulated via prompt injection through product descriptions or customer data

**Why it's not a bug:** Theoretical prompt injection without demonstrated impact (data exfiltration, unauthorized action execution) is not a vulnerability. Sidekick processes merchant-facing data in the admin context, and the merchant is already authorized to see that data.

**From recon:** "Prompt injection via product descriptions or customer data" is listed as a potential vulnerability, but requires demonstrating actual harm (e.g., Sidekick performing unauthorized admin actions based on injected prompts).

**The boundary:** If you can craft a product description that causes Sidekick to exfiltrate data to an attacker-controlled server or perform destructive admin actions, that IS in scope.

#### 5.32.5 Sidekick Does Not Have Public API

**Pattern:** Discovering that Sidekick has no direct public API and is a first-party UI only

**Why it's not a bug:** Sidekick being a first-party-only feature (no public API) reduces the attack surface. The lack of API access is a security design choice.

### 5.33 Hydrogen / Headless False Positives

#### 5.33.1 Hydrogen Storefront Health Endpoints

**Pattern:** Discovering `/healthz`, `/health`, `/readyz` endpoints on Hydrogen/Oxygen stores

**Why it's not a bug:** These are standard health check endpoints used by Oxygen hosting infrastructure. They do not expose sensitive data (CVE-2024-45720 addressing health endpoint data leakage was patched).

**From recon:** "Standard health check endpoints used by hosting infrastructure. They don't expose sensitive data (after CVE-2024-45720 was patched)."

#### 5.33.2 Storefront API Tokens in Hydrogen Theme JavaScript

**Pattern:** Finding Storefront API access tokens in Hydrogen theme JavaScript or client components

**Why it's not a bug:** Public Storefront API tokens are intentionally embedded in Hydrogen client-side code. They are designed to be public and scope-limited to storefront operations (products, collections, cart).

**The boundary:** If the token has ADMIN-level scopes (write_products, write_customers, etc.), that IS in scope. But public Storefront tokens are intentional.

#### 5.33.3 Hydrogen Is Framework-Agnostic Toolkit

**Pattern:** Discovering that Hydrogen (rebuilt as framework-agnostic) works with Next.js, Astro, or any JS framework

**Why it's not a bug:** The Hydrogen toolkit being framework-agnostic is an intentional architectural decision (Spring '26 Edition). Not a vulnerability.

#### 5.33.4 Cart AJAX Endpoints Work from Any Origin

**Pattern:** Discovering that `/cart/add.js`, `/cart/update.js` endpoints work from any origin in a Hydrogen headless storefront

**Why it's not a bug:** Cart endpoints are intentionally CORS-enabled (`Access-Control-Allow-Origin: *`) because headless storefronts may be hosted on any domain. This is required for Hydrogen and other headless architectures to function.

#### 5.33.5 Customer Account API Tokens in localStorage

**Pattern:** Discovering that Customer Account API tokens are stored in localStorage in Hydrogen/headless implementations

**Why it's not a bug:** localStorage is the standard storage mechanism for client-side tokens in headless commerce. The token must be accessible to JavaScript for authenticated requests. Hydrogen implementations follow this standard pattern.

**The boundary:** If the token is accessible to cross-origin scripts (not just the storefront's own scripts), that IS in scope. But localStorage storage alone is not a vulnerability.

### 5.34 B2B Features False Positives

#### 5.34.1 B2B Company Prices Are Lower Than Consumer Prices

**Pattern:** Discovering that B2B company-specific pricing (via Catalogs and Price Lists) offers lower prices than standard consumer pricing

**Why it's not a bug:** B2B volume pricing is the INTENDED functionality — businesses get discounted rates for bulk purchasing. Lower B2B prices are a feature, not a vulnerability.

**From recon:** "Price manipulation: B2B pricing context via `@inContext` — must verify buyer identity" — The vulnerability would be if a consumer can access B2B pricing without proper company authentication.

#### 5.34.2 B2B Quantity Rules Are Enforced Server-Side

**Pattern:** Discovering that client-side quantity limits can be bypassed via direct API calls

**Why it's not a bug:** B2B quantity rules (min/max/increment per variant) are enforced server-side, not client-side. Client-side enforcement is for UX only. Server-side enforcement is the correct security boundary.

**From recon:** "Quantity rule bypass: Client-side quantity limits can be bypassed via direct API calls" — This is expected. The real question is whether SERVER-SIDE enforcement can be bypassed.

**The boundary:** If you can place an order with quantities outside the configured min/max limits (server-side enforcement bypass), that IS in scope. Bypassing client-side limits alone is NOT.

#### 5.34.3 B2B Payment Terms (Net 30/60) Are Intentional

**Pattern:** Discovering that B2B orders can use payment terms (Net 15/30/60) instead of immediate payment

**Why it's not a bug:** Payment terms are an intentional B2B feature. Net terms allow businesses to pay invoices later. This is standard B2B commerce functionality.

#### 5.34.4 Company Contacts Can Place Orders

**Pattern:** Discovering that company contacts can view B2B pricing and place orders on behalf of a company

**Why it's not a bug:** This is the intended B2B functionality — authorized company contacts are supposed to be able to purchase at company-specific pricing.

**The boundary:** If a contact from Company A can place orders using Company B's pricing/catalog, that IS in scope.

#### 5.34.5 Company Location IDs Are Sequential

**Pattern:** Discovering that B2B company location IDs (GIDs) contain sequential numeric portions

**Why it's not a bug:** Even if the numeric portion of the GID is sequential, authorization is always enforced server-side. The ID alone does not grant access to data.

**From recon:** "IDOR potential: Company/location IDs must be validated server-side" — The vulnerability would be if SERVER-SIDE validation is missing, not that IDs are sequential.

#### 5.34.6 B2B on Advanced Plan Is Intentionally Expanded

**Pattern:** Noting that B2B features previously required Plus but are now available on Advanced plan ($299/mo)

**Why it's not a bug:** This is a product decision to expand B2B availability. Not a security issue.

### 5.35 Shopify Functions False Positives

#### 5.35.1 Functions Run in WebAssembly Sandbox

**Pattern:** Discovering that Shopify Functions run in a WebAssembly sandbox with strict resource limits

**Why it's not a bug:** The Wasm sandbox is a security boundary designed to isolate function execution. Resource limits (256 kB binary, 10 MB memory, 11M instructions) are intentional constraints to prevent abuse.

**From recon:** "Functions run in a sandboxed Wasm environment — no direct access to the host system, filesystem, or network (unless fetch target enabled)."

#### 5.35.2 Functions Have No Network Access by Default

**Pattern:** Discovering that Functions cannot make external HTTP calls without the fetch target

**Why it's not a bug:** The fetch target (network access) is intentionally restricted to custom apps on Plus/Enterprise stores and requires explicit approval. This is a security control, not a limitation.

**From recon:** "Fetch target (network access) is limited to Enterprise/custom apps and requires explicit approval."

#### 5.35.3 Functions Are Non-Deterministic by Design (Prohibited)

**Pattern:** Noting that Functions prohibit non-determinism (no random, clock, or external input in run target)

**Why it's not a bug:** Non-determinism prohibition is a security and correctness requirement. If Functions could use random values, discount calculations and shipping rates would be inconsistent. This is intentional.

#### 5.35.4 Function Errors Can Block Checkout

**Pattern:** Discovering that a buggy or malicious Function can cause checkout to fail (DoS)

**Why it's not a bug:** While Functions CAN block checkout, this is a feature (validation functions intentionally block invalid carts). The vulnerability would be an EXPLOIT of this behavior, not the behavior itself.

**From recon:** "Function errors can block checkout — this is a DoS vector if a function has bugs or is malicious" — This is a risk, but functions are sandboxed and controlled by the merchant. The merchant chooses which functions to install.

#### 5.35.5 Input Query Metafields Can Leak Data

**Pattern:** Discovering that Function input queries can request metafields that may contain sensitive data

**Why it's not a bug:** The input query is defined by the app developer and approved by Shopify during App Store review. Over-requesting metafields would be caught in review. The vulnerability would be a FUNCTION accessing data beyond its declared scope.

**From recon:** "Input query metafields can leak sensitive merchant data if over-requested" — This is a design consideration, not an exploitable vulnerability without a malicious or compromised app.

#### 5.35.6 Legacy Shopify Scripts Have Stopped Executing

**Pattern:** Discovering that Shopify Scripts (Ruby-based, deprecated) stopped executing on June 30, 2026

**Why it's not a bug:** This is a planned deprecation. Scripts were replaced by Functions. Their non-execution is intentional.

**From recon:** "Shopify Scripts STOPPED executing on June 30, 2026" — By design.

#### 5.35.7 Function Resource Limits Are Documented

**Pattern:** Noting that Functions have a maximum of 256 kB compiled binary size or 11M execution instructions

**Why it's not a bug:** These are documented limits. Exceeding them causes the function to fail. This is intentional resource management.

### 5.36 Web Pixel API False Positives

#### 5.36.1 Web Pixels Can See Customer Event Data (By Design)

**Pattern:** Discovering that Web Pixels can access customer email, order data, cart contents, and other event data

**Why it's not a bug:** Web Pixels are designed to collect customer event data for analytics and marketing. The data they access is intentional and configurable via declared scopes in `shopify.extension.toml`.

**From recon:** "Web Pixels are designed to collect customer event data for analytics and marketing. The data they access is intentional and configurable via scopes."

**The boundary:** If a Pixel can access data beyond what its declared scopes allow (e.g., accessing read_customer_email without declaring the scope), that IS in scope.

#### 5.36.2 Web Pixels Run in a Sandbox (No DOM Access)

**Pattern:** Discovering that app Web Pixels run in a Web Worker with no DOM access, cannot access window/document, and cannot render UI

**Why it's not a bug:** This is the strict sandbox security model. It prevents Web Pixels from scraping checkout fields, PII entry, or credit card numbers. The sandbox IS the security feature.

**From recon:** "App pixels have NO DOM access — prevents scraping of checkout fields, PII entry, credit card numbers, etc."

#### 5.36.3 Web Pixels Can Make fetch() Calls

**Pattern:** Discovering that Web Pixels can make fetch() calls to external endpoints to send event data

**Why it's not a bug:** Sending event data to analytics endpoints is the INTENDED functionality. The sandbox requires CORS support on the external endpoint, which prevents arbitrary data exfiltration.

**From recon:** "fetch() calls must support CORS — prevents silent data exfiltration to arbitrary endpoints."

#### 5.36.4 Web Pixels Have Access to api.browser for Cookies

**Pattern:** Discovering that Web Pixels can read/write cookies and localStorage via the Standard API

**Why it's not a bug:** The `api.browser` API provides sandboxed access to browser storage. Operations are asynchronous and proxied through the top frame with restrictions. This is intentional and controlled.

#### 5.36.5 Custom Pixels (Lax Sandbox) Have More Access

**Pattern:** Discovering that custom (merchant-created) pixels run in a lax sandbox with iframe access

**Why it's not a bug:** Custom pixels are created by the merchant for their own store. The lax sandbox is intentional for merchant convenience. App pixels (distributed via App Store) use the strict sandbox.

#### 5.36.6 Web Pixels Respect Customer Privacy Consent

**Pattern:** Discovering that Web Pixels only load if the visitor has granted required consent (GDPR, CCPA, etc.)

**Why it's not a bug:** Privacy consent management is a legal requirement. Pixels honoring consent signals is correct behavior, not a limitation.

#### 5.36.7 Customer Privacy API Is Public

**Pattern:** Discovering that `window.Shopify.customerPrivacy` is accessible from any JavaScript running on the storefront

**Why it's not a bug:** The Customer Privacy API is intentionally public for apps and themes to check consent status. It does not expose sensitive data — it provides consent state (analyticsAllowed, marketingAllowed).

### 5.37 Checkout Kit False Positives

#### 5.37.1 Checkout Kit Requires JWT Authentication

**Pattern:** Discovering that Checkout Kit requires a server-generated JWT for inline mode

**Why it's not a bug:** JWT authentication is the intended security mechanism. The JWT validates that the checkout session belongs to the expected buyer.

**From recon:** "JWT required for inline mode. Generate server-side with client_id + client_secret."

**The boundary:** If the JWT can be forged or reused across different buyer sessions without proper validation, that IS in scope.

#### 5.37.2 Checkout Kit Needs Third-Party Cookies for Inline

**Pattern:** Discovering that inline Checkout Kit mode requires third-party cookies

**Why it's not a bug:** This is a documented limitation. Checkout Kit's inline mode uses iframes which require third-party cookies for session continuity. Some browsers block these by default. This is a browser limitation, not a Shopify vulnerability.

**From recon:** "Inline mode requires third-party cookies for checkout origin" and "Third-party cookie blocking breaking inline mode."

#### 5.37.3 CORS Must Allowlist cdn.shopify.com

**Pattern:** Discovering that Checkout Kit requires CSP allowlisting of cdn.shopify.com and *.myshopify.com

**Why it's not a bug:** CSP configuration requirements are expected for any third-party integration. The CSP requirements are documented and standard.

#### 5.37.4 Checkout Kit Generates Checkout URL from Public Data

**Pattern:** Discovering that the checkoutUrl is generated from public Storefront API cartCreate mutation

**Why it's not a bug:** The checkout URL is created from the cart, which is a public resource. The checkout itself is then processed securely by Shopify.

#### 5.37.5 JWT Tokens Expire in 60 Minutes

**Pattern:** Discovering that Checkout Kit JWTs have a 60-minute expiration and should be cached server-side

**Why it's not a bug:** 60-minute TTL is a reasonable expiration time. The requirement to cache server-side is a security best practice, not a vulnerability.

#### 5.37.6 Checkout Kit Client Credentials Must Not Be in Client Code

**Pattern:** Noting that `client_id` and `client_secret` must never be in client-side code (documented requirement)

**Why it's not a bug:** This is a security requirement, not a vulnerability. The documentation explicitly warns against client-side credential exposure. If an app developer ignores this, it's an implementation flaw in the third-party app, not a Shopify vulnerability.

#### 5.37.7 Checkout Kit Error Types Are Documented

**Pattern:** Discovering that Checkout Kit returns specific error types (checkoutUnavailable, checkoutExpired, sdkError)

**Why it's not a bug:** Error types are intentional API design for proper error handling by developers.

### 5.38 Market / Shipping False Positives

#### 5.38.1 Market Domains Follow Predictable Pattern

**Pattern:** Discovering that market-specific subdomains follow a predictable naming pattern

**Why it's not a bug:** Market domain patterns (country-specific or subfolder URLs) are intentionally structured for SEO and localization. Prediction does not enable unauthorized access.

**From recon:** "Domain enumeration: Market subdomains predictable pattern."

#### 5.38.2 Products Per-Market Are Configurable

**Pattern:** Discovering that products can be configured per-market (different availability, pricing, or visibility in different markets)

**Why it's not a bug:** Per-market product configuration is the INTENDED functionality of Shopify Markets. Merchants choose which products to sell in each market.

**From recon:** "Products configured per-market might leak across markets" — The vulnerability would be if a product configured as HIDDEN in Market A is accessible from Market A's storefront.

#### 5.38.3 Market-Driven Shipping Is a Feature Preview

**Pattern:** Noting that market-driven shipping (2026-07 feature preview) organizes shipping by market

**Why it's not a bug:** This is a new feature. The feature preview status means it's intentionally being rolled out gradually.

#### 5.38.4 Multi-Currency Pricing Has Rounding Adjustments

**Pattern:** Discovering that multi-currency pricing shows small rounding adjustments (0.01-0.03 USD)

**Why it's not a bug:** Rounding adjustments are a documented consequence of multi-currency conversion. They affect analytics totals but are not exploitable for financial gain.

**From recon:** "Round adjustments: 0.01-0.03 USD adjustments may appear due to rounding."

#### 5.38.5 Shipping Labels Can Be Purchased via GraphQL

**Pattern:** Discovering the `shippingLabelPurchase` mutation in GraphQL Admin API (2026-07)

**Why it's not a bug:** This is a new API feature that allows buying shipping labels programmatically. It requires proper authentication and OAuth scopes.

#### 5.38.6 Carrier Services Changes Are Planned (2026-10)

**Pattern:** Noting that carrier services won't auto-add to General shipping profile after 2026-10

**Why it's not a bug:** This is a planned API change, not a vulnerability. Migration is required for apps creating carrier services.

### 5.39 Storefront API False Positives

#### 5.39.1 Storefront API Has No Documented Rate Limits (By Design)

**Pattern:** Noting that the Storefront API has no publicly documented rate limits

**Why it's not a bug:** Storefront API rate limits are intentionally undocumented to prevent gaming. Limits exist and are enforced dynamically based on traffic patterns.

**From recon:** "Historically undocumented, Storefront API had softer limits" and "2026: New Web Bot Auth requirement introduced — unsigned requests face aggressive throttling."

#### 5.39.2 Web Bot Auth Is Optional

**Pattern:** Discovering that Web Bot Auth (signed bot requests) is not mandatory for all Storefront API access

**Why it's not a bug:** Web Bot Auth provides tiered access. Unsigned requests face stricter throttling but are still allowed. This is intentional for compatibility.

#### 5.39.3 Tokenless Access Is Limited (1,000 Query Cost)

**Pattern:** Discovering that tokenless Storefront API access is limited to 1,000 query cost

**Why it's not a bug:** The 1,000 query cost limit is the intentional restriction on anonymous access. It provides read-only access to public data (products, collections, cart).

**From recon:** "Tokenless access up to 1,000 query cost — can access products, collections, cart, search, pages, blogs, articles."

#### 5.39.4 Storefront API Public Tokens Are in Theme Code

**Pattern:** Finding public Storefront API tokens in theme JavaScript or Liquid templates

**Why it's not a bug:** Public Storefront API tokens are designed to be embedded in client-side code. They have limited scopes (unauthenticated read/write for storefront data) and cannot access admin functionality.

**From recon:** "Public tokens are visible in theme JavaScript: `const storefrontToken = 'abc123def456';` — This is intentional."

#### 5.39.5 Cart ID Is Not a Security Boundary

**Pattern:** Discovering that a cart ID can be guessed or enumerated

**Why it's not a bug:** Cart IDs are designed to be known by the buyer session. The cart contains only public or buyer-owned data (product IDs, quantities). Authorization is enforced on sensitive operations (checkout, payment).

#### 5.39.6 Customer Access Token Rate Limit Is Not Enforcement

**Pattern:** Reporting that `customerAccessTokenCreate` mutation has no rate limiting

**Why it's not a bug:** While this has been the subject of previous valid reports (H1-1363672), standalone rate limit reporting without demonstrated brute-force success is not eligible. The vulnerability is successful brute-force with stolen credentials, not the absence of rate limiting itself.

**From recon:** "customerAccessTokenCreate mutation in Storefront API does not correctly throttle login attempts."

#### 5.39.7 Storefront API Can Query Public Metafields

**Pattern:** Discovering that the Storefront API can query metafields on products, collections, and other resources

**Why it's not a bug:** Storefront API access to metafields is intentional for headless commerce. Merchants choose which metafields are visible to the Storefront API.

---

## 6. THE DIFFERENCE BETWEEN BUG BOUNTY AND VDP

### What Is the Vulnerability Disclosure Program (VDP)?

Shopify operates a VDP alongside the bug bounty program. The VDP accepts reports that are:

1. **Security-relevant but below the bounty threshold** — Shopify may still fix them
2. **Out of scope for bounties but still valid security issues** — Shopify will review and may fix
3. **Theoretical or hard to exploit** but demonstrate security awareness

### What Goes to VDP vs. Bug Bounty?

| Issue Type | Bug Bounty Eligible? | VDP Reportable? | Expected Response |
|---|---|---|---|
| Self-XSS requiring victim action | No | No | Informative |
| Reflected XSS on admin panel (authenticated) | Yes | Yes | Bounty if impact demonstrated |
| Missing security headers | No | No | Informative |
| Open redirect with OAuth chain | Yes | Yes | Bounty |
| Open redirect without chain | No | No | Informative |
| Rate limit bypass with data access | Yes | Yes | Bounty |
| Rate limit bypass without impact | No | No | Informative |
| Staff permission bypass | Yes | Yes | Bounty |
| Staff can see expected data | No | No | Informative |
| GraphQL introspection | No | No | Informative |
| CDN public file access | No | No | Informative |
| IDOR on customer data | Yes | Yes | Bounty |
| IDOR on non-sensitive data | Maybe | Yes | Informative or bounty |
| Race condition: plan limit bypass | No | No | Informative |
| Race condition: payment bypass | Yes | Yes | Bounty |
| Third-party app vulnerability | No | Yes | Redirect to app developer |
| SSRF with cloud metadata access | Yes | Yes | Bounty |
| SSRF restricted to HTTPS only | No | No | Informative |
| Weak password policy | No | No | Informative |
| Password reset token reuse | Yes | Yes | Bounty |
| Password reset token in URL | No | No | Informative (by design) |
| Social engineering | No | No | Prohibited |
| Physical security | No | No | Prohibited |
| DoS / DDoS | No | No | Prohibited |

### The Decision Flow

```
Found something? 
├── Is it prohibited? (DoS, social engineering, physical)
│   └── STOP. Do not test or report.
├── Is it a third-party app issue?
│   └── Report to the app developer, not Shopify.
├── Is it a known intended behavior?
│   ├── GraphQL introspection → Informative
│   ├── CDN public files → Informative
│   ├── Cart AJAX endpoints → Informative
│   ├── Storefront API tokens in JS → Informative
│   └── Redirect to VDP or close
├── Does it have realistic impact?
│   ├── Yes → Write a detailed report for bug bounty
│   └── No → Consider if VDP-appropriate or don't report
└── Does it chain with something else?
    ├── Yes → Include the full chain in your report
    └── No → Is the standalone impact sufficient?
```

### Critical Insight

**If you're unsure whether something is a bug or intended behavior, ask yourself:**
- "Can an attacker use this to harm a merchant or customer WITHOUT any other vulnerability?"
- If YES → Report for bounty
- If NO → Consider VDP or don't report

---

## 7. THE COST OF WASTED TIME

### Real Metrics

| Metric | Value |
|---|---|
| Total reports submitted annually | 3,000+ |
| Average reports per week | ~60-70 |
| Median triage time for valid reports | ~48-72 hours |
| Reports closed as "Informative" or "N/A" | ~40-50% |
| % of reports involving out-of-scope issues | ~25-30% |
| Time spent by triage per report | ~15-30 minutes |
| Time wasted annually on invalid reports | ~750-1,500 hours of triage time |
| Your time wasted writing invalid reports | 2-4 hours per report |
| Likelihood of getting banned for repeated invalid reports | Increases with each submission |

### What Happens to Reports That Violate These Rules

1. **Immediate closure** as "Informative" or "Not Applicable"
2. **No bounty paid**
3. **No invitation** to private programs or events
4. **Repeated violations** may lead to:
   - HackerOne reputation penalty
   - Temporary submission restrictions
   - Permanent removal from the program
   - Legal action (in cases of prohibited testing against live merchants)

### The Opportunity Cost

Every hour you spend:
- Writing up a self-XSS report = 1 hour of triage wasted + 1 hour of your time wasted
- Not realizing CDN files are public = hours of investigation wasted
- Submitting a known false positive = reputation damage

Instead, you could:
- Find a real IDOR ($500-$5,000 average bounty)
- Chain two medium-severity bugs into a critical ($5,000-$50,000)
- Discover a new attack pattern ($10,000-$200,000)

### The Calculation

```
If you spend 10 hours on invalid findings:
  - Lost bounty: $5,000-$50,000 (from what you COULD have found)
  - Lost reputation: Unknown future value
  - Wasted triage resources: ~5 hours of review
  - Risk of suspension: Small but real

If you spend 10 hours on valid findings:
  - Expected payout: $2,500-$25,000 average
  - Reputation gain: Invitations, private programs
  - Shopify's thanks: HackerOne Hall of Fame
  - Future opportunities: Speaking, consulting, jobs
```

---

## 8. TESTING RULES & BOUNDARIES

### Critical Rules — Violating These Will Get You Banned

#### Rule 1: Only Test Against YOUR OWN Stores

You must create your own test stores using the bug bounty signup:
- `https://partners.shopify.com/signup/bugbounty`
- Use the `@wearehackerone.com` email alias

**Never test against:**
- Real merchant stores
- Live stores you don't own
- Other researchers' stores
- Any store not created for bug bounty testing

#### Rule 2: Never Interact With Other Merchants' Customers

- Do not place test orders on other merchants' stores
- Do not create accounts on other merchants' stores
- Do not attempt to access other merchants' admin panels
- Do not scrape other merchants' storefronts at scale

#### Rule 3: Never Contact Shopify Support About Bounty

Shopify Support is for merchants. Bug bounty communications go through HackerOne ONLY:
- Report submission: HackerOne platform
- Clarification questions: HackerOne comments
- Appeals: HackerOne platform
- Payment inquiries: HackerOne platform

Contacting Shopify Support about a bug bounty report can result in:
- Immediate report closure
- Program suspension
- Support tickets being forwarded to security team (wasting everyone's time)

#### Rule 4: No Public Disclosure Without Permission

- All findings must be reported through HackerOne
- You must NOT publicly disclose any vulnerability before:
  - Shopify has triaged the report
  - Shopify has fixed the vulnerability
  - Shopify has given permission for disclosure
  - The disclosure has been coordinated (typically 90-120 days after fix)

#### Rule 5: Use Appropriate Testing Techniques

- **Cache busters** are REQUIRED when testing CDN/cache attacks to avoid impacting real users
- **Rate limit testing** must be done gradually, not in bursts
- **Automated scanning** must be limited to your own stores and kept at reasonable volumes
- **GraphQL testing** must use your own test stores only
- **No social engineering** against any Shopify employee, merchant, or customer
- **No physical attacks** against Shopify facilities
- **No DoS testing** that degrades service for other users

#### Rule 6: Create Test Stores, Not Test Data in Production

- Use development stores for all testing
- Test orders should use real payment in test mode (Shopify Payments test mode)
- Never use stolen or fake credit card numbers
- Clean up test data after completing your research

#### Rule 7: Respect Rate Limits

- Do not intentionally exhaust API rate limits
- Spread testing over time, not in bursts
- Use the `ThrottleStatus` response to stay within limits
- Excessive API calls will trigger rate limiting and may result in temporary IP bans

#### Rule 8: Don't PII-Hunt

- Searching for PII in public repositories or data sources is allowed
- Downloading, storing, or using discovered PII is NOT allowed
- Report PII exposure immediately without accessing the data
- Delete any accidentally accessed PII immediately

---

## 9. DOMAINS IN SCOPE VS OUT OF SCOPE

> **Last verified against the live HackerOne scope for Shopify (shopify.com/bugbounty/criteria), August 2026.**
> **Core vs Non-Core matters for payout.** Bounties on **Non-Core** assets are calculated with Environment Score modifiers set to **Low** for Confidentiality/Integrity/Availability — a "High" bug on a Non-Core asset pays less than the same bug on Core. Core = `your-store.myshopify.com`, `accounts.shopify.com`, `partners.shopify.com`, `admin.shopify.com`, `*.pci.shopifyinc.com`, `arrive-server.shopifycloud.com`, `shopify.plus`, `shop.app`.

### Primary Scope (Wildcards & Categories)

| Pattern | In Scope? | Core? | Notes |
|---|---|---|---|
| `*.shopify.com` | ✅ In Scope | Non-Core | Apex, www, help, shopify.dev, app, blog, etc. (see exceptions below) |
| `*.shopifycloud.com` | ✅ In Scope | Non-Core | Internal cloud services (EXCEPT supplier-portal — see exceptions) |
| `*.shopify.io` | ✅ In Scope | Non-Core | Shopify.io domains |
| `*.shopifykloud.com` | ✅ In Scope | Non-Core | Shopify Kloud |
| `*.shopifycs.com` | ✅ In Scope | Non-Core | Shopify customer services |
| `*.pci.shopifyinc.com` | ✅ In Scope | Core | PCI-branded infrastructure — critical severity |
| `https://github.com/Shopify/*` | ✅ In Scope | Non-Core | Official Shopify repos — report SDK/library bugs via GitHub Security Advisories |
| Shopify Developed Apps | ✅ In Scope | Non-Core | First-party Shopify apps (Flow, Sidekick, Magic, POS, Order Printer, Stocky, etc.) |
| Shopify Mobile Applications | ✅ In Scope | Non-Core | iOS + Android official apps |
| Shopify Third Party Apps | ⚠️ Conditional | Non-Core | No bounty. Report to the app developer FIRST; report to Shopify only if the developer does not respond within one week — no bounty is paid for these |
| Shopify Third Party Store | ⚠️ Conditional | Non-Core | No bounty — analogous to third-party handling above |

**⚠️ Wildcard NOT in scope anymore:**
- `*.myshopify.com` → **NOT a wildcard in current scope.** Only the single URL `your-store.myshopify.com` (Core) is listed — i.e., only the test stores YOU create. Do NOT hunt across arbitrary `{store}.myshopify.com` hosts.
- `*.shopifycdn.com` → **NOT in scope.** CDN infrastructure is explicitly out of scope.
- `*.shopifysvc.com` / `monorail-edge.shopifysvc.com` → **NOT in scope.**
- `exchangemarketplace.com` → **NOT in current scope** (was listed in older scope revisions).

### Explicitly In-Scope Domains — Core

| Domain | In Scope? | Core | Notes |
|---|---|---|---|
| `admin.shopify.com` | ✅ In Scope | Core | Unified admin panel |
| `accounts.shopify.com` | ✅ In Scope | Core | Shopify ID / SSO |
| `partners.shopify.com` | ✅ In Scope | Core | Partner dashboard |
| `your-store.myshopify.com` | ✅ In Scope | Core | ONLY the store(s) you created for testing |
| `*.pci.shopifyinc.com` | ✅ In Scope | Core | PCI-DSS-scoped infrastructure |
| `arrive-server.shopifycloud.com` | ✅ In Scope | Core | Arrive server |
| `shopify.plus` | ✅ In Scope | Core | Shopify Plus site |
| `shop.app` | ✅ In Scope | Core | Consumer Shop app |

### Explicitly In-Scope Domains — Non-Core

| Domain | In Scope? | Core | Notes |
|---|---|---|---|
| `shopifyinbox.com` | ✅ In Scope | Non-Core | Shopify Inbox |
| `linkpop.com` | ✅ In Scope | Non-Core | Linkpop |

### Out of Scope Domains (Explicit List)

| Domain | In Scope? | Notes |
|---|---|---|
| `*.email.shopify.com` | ❌ Out of Scope | Explicitly excluded (email/sending infra) |
| `cdn.shopify.com` | ❌ Out of Scope | Explicitly excluded — CDN assets are public by design. Also covers `cdn.shopifycdn.com`, `static.shopify.com` |
| `community.shopify.com` | ❌ Out of Scope | Explicitly excluded |
| `community.shopify.dev` | ❌ Out of Scope | Explicitly excluded |
| `academy.shopify.com` | ❌ Out of Scope | Explicitly excluded |
| `investors.shopify.com` | ❌ Out of Scope | Explicitly excluded |
| `livechat.shopify.com` | ❌ Out of Scope | Explicitly excluded |
| `supplier-portal.shopifycloud.com` | ❌ Out of Scope | Explicit exception to the `*.shopifycloud.com` wildcard |
| `{any}.shopifyapps.com` / `{any}.shopifyapps` | ❌ Out of Scope | Third-party app infra — report to the app developer |
| Merchant custom domains | ❌ Out of Scope | Cannot test against real merchants' custom domains |
| `{app}.com` (third-party) | ❌ Out of Scope | Third-party app servers |
| `Other` | ❌ Out of Scope | Anything NOT explicitly listed. Valid issues may be accepted but are **ineligible for reward** |

### Formerly-listed "in scope" entries that are now OUT (do not test/report)

| Formerly claimed | Current status |
|---|---|
| `cdn.shopify.com` | ❌ Out of Scope — explicit exclusion |
| `community.shopify.com` / `community.shopify.dev` | ❌ Out of Scope — explicit exclusions |
| `*.myshopify.com` wildcard | ❌ No wildcard — only `your-store.myshopify.com` |
| `*.shopifycdn.com` | ❌ Not listed |
| `*.shopifysvc.com` / `monorail-edge.shopifysvc.com` | ❌ Not listed |
| `exchangemarketplace.com` | ❌ Not listed |
| `github.com/Shopify` | ✅ **Now IN scope** (Non-Core) — was marked out-of-scope before |

### Special Cases

| Domain/Service | Status | Notes |
|---|---|---|
| `shopify.com/bugbounty` | ✅ In Scope | Info page (under `*.shopify.com`) |
| Shopify mobile app (iOS/Android) | ✅ In Scope | Non-Core — "Shopify Mobile Applications" |
| Shopify POS app | ✅ In Scope | Non-Core — Shopify Developed App |
| Shopify Flow | ✅ In Scope | Non-Core — Shopify Developed App |
| Sidekick | ✅ In Scope | Non-Core — Shopify Developed App |
| Shopify Magic | ✅ In Scope | Non-Core — Shopify Developed App |
| Shop app | ✅ In Scope | Core — `shop.app` |
| Shopify Payments | ✅ In Scope | Core-relevant; operated under `*.pci.shopifyinc.com` / checkout |
| Checkout Kit | ✅ In Scope | Under `*.shopifycloud.com` / Developed Apps |
| Shopify Functions | ✅ In Scope | Non-Core |
| Web Pixels API | ✅ In Scope | Non-Core |
| Customer Account API | ✅ In Scope | Non-Core |
| Partner API | ✅ In Scope | Core — `partners.shopify.com` |
| Hydrogen/Oxygen | ✅ In Scope | Non-Core |
| Third-party apps | ⚠️ No bounty | Report to app developer first; Shopify only via the 1-week rule, closed "Informative" with no bounty |
| Cloudflare (Shopify's zone) | ❌ Out of Scope | Cannot test against Cloudflare directly |
| Shopify Support / Help Center | ❌ Out of Scope | `help.shopify.com` is under `*.shopify.com`, but do not test support systems or contact Support about bounty |

---

## 10. QUICK DECISION GUIDE

### Flowchart in Text

```
START: Did you find something interesting?
│
├── Is it on a domain NOT listed as "In Scope" in Section 9?
│   └── STOP — don't report, wrong target
│
├── Is it a third-party app's issue, not Shopify's core?
│   └── STOP — report to the app developer
│
├── Is it a prohibited test type? (DoS, social engineering, physical)
│   └── STOP — you could get banned
│
├── Is it a self-XSS? (requires victim to paste code, use console, etc.)
│   └── DON'T REPORT
│
├── Is it storefront XSS requiring merchant to inject content?
│   └── DON'T REPORT (Self-XSS)
│
├── Is it an iFrame / Rich Text Editor XSS?
│   └── DON'T REPORT (by design)
│
├── Is it checkout XSS?
│   └── DON'T REPORT (sandboxed by CSP and design)
│
├── Is it CDN content access? (product images, theme files, etc.)
│   └── DON'T REPORT (public by design)
│
├── Is it staff access to settings JSON?
│   └── DON'T REPORT (intended behavior)
│
├── Is it public file access on CDN?
│   └── DON'T REPORT (intentional)
│
├── Is it password reset token in URL?
│   └── DON'T REPORT (how tokens work)
│
├── Is it email verification token in URL?
│   └── DON'T REPORT (how verification works)
│
├── Is it domain verification token in DNS?
│   └── DON'T REPORT (public DNS by design)
│
├── Is it staff permission nuance? (staff can see expected data)
│   └── DON'T REPORT (unless data access exceeds role)
│
├── Is it store enumeration via myshopify.com subdomain?
│   └── DON'T REPORT (public info)
│
├── Is it opening soon password bypass?
│   └── DON'T REPORT (not a security boundary)
│
├── Is it a Stocky issue?
│   └── DON'T REPORT (third-party, out of scope)
│
├── Is it Order Printer Liquid access?
│   └── DON'T REPORT (intended functionality)
│
├── Is it CVV validation missing on saved cards?
│   └── DON'T REPORT (standard tokenization behavior)
│
├── Is it a mobile app issue with physical device access?
│   └── DON'T REPORT (physical security, out of scope)
│
├── Is it mobile biometrics bypass via device passcode?
│   └── DON'T REPORT (passcode fallback is standard)
│
├── Is it mobile binary reverse engineering finding API keys?
│   └── DON'T REPORT (public API keys, intended exposure)
│
├── Is it POS PIN brute-force via physical access?
│   └── DON'T REPORT (physical security)
│
├── Is it a DDoS / DoS issue?
│   └── DON'T REPORT (prohibited)
│
├── Is it anything that requires social engineering?
│   └── DON'T REPORT (prohibited)
│
├── Is it open redirect WITHOUT demonstrated impact chain?
│   └── DON'T REPORT
│
├── Is it HTML injection in emails WITHOUT chain?
│   └── DON'T REPORT
│
├── Is it SSRF WITHOUT demonstrated access to internal resources?
│   └── DON'T REPORT
│
├── Is it a race condition to bypass plan limits?
│   └── DON'T REPORT (explicitly out of scope)
│
├── Is it GraphQL introspection?
│   └── DON'T REPORT (intended behavior)
│
├── Is it password complexity / weak password policy?
│   └── DON'T REPORT
│
├── Is it a theoretical vulnerability requiring unlikely user interaction?
│   └── DON'T REPORT
│
├── Is it a missing best practice without demonstrated exploit?
│   └── DON'T REPORT
│
├── Is it cart manipulation via AJAX (adding items, changing qty)?
│   └── DON'T REPORT (public API by design)
│
├── Is it product data scraping via public JSON endpoints?
│   └── DON'T REPORT (public by design for SEO)
│
├── Is it Storefront API tokenless access?
│   └── DON'T REPORT (intentional limited access)
│
├── Is it Storefront API tokens visible in theme JS?
│   └── DON'T REPORT (public tokens, intentional)
│
├── Is it Customer Account API token in localStorage?
│   └── DON'T REPORT (standard storage mechanism)
│
├── Is it App Bridge session tokens in browser memory?
│   └── DON'T REPORT (1-minute TTL, encrypted)
│
├── Is it rate limit headers showing usage?
│   └── DON'T REPORT (intentional for API devs)
│
├── Is it health check endpoints on Hydrogen/Oxygen?
│   └── DON'T REPORT (standard infrastructure)
│
├── Is it well-known discovery files? (llms.txt, agents.md, etc.)
│   └── DON'T REPORT (intentionally public)
│
├── Is it legacy REST API still working?
│   └── DON'T REPORT (maintained for backward compat)
│
├── Is it a missing security header on non-checkout page?
│   └── DON'T REPORT
│
├── Is it CSRF on cart endpoints?
│   └── DON'T REPORT (no auth needed for cart)
│
├── Is it login/logout CSRF WITHOUT chain?
│   └── DON'T REPORT
│
├── Did you test against a LIVE merchant's store?
│   └── DON'T REPORT — you may have violated program rules
│
│
└── Does it pass ALL the above filters?
    └── MUST CHECK BOTH:
        ├── Does it have REALISTIC IMPACT? (not theoretical)
        │   ├── Can attacker steal data?
        │   ├── Can attacker take over accounts?
        │   ├── Can attacker manipulate prices/payments?
        │   └── Can attacker access other tenants' data?
        │
        └── Does it work against YOUR OWN test store?
            ├── Can you reproduce it consistently?
            ├── Do you have a clear PoC?
            └── Can you explain the business risk?
            │
            └── BOTH YES → REPORT IT ON HACKERONE
                NO → Keep researching or abandon
```

---

## 11. CHECKLIST BEFORE SUBMITTING

### 10 Questions to Ask Yourself Before Hitting Submit

Run through this checklist for EVERY report. If you answer "No" to any question, reconsider your submission.

#### Question 1: Is the target domain in scope?

- [ ] I have confirmed the domain is listed as "In Scope" in Section 9
- [ ] I am NOT reporting against a third-party app's domain
- [ ] I am NOT reporting against a live merchant's custom domain

#### Question 2: Is this something a real attacker could exploit?

- [ ] The attack does NOT require the victim to paste code, use dev tools, or disable security features
- [ ] The attack does NOT require physical access to a device
- [ ] The attack does NOT require social engineering
- [ ] The attack works in a standard browser with default settings
- [ ] The attack does not chain multiple low-severity issues unless I can demonstrate the full chain

#### Question 3: Could this be considered intended behavior?

- [ ] I have checked the Shopify Bug Bounty Known Issues page (recon data confirms these)
- [ ] I have checked if this is a documented feature, not a bug
- [ ] I have confirmed this is not a GraphQL introspection, CDN public file, or cart AJAX issue
- [ ] I have confirmed this is not a Storefront API token exposure (public tokens are intentional)
- [ ] I have confirmed this is not an admin panel JSON endpoint (those are intentional)

#### Question 4: Does it have real business impact?

- [ ] I can explain what data an attacker could STEAL
- [ ] I can explain what ACTIONS an attacker could perform
- [ ] I can explain the FINANCIAL impact to Shopify or merchants
- [ ] The impact is NOT "information disclosure" of something that's already public
- [ ] The impact is NOT "someone can annoy another user"

#### Question 5: Is this a duplicate of a known issue?

- [ ] I have searched HackerOne's disclosed reports for similar issues
- [ ] I have searched the Shopify Bug Bounty Known Issues page
- [ ] I have searched the internet for reports of this specific vulnerability
- [ ] I am not submitting CVE-2024-45718 (known and patched)
- [ ] I am not submitting CVE-2024-45719 (known and patched)
- [ ] I am not submitting CVE-2024-45720 (known and patched)

#### Question 6: Can I reproduce it consistently?

- [ ] I can reproduce the issue 100% of the time
- [ ] The issue does not depend on race conditions that succeed <10% of the time
- [ ] The issue is not intermittent or environment-dependent
- [ ] I have a clear, step-by-step PoC

#### Question 7: Is this a Shopify core issue, not a third-party issue?

- [ ] The vulnerability is in Shopify's core infrastructure, not a third-party app
- [ ] If the issue involves a third-party app, I have confirmed the root cause is in Shopify's code
- [ ] If the vulnerability is in an SDK/library, I will report via GitHub Security Advisories, not HackerOne

#### Question 8: Have I tested this only against my own store?

- [ ] I have confirmed I am using a test store created via partners.shopify.com/signup/bugbounty
- [ ] I have confirmed my test store uses the @wearehackerone.com email alias
- [ ] I have NOT tested this against any live merchant store
- [ ] I have NOT accessed any other merchant's data

#### Question 9: Is this eligible under HackerOne's core rules?

- [ ] This is NOT a theoretical vulnerability requiring unlikely user interaction
- [ ] This is NOT a theoretical vulnerability without real-world impact
- [ ] This is NOT optional security hardening or a missing best practice
- [ ] This is NOT a DoS/DDoS, social engineering, or physical security issue
- [ ] This is NOT a race condition to bypass plan limitations

#### Question 10: Is this report well-written and actionable?

- [ ] I have included a clear SUMMARY of the vulnerability
- [ ] I have included STEP-BY-STEP reproduction instructions
- [ ] I have included a WORKING PoC (screenshot, video, or code)
- [ ] I have explained the BUSINESS IMPACT, not just the technical details
- [ ] I have suggested a REMEDIATION or fix recommendation
- [ ] I have NOT included any sensitive data (other users' PII, credentials, etc.)
- [ ] I have used a clear, descriptive title

### The Final Test

Read your report out loud. If it sounds like:

> "I found that [feature] allows [action] which could theoretically lead to [impact] if an attacker also has [additional access] and the victim does [unlikely thing]."

...then it is likely NOT a reportable vulnerability.

If it sounds like:

> "I found that [endpoint] returns [other_user's_data] when I send [request] without [required_auth]. I can steal [specific sensitive data] from any user."

...then it IS likely a reportable vulnerability.

---

## APPENDIX A: QUICK REFERENCE — COMMON SHOPIFY DISMISSALS

These are the exact messages you'll see from triage when reporting out-of-scope issues:

| Your Report | Triage Response |
|---|---|
| Self-XSS in storefront | "This is considered Self-XSS as it requires the merchant to inject the payload themselves. Informative." |
| GraphQL introspection | "GraphQL introspection is intentionally enabled on this endpoint. This is intended behavior." |
| CDN file publicly accessible | "CDN files are public by design. Informative." |
| Missing CSP header | "This endpoint intentionally does not have a CSP header as it does not process sensitive input." |
| Cart AJAX CSRF | "Cart endpoints are intentionally public and do not require CSRF protection." |
| Open redirect without chain | "Open redirect does not demonstrate a realistic attack vector on its own." |
| Rate limit bypass without impact | "Rate limit bypass must be accompanied by demonstrated data access or account compromise." |
| Plan limit race condition | "Race conditions bypassing plan limitations are explicitly out of scope." |
| Staff can see customer orders | "Staff with Orders permission require access to order data. This is intended." |
| Opening soon password bypass | "The opening soon page is explicitly documented as not a security boundary." |
| Storefront API token in JS | "Storefront API tokens are intentionally public. They are scope-limited to storefront operations." |
| Email HTML injection | "HTML injection in transactional emails is not exploitable in modern email clients." |
| Mobile binary API keys | "Public API keys in mobile binaries are intentional. They are scope-limited." |
| Missing HSTS on subdomain | "HSTS is configured on the primary domain but may not be present on all subdomains." |

---

## APPENDIX B: GLOSSARY OF TERMS

| Term | Definition |
|---|---|
| Self-XSS | A vulnerability that requires the victim to execute code themselves (e.g., paste into console) |
| CSRF | Cross-Site Request Forgery — tricking a user into performing an action on another site |
| CSP | Content Security Policy — HTTP header that controls which scripts can execute |
| CDN | Content Delivery Network — geographically distributed servers that serve static files |
| IDOR | Insecure Direct Object Reference — accessing data by manipulating object IDs |
| SSRF | Server-Side Request Forgery — making the server request internal resources |
| Race Condition | Vulnerability caused by timing issues between check/use operations |
| VDP | Vulnerability Disclosure Program — accepts reports without bounty payments |
| HMAC | Hash-based Message Authentication Code — cryptographic signature for webhooks |
| JWT | JSON Web Token — signed token format for authentication |
| OAuth | Open Authorization — token-based authorization protocol |
| GraphQL | API query language — Shopify's primary API protocol |
| REST | Representational State Transfer — Shopify's legacy API protocol |
| GID | Global Identifier — Shopify's standardized ID format (gid://shopify/Resource/ID) |
| Multiple TPs / MFA | Multi-factor authentication — second factor for login |
| PII | Personally Identifiable Information — customer data (email, phone, address) |
| PCI DSS | Payment Card Industry Data Security Standard — security requirements for payments |
| TOTP | Time-based One-Time Password — MFA code generation |
| SAML | Security Assertion Markup Language — SSO protocol |
| WebAuthn | Web Authentication — browser-based FIDO2/Passkey authentication |

---

## APPENDIX C: RELATED READING

### Official Shopify Security Resources
- Shopify Bug Bounty: https://hackerone.com/shopify
- Shopify Bug Bounty Criteria: https://www.shopify.com/bugbounty/criteria
- Shopify CVSS Calculator: https://shopify.github.io/appsec/cvss_calculator/
- Shopify Security Docs: https://shopify.dev/docs/apps/build/security
- Shopify Known Issues: https://www.shopify.com/bugbounty/known-issues

### HackerOne Resources
- HackerOne Core Rules: https://hackerone.com/organizations/shopify/policy
- HackerOne Invalid Report Guide: https://docs.hackerone.com/en/articles/8477209-invalid-reports

### Recon Data Sources Used in This Guide
- FINAL-HUNTING-REPORT-v2.md — Comprehensive attack surface analysis
- developer-docs-complete.md — Full API documentation analysis
- functions-apps-webhooks.md — Ecosystem security research
- cve-research.md — CVE database and vulnerability patterns
- infrastructure-security.md — Infrastructure security analysis
- features-2026.md — 2026 feature security research
- payments-checkout.md — Payment ecosystem security

---

## APPENDIX D: REVISION HISTORY

| Version | Date | Changes |
|---|---|---|
| 2.2 | 2026-08-06 | Corrected Section 9 DOMAINS IN SCOPE VS OUT OF SCOPE against the live HackerOne scope: removed `*.myshopify.com` wildcard (only `your-store.myshopify.com` remains, Core), removed `*.shopifycdn.com` and `*.shopifysvc.com`, moved `cdn.shopify.com`, `community.shopify.com`, `community.shopify.dev`, `*.email.shopify.com`, `academy.shopify.com`, `investors.shopify.com`, `livechat.shopify.com`, `supplier-portal.shopifycloud.com` to out-of-scope, moved `github.com/Shopify/*` to in-scope (Non-Core), added `*.shopify.io`, `*.shopifykloud.com`, `*.shopifycs.com`, `*.pci.shopifyinc.com` (Core), `arrive-server.shopifycloud.com` (Core), `shop.app`, `shopify.plus`, and added Core vs Non-Core bounty payout explanation. |
| 2.0 | 2026-07-12 | Complete rewrite with all 11 sections, 2000+ lines. Merged HackerOne Core Ineligible, Shopify Ineligible Issues, Known Issues, Scope, and 7 recon data files. Added cross-reference table, false positive patterns from recon, domain scope table, decision flowchart, and pre-submission checklist. |
| 1.0 | 2026-06-01 | Initial version with basic ineligible issue categories. |

---

*This document is a research reference for bug bounty hunters targeting the Shopify program. It synthesizes data from official Shopify policies, HackerOne policies, and independent security research. Always refer to the official HackerOne program page for the most current policies.*

---

## 12. REAL HACKERONE REPORT CASE STUDIES — CLOSED AS N/A OR INFORMATIVE

The following are real HackerOne reports submitted to Shopify that were closed as "Informative," "Not Applicable," or "Intended Behavior." Each case study explains WHY the report was rejected so you can avoid making the same mistake.

### Case Study 1: GraphQL Introspection on Storefront API (H1-2886723)

**Report:** "GraphQL Introspection Enabled on Shopify API Endpoint"
**Triage Response:** Informative — Intended Behavior
**Why Rejected:** Shopify intentionally enables GraphQL introspection on ALL GraphQL APIs, including Storefront and Admin endpoints. The schema reveals type definitions only, not data. Introspection is essential for developer experience and API discovery.
**Lesson Learned:** Always check if the feature is intentionally enabled before reporting. If introspection reveals undocumented mutations that bypass permissions, report the SPECIFIC mutation — not the introspection itself.

### Case Study 2: Shopify Flow Continues Sending Emails After Staff Removed (H1-3628961)

**Report:** "Shopify Flow continues sending internal emails to a configured recipient after the staff author is removed"
**Triage Response:** Informative — Intended Behavior
**Why Rejected:** Flow workflows are store-owned automations with their own OAuth scopes. The email address is stored as part of the workflow configuration, not linked to a staff account. Workflows continue running after the creating staff member is removed because the workflow itself is authorized independently.
**Lesson Learned:** Understand the authorization model before reporting. Flow workflows operate with store-level authorization, not user-level. A removed staff member's workflow continuing to run is by design — the workflow has its own API credentials.

### Case Study 3: Staff Permissions Can View Customer Data on Orders

**Report:** "Staff with Orders permission can see customer names, emails, and phone numbers"
**Triage Response:** Informative — Intended Behavior
**Why Rejected:** Staff members with Orders permission REQUIRE access to customer contact information to process orders, handle fulfillment, and provide customer service. This is not a permission bypass — it's the intended function of the Orders permission.
**Lesson Learned:** Staff permissions are intentionally broad in areas where data access is necessary for job function. Permission boundaries only become vulnerabilities when data access EXCEEDS what the role requires.

### Case Study 4: CDN Files Are Publicly Accessible

**Report:** "Files uploaded to cdn.shopify.com are accessible without authentication"
**Triage Response:** Informative — Public by Design
**Why Rejected:** CDN-hosted files (product images, theme assets, email templates) are intentionally public. The entire purpose of the CDN is to serve public assets to customers browsing the store.
**Lesson Learned:** Public CDN access is not a vulnerability. The vulnerability would be accessing files that are NOT intended to be public (API keys, database backups, internal configuration).

### Case Study 5: Opening Soon Password Bypass

**Report:** "Storefront password page can be bypassed by accessing the store via direct IP"
**Triage Response:** Informative — Not a Security Boundary
**Why Rejected:** The "Opening Soon" / password-protected storefront page is explicitly documented as NOT a security boundary. It is designed to prevent casual visitors, not determined attackers. Shopify's own documentation confirms it is bypassable.
**Lesson Learned:** Never treat a cosmetic access restriction as a security boundary. Check what Shopify's documentation says about the feature.

### Case Study 6: Cart AJAX Endpoints Have No CSRF Protection

**Report:** "CSRF on /cart/add.js allows adding products to a victim's cart without their consent"
**Triage Response:** Informative — Intentionally Public
**Why Rejected:** Cart endpoints are intentionally unprotected by CSRF tokens. The cart is a public, non-authenticated resource designed to be called from any origin (CORS: `Access-Control-Allow-Origin: *`). Anyone can add items to a cart — that's how shopping works.
**Lesson Learned:** CSRF requires an authenticated action. If the endpoint doesn't require authentication, CSRF protection is irrelevant.

### Case Study 7: Checkout URL Structure Is Standardized

**Report:** "All Shopify stores use the same checkout URL pattern, making checkout tokens predictable"
**Triage Response:** Informative — By Design
**Why Rejected:** While the URL structure is standardized, checkout tokens are cryptographically random (not sequential). Standardized URL structure does not enable enumeration or unauthorized access.
**Lesson Learned:** Structure standardization ≠ vulnerability. The randomness and security of the token is what matters, not the URL pattern.

### Case Study 8: Rate Limiting Not Present on Storefront API Login

**Report:** "No rate limiting on customerAccessTokenCreate mutation allows unlimited login attempts"
**Triage Response:** Informative — Insufficient Impact
**Why Rejected:** While this has been reported multiple times (H1-1363672, H1-708013), the absence of rate limiting alone is not a vulnerability. It must be demonstrated that an attacker can successfully brute-force credentials. Without demonstrated credential compromise, it's a theoretical issue.
**Lesson Learned:** Rate limiting bypass must be CHAINED with demonstrated data access or account compromise. Rate limiting alone is not a vulnerability.

### Case Study 9: Missing CSP Header on Marketing Pages

**Report:** "shopify.com blog has no Content Security Policy header"
**Triage Response:** Informative — Missing Best Practice
**Why Rejected:** CSP is implemented on checkout pages (where PCI compliance requires it) but not on marketing pages. The blog does not process sensitive input, so missing CSP is a hardening recommendation, not a vulnerability.
**Lesson Learned:** Missing security headers must be paired with demonstrated exploitability. A header on a non-sensitive page is a best-practice suggestion.

### Case Study 10: Storefront API Token Visible in Theme JavaScript

**Report:** "Storefront API access token found in theme.liquid and theme.js"
**Triage Response:** Informative — Intentionally Public
**Why Rejected:** Public Storefront API tokens are designed to be embedded in client-side code. They have scope-limited access (unauthenticated read/write for storefront data only). This is documented behavior.
**Lesson Learned:** Not all API tokens are secrets. Public tokens with limited scopes are intentionally exposed.

### Case Study 11: Email Verification Token in URL

**Report:** "Email verification link contains the verification token in the URL — token hijacking possible"
**Triage Response:** Informative — By Design
**Why Rejected:** Email verification tokens MUST be in the URL because the user receives them via email and clicks the link. The token is single-use and time-limited. This is how ALL email verification systems work.
**Lesson Learned:** URL-based tokens for email verification and password reset are standard. The vulnerability is when tokens are reusable, predictable, or never expire, not that they appear in URLs.

### Case Study 12: Self-XSS in Storefront Product Title

**Report:** "Stored XSS in product title — when merchant sets product title to `<script>alert(1)</script>`, it executes on the storefront"
**Triage Response:** Informative — Self-XSS
**Why Rejected:** The merchant would need to inject the malicious product title themselves through the admin panel. The attacker cannot force a merchant to inject content into their own store. This is Self-XSS.
**Lesson Learned:** Storefront XSS only counts if an attacker can inject content WITHOUT merchant admin credentials.

### Case Study 13: Staff Can Export Customer Data

**Report:** "Staff member with Customers permission can export all customer emails and phone numbers"
**Triage Response:** Informative — Intended Functionality
**Why Rejected:** Staff members with Customers permission are intended to be able to view and export customer data for marketing, customer service, and operations. This is the designed functionality of the permission.
**Lesson Learned:** Data export is not a vulnerability when the exporting user has legitimate permission to access the data.

### Case Study 14: Missing HSTS on Non-Checkout Page

**Report:** "blog.shopify.com does not have HSTS header while checkout.shop.myshopify.com does"
**Triage Response:** Informative — Not Exploitable
**Why Rejected:** HSTS is configured where it matters (checkout, admin). Marketing pages and blogs without HSTS cannot be exploited without a working MiTM scenario, which is impractical against a site served entirely over HTTPS.
**Lesson Learned:** Inconsistent security header application across subdomains is not a vulnerability if the critical paths are protected.

### Case Study 15: B2B Quantity Rule Client-Side Bypass

**Report:** "B2B quantity limits can be bypassed by sending direct API requests instead of using the storefront UI"
**Triage Response:** Informative — Expected Behavior
**Why Rejected:** Client-side quantity limits are UX-only. Server-side enforcement is the actual security boundary. Bypassing client-side restrictions without bypassing server-side validation is expected and not a vulnerability.
**Lesson Learned:** Always verify whether the security control is enforced client-side or server-side. Client-side controls are UX, not security.

### Case Study 16: Health Endpoint on Hydrogen Store

**Report:** "Hydrogen/Oxygen store has /healthz endpoint that responds with 200 OK"
**Triage Response:** Informative — Standard Infrastructure
**Why Rejected:** Health check endpoints are standard for any production web application. They are required for load balancer and orchestrator monitoring. They do not expose sensitive data.
**Lesson Learned:** Health endpoints are infrastructure requirements, not vulnerabilities. Only report health endpoints if they leak sensitive data.

### Case Study 17: Storefront Events/Actions API Is Public

**Report:** "Standard storefront events and actions are accessible via JavaScript console"
**Triage Response:** Informative — Intended Behavior
**Why Rejected:** The Standard storefront events and actions API is intentionally public for app developers and theme developers. It exposes page_viewed, product_viewed, and other analytics events that are part of the public Web Pixels API.
**Lesson Learned:** Public JavaScript APIs that are documented and intentional should not be reported.

### Case Study 18: Old API Versions Still Work

**Report:** "Deprecated REST API endpoints from 2024-01 still respond to requests in 2026"
**Triage Response:** Informative — Maintained for Backward Compatibility
**Why Rejected:** Shopify maintains backward compatibility for API versions. Old versions continuing to work is intentional — merchants and apps need time to migrate. No security boundary is crossed.
**Lesson Learned:** Legacy API endpoint availability is not a vulnerability. The vulnerability would be if a legacy endpoint bypasses authorization checks that newer versions enforce.

### Case Study 19: App Bridge Session Tokens in Browser Memory

**Report:** "Session tokens (JWTs) can be found in browser memory via developer tools"
**Triage Response:** Informative — Expected Behavior
**Why Rejected:** Session tokens MUST be accessible to the embedded app for authentication. They have a 1-minute TTL, are encrypted in transit, and are never stored persistently. Finding them in memory is expected.
**Lesson Learned:** The presence of tokens in memory is necessary for the application to function. The security properties are the TTL, encryption, and server-side validation, not the token's invisibility.

### Case Study 20: Customer Account API Token in localStorage

**Report:** "Customer Account API token is stored in localStorage and accessible via JavaScript"
**Triage Response:** Informative — Standard Storage
**Why Rejected:** localStorage is the standard storage mechanism for client-side tokens in headless commerce. The token MUST be accessible to JavaScript for authenticated API requests. Cross-origin isolation prevents other scripts from accessing it.
**Lesson Learned:** localStorage token storage is standard practice. The vulnerability is cross-origin access to the token, not its presence in localStorage.

---

## 13. THE NUANCE OF "CHAIN WITH ANOTHER VULNERABILITY"

### Why Chains Matter

Shopify (and HackerOne) consider the IMPACT of a vulnerability, not just the technical finding in isolation. A single low-severity issue often becomes a critical chain when combined with another vulnerability. Understanding when chains are accepted versus when they are rejected is crucial for bounty hunters.

### The Chain Acceptance Rule

> A vulnerability is eligible if the FULL chain can be demonstrated by an attacker in a realistic scenario. Each link in the chain must be a verifiable weakness — hypothetical or theoretical links make the entire chain ineligible.

### Concrete Chain Examples

#### Chain 1: Open Redirect + XSS → Eligible

**Standalone (Ineligible):**
- Open redirect on `https://shopify.com/redirect?to=https://evil.com` — redirects to external domain. Alone, this is a no-impact finding (cannot steal data, cannot take over accounts).

**Chained (Eligible):**
- Open redirect is used to bypass the redirect_uri whitelist in an OAuth flow:
  1. Victim clicks: `https://store.myshopify.com/admin/oauth/authorize?client_id=APP_ID&redirect_uri=https://shopify.com/redirect?to=https://attacker.com/callback&scope=write_orders`
  2. Victim authorizes the app
  3. Authorization code is sent to `https://shopify.com/redirect?to=https://attacker.com/callback`
  4. Open redirect forwards the code to `https://attacker.com/callback?code=AUTH_CODE`
  5. Attacker exchanges the code for an access token at `https://store.myshopify.com/admin/oauth/access_token`
  6. **Impact:** Full API access to the victim's store (order data, customer PII, financial info)

**Why this chain works:** The open redirect is not theoretical — it's a specific, verifiable redirect parameter. The OAuth flow is a realistic attack scenario. The chain demonstrates concrete data theft.

#### Chain 2: CSRF Logout + Session Fixation → Eligible

**Standalone (Ineligible):**
- CSRF logout on `/account/logout` — can log the victim out, but they can simply log back in. No data compromised.
- Session fixation — session ID not regenerated after login, but attacker has no way to set the victim's session ID.

**Chained (Eligible):**
- Researcher chained XSS (to set the session cookie) with session fixation (session ID not regenerated) to gain authenticated access:
  1. Attacker obtains a pre-login session cookie from the target site
  2. Attacker injects that cookie into the victim's browser via XSS or other means
  3. Victim logs in (session ID stays the same — session fixation)
  4. Attacker now has the same session ID and accesses victim's authenticated session
  5. **Impact:** Full account takeover

**Why this chain works:** The XSS provides the cookie-injection mechanism, and session fixation provides the persistence. Both vulnerabilities are real and verifiable. H1-423136 ($5,000 bounty) used this exact chain.

#### Chain 3: SSRF + Cloud Metadata → Eligible

**Standalone (Ineligible):**
- SSRF that can only make HTTP requests to external domains — no access to internal services, no data exfiltration.

**Chained (Eligible):**
- SSRF is used to access cloud provider metadata endpoints:
  1. App proxy or vulnerable endpoint accepts a URL parameter
  2. Parameter bypasses URL restrictions (e.g., by using `http://169.254.169.254/` encoded, via redirect, or via DNS rebinding)
  3. Server requests AWS/GCP metadata at `http://169.254.169.254/latest/meta-data/`
  4. Returns IAM credentials, instance profile, security group info
  5. Attacker uses IAM credentials to access cloud resources
  6. **Impact:** Cloud infrastructure compromise, data exfiltration from internal services

**Why this chain works:** The SSRF is not restricted to external domains — it can reach internal IP ranges. Cloud metadata endpoints are well-known and reliably accessible from cloud-hosted infrastructure. The IAM credentials provide concrete access escalation.

#### Chain 4: Rate Limit Bypass + Brute-Force → Eligible

**Standalone (Ineligible):**
- Rate limit bypass via GraphQL aliasing — can send 10,000 login attempts in a single HTTP request. Alone, this is a bypass without demonstrated impact.

**Chained (Eligible):**
- Rate limit bypass enables brute-force credential stuffing:
  1. Attacker obtains a list of email/password pairs (from a previous breach)
  2. Uses GraphQL alias batching to send 500 login attempts in one HTTP request
  3. Bypasses per-request rate limiting (server sees 1 request, executes 500 mutations)
  4. One credential pair works — attacker gains access to a customer account
  5. Accesses order history, shipping addresses, saved payment methods
  6. **Impact:** Account takeover, PII theft, potential financial fraud

**Why this chain works:** The rate limit bypass directly enables the brute-force attack. The attacker has realistic credential lists (from data breaches). The account access provides concrete data theft. Previous HackerOne reports (H1-1363672) have confirmed rate limit bypass on Storefront API but required chaining with actual credential compromise for bounty.

#### Chain 5: GraphQL Introspection + Data Extraction → Eligible

**Standalone (Ineligible):**
- GraphQL introspection reveals the full API schema — types, fields, mutations, descriptions. Alone, this is intended behavior.

**Chained (Eligible):**
- Introspection is used to discover undocumented or insufficiently authorized mutations:
  1. Attacker runs introspection on the GraphQL Admin API
  2. Discovers a mutation that should require admin permissions but doesn't (e.g., `billingDocumentDownload` or `billDetails`)
  3. Uses the discovered mutation to access other merchants' billing data
  4. Enumeration of sequential billing IDs reveals hundreds of merchants' financial information
  5. **Impact:** Mass data leakage of financial documents (H1-2207248)

**Why this chain works:** The introspection itself is not the vulnerability — it's the reconnaissance tool. The vulnerability is the IDOR in the discovered mutation. The chain is: introspection (tool) → discovery of IDOR (vulnerability) → data extraction (impact).

#### Chain 6: Email Verification Bypass + Cross-System Trust → ATO ($22,500)

**Standalone (Ineligible individually):**
- POS staff update endpoint lacks email confirmation (Low severity)
- Partner Dashboard marks emails as "verified" during store activation (Informational)

**Chained (Eligible):**
1. Create dev store with attacker's email → activation link clicks → email tagged "verified"
2. Use POS endpoint to change staff account email to VICTIM's email (no confirmation sent)
3. Create Shopify ID using victim's email → system sees "already verified" → no confirmation
4. Set password for victim's Shopify ID → full store takeover
5. **Impact:** Complete silent account takeover, orders, customer data, payment configs, apps. No notification to victim. Bounty: $22,500.

**Why this chain works:** Each link is a verifiable weakness. The cross-system trust flaw is the critical enabler — Partner Dashboard's verification status propagates to Shopify ID creation without re-verification.

### When Chains Are NOT Accepted

1. **Theoretical chains:** "An attacker could XSS a staff member AND then use CSRF to create a new admin" — requires the victim to click an XSS link AND be logged into admin. If the XSS is Self-XSS or the CSRF requires multiple unlikely actions, the chain is theoretical.

2. **Cross-program chains:** "This vulnerability in Shopify could be combined with a vulnerability in Chrome" — Shopify doesn't accept chains that require browser zero-days or other non-Shopify vulnerabilities.

3. **Physical access chains:** "This vulnerability requires physical access to the victim's unlocked phone" — physical access bypasses all digital security, making the Shopify vulnerability irrelevant.

4. **Social engineering chains:** "An attacker could call Shopify Support and..." — social engineering is explicitly out of scope for all HackerOne programs.

5. **Missing prerequisite chains:** "If the attacker already has admin access to the store, they could..." — the chain must start from a position an attacker could realistically achieve without already having the target access.

### Key Chain Decision Tree

```
Found a low-severity issue?
├── Can it be chained with another Shopify vulnerability?
│   ├── YES → Can you demonstrate the FULL chain from attacker to impact?
│   │   ├── YES → Report the FULL chain (highest bounty for the highest impact link)
│   │   └── NO → Keep researching; the chain is theoretical
│   └── NO → Is the standalone impact sufficient?
│       ├── YES → Report as-is
│       └── NO → Abandon or hold for future chaining
│
├── Does the chain require third-party app vulnerabilities?
│   └── Report to app developer, not Shopify
│
├── Does the chain require browser zero-days?
│   └── Not accepted — Shopify assumes modern, secure browsers
│
└── Does the chain require physical access or social engineering?
    └── Not accepted — explicitly out of scope
```

---

## 14. SPECIFIC HUNTING PITFALLS FOR SHOPIFY

### Pitfall 1: Testing Against Other Merchants' Stores (BANNED)

**The Mistake:** Testing a vulnerability against a live merchant's store instead of your own test store. This includes:
- Placing test orders on real merchant stores
- Attempting IDOR against real merchant data
- Running scanners against merchant storefronts
- Accessing admin panels of stores you don't own

**The Consequence:** Immediate ban from the Shopify HackerOne program. Possible legal action. Shopify explicitly requires testing ONLY against stores you created via `partners.shopify.com/signup/bugbounty`.

**Why It Happens:** Hunters are eager to demonstrate "real" impact and assume they won't get caught. However, Shopify monitors traffic patterns and can detect unauthorized testing. Even if the vulnerability is real, testing against live merchants violates program rules and invalidates the finding.

**The Correct Approach:** Create your own test stores with realistic data. Use the `@wearehackerone.com` email alias. If you need to demonstrate cross-tenant access, create TWO test stores and show data access between them.

### Pitfall 2: Contacting Shopify Support About Bounty (Disqualification)

**The Mistake:** Emailing, calling, or live-chatting Shopify Support to ask about a bug bounty report, payment status, or vulnerability question.

**The Consequence:** Immediate report closure, potential program suspension. Shopify Support is for MERCHANTS — bug bounty communications go through HackerOne ONLY.

**Why It Happens:** Hunters get impatient waiting for triage and think contacting Support will speed things up. Instead, it creates confusion — Support agents forward tickets to the security team, who then see that the hunter bypassed the proper HackerOne channel.

**The Correct Approach:** All communications — report submission, clarification questions, payment inquiries, appeals — go through the HackerOne platform. Use the HackerOne comment system to communicate with the triage team.

### Pitfall 3: Testing on Production Stores Instead of Dev Stores

**The Mistake:** Running vulnerability tests against a store that has real customers, real orders, and real payment data.

**The Consequence:** Even if you own the store, testing on a production store can affect real customer data. You could accidentally:
- Corrupt order data
- Trigger fraudulent transaction alerts
- Impact customer accounts
- Generate spam emails to real customers

**Why It Happens:** Hunters want to test with "realistic" data and assume their own production store is safe. However, development stores provide the same functionality without the risk.

**The Correct Approach:** Always use development stores for testing. Development stores have all the same features (B2B, Markets, Functions, etc.) but with no real customers or orders. If you need realistic data, seed your dev store with test data.

### Pitfall 4: Reporting GraphQL Introspection Alone

**The Mistake:** Running an introspection query on a Shopify GraphQL endpoint and reporting it as an information disclosure vulnerability.

**The Consequence:** Immediate closure as "Informative — Intended Behavior." Shopify has confirmed multiple times (including H1-2886723) that GraphQL introspection is intentionally enabled on ALL endpoints.

**Why It Happens:** On many bug bounty programs, hidden GraphQL introspection is a valid finding. Hunters new to Shopify assume the same applies here. But Shopify explicitly designs for introspection to be enabled for developer experience.

**The Correct Approach:** Use introspection as a TOOL for finding real vulnerabilities. Look for undocumented mutations, fields that leak data, or insufficient authorization on discovered operations. Report the AUTHORIZATION issue, not the introspection.

### Pitfall 5: Reporting Rate Limiting Alone

**The Mistake:** Discovering and reporting that an API endpoint has weak or missing rate limiting.

**The Consequence:** Closure as "Informative — Insufficient Impact." Rate limiting alone — even if completely absent — is not a vulnerability. The impact must be demonstrated through successful brute-force, data access, or account compromise enabled by the rate limit gap.

**Why It Happens:** Many programs accept rate limiting findings. Shopify requires demonstrated impact. The absence of rate limiting is only relevant if an attacker can USE that absence to achieve something harmful.

**The Correct Approach:** If you find missing rate limiting on a login endpoint, PROVE it can be brute-forced by actually cracking a weak password. If you find missing rate limiting on an OTP endpoint, PROVE you can enumerate valid codes. Include the successful attack in your report.

### Pitfall 6: Reporting Staff Permission Edge Cases Without Impact

**The Mistake:** Finding a staff member can see slightly more data than you think they should, but the data is still within the scope of their job function.

**The Consequence:** Closure as "Informative — Intended Behavior." Shopify's staff permission system is intentionally broad in some areas. A staff member with "Orders" permission seeing customer phone numbers on orders is necessary for fulfillment.

**Why It Happens:** Hunters assume any data access by a non-admin is a permission bypass. However, Shopify's permission model grants access based on role requirements, not a strict least-privilege model.

**The Correct Approach:** The boundary is: can a staff member access data that is CLEARLY UNRELATED to their role? For example:
- "Products" staff accessing customer payment data → potentially in scope
- "Orders" staff accessing customer names on orders → out of scope (necessary for fulfillment)
- "Analytics" staff modifying product prices → in scope
- "Analytics" staff viewing revenue reports → out of scope (the entire point of analytics)

### Pitfall 7: Reporting CDN XSS Without Cross-Context Impact

**The Mistake:** Uploading an HTML file (with embedded JavaScript) to the Shopify CDN and reporting it as stored XSS.

**The Consequence:** Closure as "Informative — Self-XSS / Isolated Origin." Files on `cdn.shopify.com` are on a different origin than storefronts (`*.myshopify.com`) and admin (`admin.shopify.com`). The XSS is isolated to the CDN origin and cannot access cookies or data from other origins.

**Why It Happens:** Hunters see "I can execute JavaScript on a Shopify domain" and immediately think XSS. They forget the critical detail: the script must execute in the SAME ORIGIN as the target data. CDN-origin scripts cannot access storefront cookies or admin data.

**The Correct Approach:** For CDN XSS to be reportable, you must demonstrate cross-context impact. For example:
- The CDN file is loaded via a script tag on the storefront (allowing access to storefront cookies)
- The CDN file is loaded as a JSONP callback (allowing data injection)
- The CDN origin hosts a trusted script that the storefront or admin imports

### Pitfall 8: Reporting Self-XSS That Requires Developer Tools

**The Mistake:** Finding that a URL parameter reflects in the page content and claiming XSS, but the payload requires HTML encoding or browser quirks to execute.

**The Consequence:** Closure as "Informative — Self-XSS / Requires Developer Tools." If the victim needs to manually inspect the page, edit HTML, or paste into console, it's not a vulnerability.

**Why It Happens:** Hunters test with `alert(1)` in the URL and see their payload reflected. Without checking if modern browsers actually execute it (due to CSP, encoding, or XSS auditor), they assume it's valid XSS.

**The Correct Approach:** Verify XSS executes in a STANDARD browser with DEFAULT settings. Test in Chrome, Firefox, and Safari. If it only works when you disable CSP, edit the DOM, or use a deprecated browser version, it's not a valid XSS.

### Pitfall 9: Reporting Theoretical OAuth Redirect URI Issues

**The Mistake:** Finding that Shopify's own OAuth flow has a permissive redirect_uri validator and reporting it.

**The Consequence:** This can actually be valid if demonstrated properly. The pitfall is REPORTING IT WITHOUT A COMPLETE CHAIN. Many hunters report open redirect in OAuth but fail to show how an attacker would get the victim to authorize a malicious app.

**Why It Happens:** OAuth redirect_uri vulnerabilities are complex. Just finding that `https://shopify.com/redirect?to=https://evil.com` is an accepted redirect_uri doesn't complete the chain — you need to show how the victim arrives at the OAuth authorization URL with the attacker's redirect_uri.

**The Correct Approach:** Demonstrate the FULL chain:
1. Register a malicious app on Shopify (or show how an attacker could)
2. Craft the OAuth authorization URL with the malicious redirect_uri
3. Show the authorization code being sent to your server
4. Exchange the code for an access token
5. Use the token to access store data

### Pitfall 10: Reporting Old CVEs Without Verifying Patch Status

**The Mistake:** Searching for CVE-2024-45718, CVE-2024-45719, or CVE-2024-45720 (known Hydrogen health endpoint issues) and reporting them as new findings.

**The Consequence:** Immediate closure as "Duplicate — Known Issue / Already Patched." These CVEs were published in 2024 and have been fixed. Reporting them wastes everyone's time.

**Why It Happens:** Hunters don't check the Shopify Known Issues page or search for existing CVEs before testing. They test, find the vulnerability, and report without realizing it's been known for years.

**The Correct Approach:** Before testing, check:
- Shopify Bug Bounty Known Issues page
- NVD/CVE database for Shopify CVEs
- HackerOne disclosed reports for similar findings
- GitHub security advisories for Shopify repositories

---

## 15. SHOPIFY SECURITY TEAM EXPECTATIONS

### What the Triage Team Wants

Shopify's triage team reviews 60-70+ reports per week. They have limited time for each report. Reports that are clear, concise, and demonstrate real impact get prioritized. Reports that are vague, theoretical, or incomplete get closed quickly.

#### Expectation 1: Clear Reproduction Steps

**What They Expect:**
- Step-by-step instructions that they can follow in order
- Each step should include: URL, HTTP method, request body, headers
- Exact payloads and parameters used
- Expected behavior vs. actual behavior
- Any prerequisites (e.g., "requires two test stores with different plans")

**Example of GOOD reproduction steps:**
```
1. Create Store A (shop-a.myshopify.com) and Store B (shop-b.myshopify.com)
2. On Store A, create a product with ID 123 under "Products > Add Product"
3. On Store B, navigate to /admin/products.json
4. Observe that Store B's response INCLUDES Store A's product ID 123
5. Expected: Store B should only see its own products
6. Actual: Store B sees Store A's products (cross-tenant data leakage)
```

**Example of BAD reproduction steps:**
```
1. Go to the admin panel
2. Look at the JSON endpoint
3. You can see other stores' data
4. This is a security issue
```

#### Expectation 2: Impact Demonstration

**What They Expect:**
- Clear explanation of WHAT an attacker can do
- Clear explanation of WHAT data can be stolen or modified
- Financial or business impact assessment
- CVSS or severity estimation (using Shopify's calculator at shopify.github.io/appsec/cvss_calculator/)

**Example of GOOD impact demonstration:**
```
Impact: An attacker with a compromised staff account (Products permission only) can
access the full customer database by calling /admin/api/2026-07/customers.json.
This exposes 10,000+ customer records including names, emails, phone numbers, and
shipping addresses. This violates GDPR Article 32 (security of processing) and could
lead to regulatory fines of up to €20M or 4% of annual turnover.

CVSS: 8.1 (High) — AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N
```

**Example of BAD impact demonstration:**
```
Impact: Someone could steal data. This is bad for security. Please fix.
```

#### Expectation 3: Two-Account Differential for IDOR

**What They Expect:**
- Two separate test accounts or stores with distinct, identifiable data
- A clear demonstration that Account A's data is accessible from Account B's session
- Screenshots or HAR files showing the request and response from both accounts
- Explanation of the authorization gap

**Why It Matters:** IDOR requires proof that the authorization boundary is crossed. Showing data from one account is not enough — you must show that ANOTHER account's data is accessible.

**Good approach for IDOR:**
```
Store A: Create product "UNIQUE-VULN-TEST-A-12345" with SKU "TEST-A"
Store B: Create product "UNIQUE-VULN-TEST-B-67890" with SKU "TEST-B"
Both stores: Create staff accounts with "Products" permission only

Step 1: Authenticate to Store A's admin API
Step 2: Request /admin/api/2026-07/products.json?sku=TEST-B
Step 3: Response includes Store B's product "UNIQUE-VULN-TEST-B-67890"
Step 4: This proves cross-tenant data access
```

#### Expectation 4: Working Proof-of-Concept

**What They Expect:**
- A PoC that the triage team can reproduce in under 5 minutes
- Ideally a script, Burp request file, or HAR export
- Screenshots or screen recordings for visual impact
- Clear demonstration of the vulnerability working against YOUR OWN test stores
- Cache busters used when testing CDN/cache attacks

**Good PoC formats:**
- **Python script:** `python3 poc.py` — does the entire chain automatically
- **Burp suite:** Save as .burp request file with instructions
- **HAR file:** Export from browser dev tools
- **Screen recording:** <60 seconds, showing the attack from start to finish
- **curl commands:** Exact commands that can be pasted into a terminal

**Bad PoC examples:**
- "Just try it and you'll see" (vague)
- "I can show you in a screen share" (triage doesn't do live calls)
- A 20-page PDF with no executable steps (too much noise, no signal)

#### Expectation 5: Concise Reports

**What They Expect:**
- Title: Clear and descriptive (e.g., "IDOR on /admin/api/2026-07/customers.json allows cross-store customer data access")
- Summary: 2-3 sentences about the vulnerability
- Impact: 3-5 sentences about the business risk
- Reproduction: Step-by-step with exact requests
- PoC: Code, screenshots, or HAR file
- Remediation suggestion: Optional but appreciated

**What They DON'T Want:**
- 20 pages of background research
- Multiple vulnerabilities in one report (file separate reports)
- Screenshots of source code you shouldn't have access to
- Personal information of other users or merchants
- Rants about how Shopify should do better
- Speculation about what ELSE might be possible

### The Triage Timeline

| Stage | Typical Timeframe | What Happens |
|---|---|---|
| Submission | Day 0 | Report submitted via HackerOne |
| Initial triage | 24-72 hours | Team reviews for validity, scope, and impact |
| Clarification | 1-7 days | If needed, team asks clarifying questions |
| Bounty decision | 1-4 weeks | Valid findings receive bounty and severity rating |
| Fix development | 30-90 days | For accepted findings, team develops fix |
| Public disclosure | After fix | Coordinated disclosure (90-120 day typical timeline) |

### How to Get the Best Response from Triage

1. **Use the right severity.** Use Shopify's CVSS calculator at shopify.github.io/appsec/cvss_calculator/. Overrating severity (reporting a low as critical) wastes everyone's time. Underrating can undervalue your finding.

2. **Be responsive.** Answer clarification questions within 24 hours. If you go silent for a week, the report may be closed.

3. **Be professional.** Triagers are human. Aggressive, entitled, or demanding language damages your reputation. A polite "thank you" goes a long way.

4. **Accept "Informative" gracefully.** If the team explains why your finding is intended behavior, accept it and move on. Arguing extensively damages your reputation. If you genuinely believe the team missed something, provide ONE concise rebuttal.

5. **Keep learning.** Every Informative response is a learning opportunity. Update your personal knowledge base and this guide with what you learned.

### The Golden Rule Revisited

> **If the impact requires chaining with another vulnerability (XSS, CSRF, MITM, physical access) to be meaningful, it is likely NOT a reportable finding on its own.**

But if you can DEMONSTRATE the full chain — from attacker action to concrete impact — it IS reportable, and the bounty reflects the chain's total impact, not just the individual links.

---

## 16. BY DESIGN — NOT VULNERABILITIES

This section explicitly separates things that are **architecturally by design** (not bugs, not security issues) from things that are merely ineligible.

For each by-design item:
- **What it is**
- **Why Shopify designed it this way** (architectural intent)
- **Why it's NOT a vulnerability** (technical justification)
- **What would actually be a vulnerability in this area** (so hunters know where the line is)

### 16.1 Admin Staff JSON Endpoints

**What it is:** `/admin/settings/*.json` and similar staff-only JSON endpoints that return store settings and configuration data in machine-readable format.

**Why Shopify designed it this way:** The admin panel is built as a single-page application (SPA) that consumes JSON APIs. Every HTML admin page has a corresponding `.json` endpoint that powers the UI. Staff members need programmatic access to settings via API for efficiency and for building custom tools.

**Why it's NOT a vulnerability:** All `.json` endpoints require staff authentication — the same authentication required for the HTML version. Appending `.json` to an admin URL returns the same data in JSON format; it does not bypass permissions. The endpoints are documented and consistent with RESTful API design principles.

**What WOULD be a vulnerability:** If unauthenticated users could access these JSON endpoints (authentication bypass). If the JSON endpoint returned MORE data than the HTML version (information disclosure). If a staff member with limited permissions could access JSON endpoints for functions beyond their role (authorization bypass). Cross-tenant data leakage would also be a vulnerability.

### 16.2 CDN File Hosting (cdn.shopify.com)

**What it is:** Merchants can upload files (images, PDFs, CSS, JS) to their own CDN space on `cdn.shopify.com` via the admin file uploader. These files are served publicly without authentication.

**Why Shopify designed it this way:** Storefronts need to serve public assets — product images, theme stylesheets, and JavaScript files — to customers browsing the store without requiring login. The CDN is designed for public content delivery at global scale with edge caching. Files are organized per-store but served from a shared CDN domain.

**Why it's NOT a vulnerability:** A merchant uploading their own files to their own CDN space is expected behavior. The CDN serves public content by design. Product images, theme CSS/JS, and email templates must be publicly accessible for the store to function. Files on `cdn.shopify.com` are on a separate origin from storefronts (`*.myshopify.com`) and admin (`admin.shopify.com`), so any script execution in a CDN file is sandboxed to the CDN origin and cannot access cookies or data from other origins.

**What WOULD be a vulnerability:** Cross-tenant CDN access — merchant A reading merchant B's uploaded files using predictable URLs or directory traversal. Direct CDN upload without admin authentication. CDN cache poisoning that serves malicious content instead of legitimate files (H1-1695604 was a $3,800 finding for cache-poisoning DoS). Upload of files that overwrite system-level files (not merchant-uploaded files).

### 16.3 GraphQL Introspection

**What it is:** The GraphQL Admin API (`/admin/api/*/graphql.json`) and Storefront API (`/api/*/graphql.json`) respond to introspection queries like `{ __schema { types { name fields { name } } } }`, revealing the complete schema including types, fields, arguments, and descriptions.

**Why Shopify designed it this way:** Shopify intentionally enables GraphQL introspection on ALL GraphQL APIs to support developer experience (DX). Developers need to discover the schema to build integrations, apps, and custom storefronts. Shopify CLI, IDE plugins, and GraphQL tooling (GraphiQL, Apollo Studio) rely on introspection for autocomplete, documentation, and query validation.

**Why it's NOT a vulnerability:** The schema only contains type definitions — not data. Introspection reveals what you CAN query, not what you SHOULD query. Report #2886723 was closed as "Informative — Intended Behavior." Admin API introspection requires a valid OAuth token. Storefront API introspection is intentionally public. Schema visibility is standard GraphQL practice used by Shopify CLI, partners, and apps worldwide.

**What WOULD be a vulnerability:** If introspection revealed sensitive data (customer PII, credentials, API keys) — which it doesn't. If introspection uncovers undocumented mutations that bypass permission checks, report the SPECIFIC mutation, not the introspection itself. Using introspection as reconnaissance to find IDOR or authorization bypass in discovered operations is valid — the vulnerability is the missing authorization, not the schema visibility.

### 16.4 Opening Soon / Password Protection

**What it is:** Storefront password gate that merchants can enable during trial, maintenance, or pre-launch. Visitors must enter a password to view the storefront.

**Why Shopify designed it this way:** The password page is a cosmetic feature designed to prevent casual visitors from seeing an unfinished store under construction. It is explicitly documented as NOT a security boundary — it's equivalent to a "Coming Soon" sign on a physical storefront.

**Why it's NOT a vulnerability:** Bypassing the password page reveals only the merchant's own store content that the merchant intentionally makes public. The password can be bypassed via direct IP access, alternative endpoints, or by appending `/password` to the URL — all documented behaviors. Shopify's official documentation notes the password page is bypassable and recommends proper authentication (customer accounts, staff login) for real security boundaries.

**What WOULD be a vulnerability:** If bypassing the password page revealed OTHER merchants' stores or admin access. If the password gate prevented access to authenticated resources but could be bypassed (e.g., bypassing admin login via the password page). If the password mechanism itself had a cryptographic weakness (predictable tokens, brute-forceable passwords).

### 16.5 POS PIN (4-Digit)

**What it is:** A 4-digit PIN used for employee access to Shopify POS devices in retail environments.

**Why Shopify designed it this way:** The POS PIN is designed for convenience in a retail environment where employees need quick access to process transactions. A 4-digit PIN with no rate limiting is a deliberate tradeoff between security and usability — retail staff need to complete transactions quickly during busy periods.

**Why it's NOT a vulnerability:** The PIN length is a merchant choice, not a Shopify security boundary. If an attacker has physical access to the POS device, brute-forcing a 4-digit PIN is a physical security issue, not a Shopify vulnerability. The POS PIN is designed for quick employee access, not as a hardened authentication mechanism for remote access.

**What WOULD be a vulnerability:** If the POS PIN could be bypassed REMOTELY without physical access (remote authentication bypass). If PIN verification could be bypassed programmatically (API endpoint accepts any PIN). If the PIN is stored in plaintext or transmitted without encryption.

### 16.6 HTML in Product Descriptions / Rich Text Editor

**What it is:** Shopify's rich text editors (TinyMCE, etc.) allow merchants to embed HTML including `<script>` tags in product descriptions, blog posts, collection pages, and other content fields.

**Why Shopify designed it this way:** Merchants need to embed custom content — videos, maps, embeds, interactive elements — in their product descriptions and blog posts. The Rich Text Editor intentionally supports full HTML to give merchants complete control over their storefront content.

**Why it's NOT a vulnerability:** The merchant would need to inject the malicious content themselves through the admin panel. An attacker cannot force a merchant to inject content into their own store without already having admin credentials. Any XSS executes only in the merchant's own storefront context. This is self-XSS within the merchant's own store — the merchant controls what goes into their store, and if they inject malicious JavaScript, they are harming their own customers.

**What WOULD be a vulnerability:** If injected content could affect OTHER merchants' stores (cross-tenant stored XSS). If an attacker could inject content into a merchant's product description WITHOUT admin credentials (via third-party app vulnerability, review system, or contact form). If the rich text renderer had a server-side vulnerability like SSTI via Liquid rendering.

### 16.7 MCP Server — Read-Only Data Exposure

**What it is:** The Storefront MCP (Model Context Protocol) server exposes tools like `product_search`, `cart_create`, `checkout_create`, `order_status`, and `return_create` without authentication. The Customer Accounts MCP server requires a valid token. The Dev MCP server runs locally via stdio.

**Why Shopify designed it this way:** MCP is an open standard for AI agents to interact with external tools and data. Shopify has embraced MCP as the standard for Agentic Commerce — AI agents that shop, manage stores, and perform commerce tasks autonomously. The Storefront MCP mirrors the public Storefront API, which is intentionally unauthenticated for customer-facing operations.

**Why it's NOT a vulnerability:** The Storefront MCP tools do not require authentication because they mirror public Storefront API functionality — product search, cart creation, and checkout initiation are all intentionally public. Tool names and schema descriptions are public information designed for AI agent discovery. The Dev MCP server runs on the developer's local machine only. Customer Accounts MCP requires a valid customer token. These are all by-design architectural decisions.

**What WOULD be a vulnerability:** If the MCP server exposed credentials, API keys, or PII. If MCP tools accessed ADMIN-level data (orders, customers, products) without authentication. If the Customer Accounts MCP server accepted falsified tokens or operated without proper authorization scope checks. If the Dev MCP server exposed network-accessible endpoints without authentication.

### 16.8 Sidekick AI

**What it is:** Shopify Sidekick is an AI assistant with a purple glasses icon in the Shopify admin. It answers questions about store performance, generates content, creates discount codes, builds Flow workflows, and performs admin actions via natural language.

**Why Shopify designed it this way:** Sidekick is designed to help merchants manage their stores more efficiently using natural language. It needs access to the merchant's own data (orders, products, customers, analytics) to answer questions and perform actions. Sidekick respects admin permissions — staff members only see data they are authorized to access.

**Why it's NOT a vulnerability:** Sidekick accessing the authenticated merchant's own orders, products, and customers is the intended function. It operates within the same permission boundaries as the admin panel. The data exposure is limited to what the authenticated staff member can already see. Sidekick cannot access data outside the staff member's permission scope. There is no public Sidekick API — it's a first-party UI feature, which reduces attack surface.

**What WOULD be a vulnerability:** Sidekick leaking data between merchants (cross-tenant data access). Sidekick performing unauthorized actions via prompt injection — if a crafted product description causes Sidekick to exfiltrate data or perform destructive admin actions. Sidekick bypassing admin permission boundaries. Sidekick extension accessing data beyond its declared scope.

### 16.9 Storefront API Public Access

**What it is:** The Storefront GraphQL API is accessible without authentication (tokenless) for basic queries up to 1,000 query cost. Public access tokens are embedded in theme JavaScript. Tokenless access allows querying products, collections, cart, search, pages, blogs, and articles.

**Why Shopify designed it this way:** Storefronts need to be accessible to shoppers without requiring login — this is the fundamental nature of e-commerce. The Storefront API is designed for headless commerce implementations where the storefront may be hosted on any domain. Tokenless access provides limited read-only access to public catalog data while restricting write operations and sensitive data access.

**Why it's NOT a vulnerability:** Querying product and catalog data from the Storefront API is intended behavior for shoppers. Public tokens are intentionally scope-limited to unauthenticated storefront operations. The 1,000 query cost limit prevents abuse of anonymous access. Cart operations are designed to be public because any shopping visitor needs to add items to a cart.

**What WOULD be a vulnerability:** Accessing admin-level data through the Storefront API (authorization bypass). Modifying data without proper authentication (write operations without token). Accessing private metafields or customer PII through the Storefront API without proper scopes. Using the Storefront API to enumerate customer accounts or perform credential stuffing.

### 16.10 Rate Limiting Is Not a Vulnerability

**What it is:** API rate limits exist across Shopify's platform: 40 req/s for REST Admin API (standard), 1,000 point bucket for GraphQL Admin API (standard), dynamic limits for Storefront API. Headers like `X-Shopify-Shop-Api-Call-Limit` and `extensions.cost.throttleStatus` report current usage.

**Why Shopify designed it this way:** Rate limits are operational controls designed to ensure platform stability, fair resource allocation, and protection against abusive traffic patterns. They are not security boundaries — they are performance management tools.

**Why it's NOT a vulnerability:** Being rate limited is expected behavior when API usage exceeds thresholds. The absence of rate limiting on a specific endpoint is not a vulnerability unless an attacker can USE that absence to achieve actual harm (credential compromise, data theft). Rate limits vary by plan (Standard, Advanced, Plus) intentionally. Storefront API limits are intentionally undocumented to prevent gaming.

**What WOULD be a vulnerability:** If rate limits could be bypassed to enable successful brute-force attacks (credential compromise demonstrated). If rate limit bypass allowed unlimited OTP/coupon enumeration leading to account takeover. If the absence of rate limiting on a payment endpoint allowed financial fraud. The vulnerability is the successful attack enabled by the rate limit gap, not the gap itself.

### 16.11 Email Verification During Signup

**What it is:** No email verification is required during HackerOne bug bounty signup or Shopify ID creation. Users can create accounts with unverified email addresses.

**Why Shopify designed it this way:** Shopify accepts unverified emails during signup to reduce friction and allow users to explore the platform before committing to verification. This is a deliberate tradeoff between security and user experience — unverified accounts have limited functionality.

**Why it's NOT a vulnerability:** An unverified email = a lower-trust account with restricted capabilities. Verified email = the ability to accept bounties, install apps, and access full functionality. Shopify has implemented additional controls (rate limiting, CAPTCHA) to prevent abuse of unverified accounts. The lack of upfront verification is not a security boundary — it's a graduated trust model.

**What WOULD be a vulnerability:** If unverified emails could access verified-only features (bounty payments, app installation, store creation without additional checks). If an attacker could use an unverified account to take over a verified account. If email verification could be bypassed to gain unauthorized access to another user's store — this was the $22,500 ATO chain where POS endpoint + Partner Dashboard trust flaw allowed account takeover without email verification.

### 16.12 CORS Headers on Public Endpoints

**What it is:** Public API endpoints (Storefront API, cart AJAX endpoints) have permissive CORS headers like `Access-Control-Allow-Origin: *`. Admin API endpoints have restrictive CORS.

**Why Shopify designed it this way:** Storefronts need to be embeddable via AJAX from any domain — this is required for headless commerce where the storefront may be hosted on a custom domain. Cart AJAX endpoints (`/cart/add.js`, `/cart/update.js`, `/cart/change.js`) are designed to be called from any origin because they are public, unauthenticated endpoints.

**Why it's NOT a vulnerability:** CORS on public data is expected and necessary for web functionality. The cart is a public, non-authenticated resource — CORS restrictions would break headless commerce implementations. Admin API endpoints are properly restricted with CORS to prevent cross-origin credential theft.

**What WOULD be a vulnerability:** If admin API endpoints had permissive CORS allowing credential theft via cross-origin requests. If a sensitive authenticated endpoint (password change, payment configuration) had `Access-Control-Allow-Origin: *` allowing an attacker to read the response.

### 16.13 Web Pixel API Capabilities

**What it is:** Web Pixels can access customer event data (cart contents, order data, customer email, name, phone), subscribe to analytics events, read/write cookies and localStorage via the Standard API, and send data to external endpoints via fetch().

**Why Shopify designed it this way:** Web Pixels are designed for analytics, marketing, and personalization. They need access to customer event data to provide analytics, tracking, and personalization services. The data access is intentional and configurable via declared scopes in `shopify.extension.toml`.

**Why it's NOT a vulnerability:** Web Pixels run in the merchant's own storefront context. App Pixels execute in a strict sandbox (Web Worker with no DOM access) that prevents scraping of checkout fields, PII entry, or credit card numbers. Custom Pixels (merchant-created) use a lax sandbox but are created by the merchant for their own store. All Pixel fetch() calls require CORS support on the external endpoint, preventing arbitrary data exfiltration.

**What WOULD be a vulnerability:** If Web Pixels could access the admin panel or cross-tenant data. If a Pixel could access data beyond its declared scopes (accessing `read_customer_email` without declaring the scope). If the sandbox could be escaped to access the DOM or parent frame context, enabling Magecart-style checkout skimming.

### 16.14 Checkout Kit / Shop App Integration

**What it is:** Checkout Kit runs in a WebView within the Shop app (or embeddable via web component). It uses JWT authentication, requires CSP allowlisting, and operates via Embedded Checkout Protocol (ECP) over JSON-RPC 2.0.

**Why Shopify designed it this way:** Checkout Kit provides a native checkout experience within the Shop app and other mobile/web surfaces. The WebView is the intended checkout surface for mobile commerce. JWT authentication ensures the checkout session belongs to the correct buyer.

**Why it's NOT a vulnerability:** The WebView follows the device security model — if the device is secure, the checkout is secure. Session tokens have a 5-minute TTL with nonce (jti) for replay prevention. Client credentials must never be in client-side code (documented requirement). The inline mode's third-party cookie requirement is a browser limitation, not a Shopify vulnerability.

**What WOULD be a vulnerability:** If checkout data could be exfiltrated across app boundaries (WebView sandbox escape). If JWT tokens could be forged or reused across different buyer sessions. If `client_secret` is exposed in mobile app binaries (Shopify's official credentials, not third-party apps). If the Checkout Kit could be used to bypass payment.

### 16.15 Customer Account API (Public)

**What it is:** The Customer Account API (GraphQL) allows customers to access their own data: orders, addresses, profile information, store credit. Authentication uses Customer Account API tokens (JWT-based) stored in localStorage.

**Why Shopify designed it this way:** Customers need access to their own data — order history, shipping addresses, and account settings. The API enables headless commerce implementations and custom storefronts where customers manage their accounts. The token-in-localStorage pattern is standard for modern web applications.

**Why it's NOT a vulnerability:** A customer seeing their own data is intended functionality. The Customer Account API token is scoped to the customer's own resources — it cannot access other customers' data, admin functionality, or store configuration. The token must be accessible to JavaScript for authenticated requests (standard OAuth bearer token pattern). Cross-origin isolation (CORS) prevents other scripts from accessing the token.

**What WOULD be a vulnerability:** Customer A seeing Customer B's data via IDOR (manipulating order IDs, customer IDs in API requests). If the Customer Account API token grants access to admin-level functionality. If the token is accessible to cross-origin scripts (CORS misconfiguration allowing token theft). If tokens are predictable or forgeable.

### 16.16 Multi-Pass / Shared Customer Accounts

**What it is:** Multi-Pass allows merchants to share customer accounts between their own stores (e.g., a merchant with multiple brands using a shared customer database). Customers logged into the main website can be auto-redirected to the Shopify store without re-authentication.

**Why Shopify designed it this way:** Multi-Pass is a convenience feature for multi-store merchants who want a unified customer experience across their brand sites. It uses cryptographic tokens signed with the merchant's Multi-Pass secret to prevent forgery.

**Why it's NOT a vulnerability:** Shared customer accounts are by consent of the merchants involved — merchants choose to share customer databases between stores they own. The Multi-Pass token is cryptographically signed to prevent tampering. This is a documented feature with security controls.

**What WOULD be a vulnerability:** If the Multi-Pass secret could be guessed or brute-forced, allowing token forgery. If Multi-Pass tokens could be replayed across different sessions without invalidation. If an attacker could create a Multi-Pass token that grants access to a store the merchant does not own. If the main website does not require email verification, an attacker could create an account with the victim's email and use Multi-Pass to gain authenticated access to the victim's order data (known attack chain).

### 16.17 Order Printer / Stocky False Positives

**What it is:** Order Printer and Stocky are Shopify-owned separate applications. Order Printer renders order templates using Liquid. Stocky is an inventory management app.

**Why Shopify designed it this way:** These are tools for merchants — Order Printer for customizable invoices/packing slips, Stocky for inventory management. They have their own infrastructure and security boundaries separate from the core Shopify platform.

**Why it's NOT a vulnerability:** Most findings in these applications are feature behavior, not security issues. Order Printer templates intentionally have access to order data via Liquid for customization. Stocky operates independently with its own authentication. Both are explicitly listed as ineligible or out of scope by Shopify.

**What WOULD be a vulnerability:** If Order Printer Liquid templates can access data beyond the merchant's own orders (cross-tenant access). If an attacker can inject malicious Liquid code into another merchant's Order Printer template without admin access. If Stocky allows unauthorized inventory access across store boundaries.

### 16.18 Staff Permissions Nuances

**What it is:** Shopify uses Role-Based Access Control (RBAC) with granular permissions for staff members. Different roles have different levels of access to orders, products, customers, analytics, and settings.

**Why Shopify designed it this way:** Shopify's permission model is intentionally broad in some areas because staff members need data access to perform their job functions. A staff member with "Orders" permission needs to see customer names, emails, and phone numbers on orders for fulfillment and customer service. The permission system is designed around role requirements rather than strict least-privilege.

**Why it's NOT a vulnerability:** A staff member accessing data necessary for their role is intended behavior. "Orders" staff seeing customer names on orders is necessary for fulfillment. "Products" staff seeing inventory levels is necessary for product management. "Analytics" staff seeing revenue data is the entire point of the analytics role. Permission boundaries only become vulnerabilities when data access EXCEEDS what the role requires.

**What WOULD be a vulnerability:** A staff member accessing resources they explicitly DON'T have permission for — e.g., "Products" staff accessing the customer payment data export, or "Marketing" staff modifying product prices. Bypassing permission scopes via direct API calls. Accessing admin sections that aren't listed in the staff member's permissions. A staff member with "Manage Orders" permission accessing customer PII that goes beyond what's needed for order fulfillment.

---

## 17. DECISION TREE: IS IT A VULNERABILITY?

```
Is it a vulnerability?
├── Is it by design?
│   ├── Yes → NOT A VULNERABILITY (Section 16)
│   │   ├── Admin JSON endpoints? → Section 16.1
│   │   ├── CDN public files? → Section 16.2
│   │   ├── GraphQL introspection? → Section 16.3
│   │   ├── Opening Soon password bypass? → Section 16.4
│   │   ├── POS PIN (4-digit)? → Section 16.5
│   │   ├── HTML in rich text editor? → Section 16.6
│   │   ├── MCP data exposure? → Section 16.7
│   │   ├── Sidekick AI data access? → Section 16.8
│   │   ├── Storefront API public access? → Section 16.9
│   │   ├── Rate limiting issues? → Section 16.10
│   │   ├── Email verification not required? → Section 16.11
│   │   ├── CORS on public endpoints? → Section 16.12
│   │   ├── Web Pixel capabilities? → Section 16.13
│   │   ├── Checkout Kit WebView? → Section 16.14
│   │   ├── Customer Account API? → Section 16.15
│   │   ├── Multi-Pass accounts? → Section 16.16
│   │   ├── Order Printer/Stocky? → Section 16.17
│   │   └── Staff permissions? → Section 16.18
│   │
│   └── No → Is it ineligible?
│       ├── Yes → READ Sections 2-3 before reporting
│       │   ├── Self-XSS? → Section 3.1
│       │   ├── CSRF on cart? → Section 3.2
│       │   ├── Theoretical without impact? → Section 2.2
│       │   ├── Missing best practice? → Section 2.3
│       │   ├── Plan limit race condition? → Section 3.11
│       │   ├── CDN issues? → Section 3.3
│       │   └── Third-party app? → Section 3.6
│       │
│       └── No → Can you chain it?
│           ├── Yes (realistic chain) → REPORT
│           │   ├── Open redirect + OAuth → Chain 1 (Section 13)
│           │   ├── CSRF + session fixation → Chain 2 (Section 13)
│           │   ├── SSRF + cloud metadata → Chain 3 (Section 13)
│           │   ├── Rate limit bypass + brute-force → Chain 4 (Section 13)
│           │   ├── Introspection + IDOR → Chain 5 (Section 13)
│           │   └── Email verification + cross-system trust → Chain 6 (Section 13)
│           │
│           ├── Yes (theoretical chain) → Likely not reportable
│           │   ├── Requires third-party app vulnerability? → Different scope
│           │   ├── Requires browser zero-day? → Not accepted
│           │   ├── Requires physical access? → Out of scope
│           │   └── Requires social engineering? → Prohibited
│           │
│           └── No → Likely not a vulnerability
│               ├── Is the standalone impact sufficient?
│               │   ├── Yes → Report as-is
│               │   └── No → Abandon or hold for future chaining
│               └── Does it require demonstrated impact?
│                   ├── Yes → Report with full PoC
│                   └── No → Not reportable
```

### 16.19 Hydrogen / Oxygen Health Endpoints

**What it is:** Hydrogen/Oxygen stores have `/healthz`, `/health`, `/readyz` endpoints that respond with 200 OK or status information.

**Why Shopify designed it this way:** These are standard health check endpoints required by Oxygen hosting infrastructure for load balancer monitoring, orchestrator health checks, and deployment verification.

**Why it's NOT a vulnerability:** Health endpoints are standard infrastructure for any production web application. They are required for load balancer and orchestrator monitoring. After CVE-2024-45720 was patched, these endpoints no longer expose sensitive data.

**What WOULD be a vulnerability:** If health endpoints leaked sensitive data (environment variables, internal IPs, database connection strings). CVE-2024-45718, CVE-2024-45719, and CVE-2024-45720 were valid findings for health endpoint data leakage — but they have been patched.

### 16.20 Storefront API Tokens Visible in Theme JavaScript

**What it is:** Public Storefront API access tokens are embedded in theme JavaScript files (`theme.js`, `theme.liquid`) and Hydrogen client components. They appear as string constants like `const storefrontToken = 'abc123def456';`.

**Why Shopify designed it this way:** Public Storefront API tokens are designed to be client-visible. They are scope-limited to unauthenticated storefront operations (products, collections, cart, search). They cannot access admin functionality or sensitive customer data without additional authentication.

**Why it's NOT a vulnerability:** These are intentionally public tokens with limited scopes. They are documented as intentionally exposed. The vulnerability would be if an ADMIN token (with write_products, write_customers scopes) were exposed in client-side code. Public tokens only grant access to data that is already publicly available on the storefront.

**What WOULD be a vulnerability:** If the exposed token has ADMIN-level scopes (write_products, write_customers, write_orders). If the token is a private app token with full admin access. If the token could be used to access other merchants' data (cross-tenant).

### 16.21 Cart AJAX Endpoints Are Public

**What it is:** Cart AJAX endpoints (`/cart/add.js`, `/cart/update.js`, `/cart/change.js`, `/cart/clear.js`) are publicly accessible without authentication and have `Access-Control-Allow-Origin: *` CORS headers.

**Why Shopify designed it this way:** Cart operations must be public by necessity — any visitor to a store needs to be able to add items to their cart without logging in. The cart is an unauthenticated, session-based resource. CORS is open because headless storefronts may be hosted on any domain.

**Why it's NOT a vulnerability:** Adding items to a cart, changing quantities, or clearing a cart are all intentional shopper actions. No authentication is required, so CSRF protection is irrelevant — you cannot CSRF an unauthenticated action. The cart contains only public data (product IDs, quantities) and does not expose customer PII.

**What WOULD be a vulnerability:** If an attacker could access another user's active cart via cart ID enumeration (some platforms have suffered this). If the cart AJAX endpoints could be used to perform authenticated actions (checkout, payment). If cart data could be manipulated to cause financial loss (price manipulation via cart).

### 16.22 Customer Account API Token in localStorage

**What it is:** Customer Account API tokens (JWTs) are stored in the browser's localStorage for authenticated Customer Account API requests.

**Why Shopify designed it this way:** localStorage is the standard storage mechanism for client-side tokens in headless commerce and modern web applications. The token MUST be accessible to JavaScript for authenticated API requests — this is the OAuth bearer token pattern used across the industry.

**Why it's NOT a vulnerability:** Cross-origin isolation (via CORS, SameSite cookies, and origin-based security) prevents other scripts from accessing the token. The token is scoped to the customer's own resources only — it cannot access admin functionality or other customers' data. This pattern is used by thousands of applications including Auth0, Firebase, and AWS Cognito.

**What WOULD be a vulnerability:** If the token is accessible to cross-origin scripts (CORS misconfiguration allowing token theft from a malicious origin). If the token could be accessed by scripts injected via XSS on the storefront. If tokens are predictable or have excessive scope.

### 16.23 App Bridge Session Tokens in Browser Memory

**What it is:** Session tokens (JWTs) used by embedded Shopify apps are accessible in browser memory via developer tools. App Bridge fetches these tokens for frontend-to-backend authentication.

**Why Shopify designed it this way:** Session tokens MUST be accessible to the embedded app for authentication — the app needs to prove its identity to its own backend. Tokens have a 1-minute TTL, are encrypted in transit, and are never stored persistently.

**Why it's NOT a vulnerability:** Finding tokens in browser memory is expected — they are loaded into memory for use. The short TTL (1 minute) limits exposure window. Server-side validation (HMAC signature, claims verification, jti uniqueness) prevents token forgery and replay. The vulnerability would be persistence (tokens stored in cookies or localStorage) or excessive TTL, not in-memory presence.

**What WOULD be a vulnerability:** If session tokens could be extracted and reused after the user logs out (no server-side invalidation). If tokens had excessive TTL (hours or days). If the token's JWT signature could be forged (weak secret, algorithm confusion). If offline tokens were exposed to the browser.

### 16.24 Legacy REST API Still Works

**What it is:** Deprecated REST Admin API endpoints (from 2024-01 and earlier versions) continue to respond to requests in 2026. The REST API was designated legacy in October 2024.

**Why Shopify designed it this way:** Shopify maintains backward compatibility for API versions to give merchants and apps time to migrate to GraphQL. Old API versions continuing to work is intentional — breaking existing integrations would cause significant merchant disruption.

**Why it's NOT a vulnerability:** Legacy API availability does not cross any security boundary — authentication and authorization checks are the same regardless of API version. The vulnerability would be if a legacy endpoint bypasses authorization checks that newer versions enforce. Working as designed.

**What WOULD be a vulnerability:** If a legacy REST endpoint accepts authentication tokens that newer versions reject, allowing token reuse after revocation. If a legacy endpoint returns MORE data than the GraphQL equivalent (information disclosure). If a legacy endpoint bypasses permission checks added in newer versions.

### 16.25 Different API Versions Have Different Behavior

**What it is:** Each API version (2024-01, 2024-07, 2025-01, 2025-07, 2026-01, 2026-07) may have different field availability, mutation signatures, validation rules, and default behaviors.

**Why Shopify designed it this way:** API versioning allows Shopify to evolve the API without breaking existing apps. Each version is maintained separately for backward compatibility during its support window (approximately 12 months).

**Why it's NOT a vulnerability:** Differences in behavior between API versions are expected and intentional. Old fields being available in older versions is backward compatibility. New validation in newer versions is security improvement. The version-specific contract is documented for each release.

**What WOULD be a vulnerability:** If an older API version bypasses authorization checks that newer versions enforce (authorization regression). If data returned by an older version includes fields that were later made private (data leakage through version downgrade).

### 16.26 Private App Tokens in Your Own Source Code

**What it is:** A merchant can find their own private app tokens in their own store's code, configuration files, or environment variables.

**Why Shopify designed it this way:** Private app tokens are generated for the merchant's own use. They are analogous to passwords — if the merchant leaks their own token, it affects only their own store.

**Why it's NOT a vulnerability:** You control your own private app tokens. If you leak them, it affects only your store. This is a personal security practice issue, not a Shopify platform vulnerability.

**What WOULD be a vulnerability:** If you find OTHER merchants' private tokens in public GitHub repositories, Pastebin, or other data sources — report these via HackerOne as credential leakage.

### 16.27 Sitemap XML Contains Product URLs

**What it is:** `/sitemap_products.xml` contains a listing of all product URLs for the store, including product handles and IDs.

**Why Shopify designed it this way:** Sitemaps are an SEO best practice — they list all URLs for search engine crawling and indexing. They help Google, Bing, and other search engines discover and rank store content.

**Why it's NOT a vulnerability:** Sitemaps are designed to make all store URLs discoverable. Product URLs are intentionally public — they are the storefront pages customers visit. The information in sitemaps is already available through the storefront navigation, search, and product listings.

**What WOULD be a vulnerability:** If the sitemap exposed hidden or draft products that are not intended to be public. If the sitemap exposed admin URLs or sensitive endpoints.

### 16.28 Script Tags on Storefront

**What it is:** Script Tags (legacy feature) allow apps to inject JavaScript into all storefront pages. They exist on the storefront to add functionality.

**Why Shopify designed it this way:** Script Tags are an intended feature for app developers to add functionality to storefronts — analytics scripts, live chat widgets, popup notifications, and other third-party integrations.

**Why it's NOT a vulnerability:** Creating Script Tags requires admin access with valid OAuth tokens. They are not a vector for attackers unless the attacker already has admin access. This is a documented API feature.

**What WOULD be a vulnerability:** If an attacker can create a Script Tag WITHOUT admin access or OAuth tokens. If Script Tags can be created cross-tenant (app A injecting scripts into merchant B's store without authorization).

### 16.29 App Proxy Has Storefront Context Access

**What it is:** App Proxy endpoints inherit the storefront's Liquid context, allowing them to access store data, customer info, and metafields when rendering proxied content.

**Why Shopify designed it this way:** App Proxies need store context to serve personalized or store-specific content. This is how they provide dynamic functionality on storefront URLs.

**Why it's NOT a vulnerability:** App Proxies require valid HMAC signatures in requests for authentication. They are configured by the app developer and approved during App Store review. The Liquid context access is intentional for rendering store-specific content.

**What WOULD be a vulnerability:** If an App Proxy endpoint returns data accessible without proper HMAC verification. If the App Proxy can be used to access other stores' data (cross-tenant via signature manipulation). If user-controlled input is rendered as Liquid code (SSTI).

### 16.30 Product/Collection JSON Endpoints Are Public

**What it is:** `/products.json`, `/collections.json`, `/pages.json`, `/products/{handle}.js` are publicly accessible without authentication and return JSON-formatted store data.

**Why Shopify designed it this way:** These endpoints are essential for headless commerce and theme development. They allow custom storefronts and third-party tools to access public catalog data in machine-readable format.

**Why it's NOT a vulnerability:** These are publicly documented endpoints that return JSON versions of storefront data. The data they expose (product titles, prices, descriptions, images) is already visible on the storefront HTML pages.

**What WOULD be a vulnerability:** If these endpoints returned data that is NOT visible on the storefront (hidden products, draft content, customer data). If they returned admin-only fields (cost price, supplier info).

### 16.31 Monorail Telemetry Endpoint

**What it is:** `monorail-edge.shopifysvc.com` accepts telemetry data from Shopify properties for internal event tracking and analytics.

**Why Shopify designed it this way:** Monorail is Shopify's internal event telemetry system for monitoring platform health, usage patterns, and performance metrics.

**Why it's NOT a vulnerability:** The endpoint is designed to accept data — this is its purpose. Sending data to it is not a vulnerability; it's expected behavior. The data sent is telemetry, not sensitive user data.

**What WOULD be a vulnerability:** If the telemetry endpoint leaked data to unauthorized parties. If it could be used to inject malicious data into Shopify's monitoring systems.

### 16.32 Well-Known Discovery Files

**What it is:** Files like `/.well-known/security.txt`, `/.well-known/ucp`, `/.well-known/customer-account-api`, `/llms.txt`, `/agents.md` are publicly accessible on Shopify domains.

**Why Shopify designed it this way:** These files are intentionally placed for discovery purposes. `security.txt` is a security best practice (RFC 9116) that tells researchers how to report vulnerabilities. UCP discovery and Customer Account API discovery files help AI agents and developers find the correct endpoints. `llms.txt` and `agents.md` are standard files for LLM/agent discovery.

**Why it's NOT a vulnerability:** These files are intentionally public — they are designed to be discovered. `security.txt` helps researchers find the bug bounty program. API discovery files help developers integrate correctly.

**What WOULD be a vulnerability:** If these files exposed sensitive internal URLs, credentials, or configuration details.

### 16.33 Response Headers Leak Infrastructure Details

**What it is:** HTTP response headers include `Server`, `X-Frame-Options`, `CF-Ray`, `X-Powered-By: Shopify`, and Shopify-specific headers. The Shopify Debug Tool exposes edge server instance ID, hostname, IP, timestamp, and TLS version.

**Why Shopify designed it this way:** HTTP headers are a standard part of the HTTP protocol. Some are required for functionality (CORS, caching), others provide debugging information. The Debug Tool is intentionally public for troubleshooting.

**Why it's NOT a vulnerability:** Server version strings and framework fingerprints are not sensitive — they do not expose exploitable information without a corresponding vulnerability in that version. The Debug Tool is an intentionally public endpoint. These headers do not expose PII, credentials, or session data.

**What WOULD be a vulnerability:** If response headers exposed session tokens, API keys, or internal IP addresses that could be used for targeted attacks.

### 16.34 Shopify Functions Sandbox

**What it is:** Shopify Functions run in a WebAssembly (Wasm) sandbox with strict resource limits: 256 kB compiled binary, 10 MB linear memory, 512 kB stack, 11M execution instructions, no direct filesystem or network access (unless fetch target is explicitly enabled).

**Why Shopify designed it this way:** The Wasm sandbox is a security boundary designed to isolate function execution from Shopify's infrastructure. Functions run inside Shopify's systems, not on the app developer's server, so isolation is critical for platform security. Resource limits prevent abuse and ensure fair resource allocation.

**Why it's NOT a vulnerability:** The sandbox and limits are intentional security controls. Non-determinism is prohibited to ensure consistent discount/pricing calculations. Network access requires explicit approval for enterprise use cases. Input queries are reviewed during App Store approval. These are all by-design security measures.

**What WOULD be a vulnerability:** If a Function could escape the Wasm sandbox to access the host system (sandbox escape). If a Function could access data beyond its declared input query scope. If a Function could make unauthorized network requests via the fetch target. If the sandbox could be used to execute arbitrary system commands.

### 16.35 Web Pixel Sandbox

**What it is:** App Web Pixels run in a strict sandbox (Web Worker) with no DOM access, no window/document access, no UI rendering capability. Custom Pixels use a lax sandbox (iframe with allow-scripts).

**Why Shopify designed it this way:** The sandbox prevents malicious Web Pixels from scraping checkout fields, PII entry, or credit card numbers (Magecart-style attacks). App Pixels are sandboxed because they are distributed through the App Store and could be created by third-party developers. Custom Pixels are created by the merchant for their own store, so the lax sandbox provides more flexibility.

**Why it's NOT a vulnerability:** The sandbox IS the security feature — it intentionally restricts what Pixels can access. No DOM access prevents checkout data theft. fetch() calls require CORS, preventing silent data exfiltration. No UI rendering prevents phishing. Events are explicitly published by Shopify, not scraped.

**What WOULD be a vulnerability:** If the sandbox could be escaped to access the DOM or parent frame (sandbox escape allowing Magecart-style checkout skimming). If a Pixel could access data beyond its declared scopes in `shopify.extension.toml`. If the sandbox allowed network requests to arbitrary endpoints without CORS restrictions.

### 16.36 Checkout CSP Is Strict by Design

**What it is:** Shopify checkout pages have a strict Content Security Policy (CSP) that blocks `unsafe-inline` and `unsafe-eval`, sandboxes third-party scripts, and restricts what resources can be loaded.

**Why Shopify designed it this way:** Checkout pages process sensitive payment data and customer PII. The strict CSP is part of Shopify's PCI DSS compliance — it prevents Magecart-style attacks where malicious scripts inject skimming code into checkout pages.

**Why it's NOT a vulnerability:** The CSP is intentionally restrictive. Finding that `unsafe-inline` is not allowed or that third-party scripts are sandboxed is expected — this is the security control working as designed. Checkout extensions run in sandboxed iframes specifically to prevent data theft.

**What WOULD be a vulnerability:** If the checkout CSP could be bypassed or disabled. If a script could inject content into the checkout page despite the CSP (CSP bypass via JSONP, CDN trust, or policy misconfiguration).

### 16.37 Customer Privacy API Is Public

**What it is:** `window.Shopify.customerPrivacy` is accessible from any JavaScript running on the storefront, exposing methods like `setTrackingConsent()`, `currentVisitorConsent()`, `analyticsProcessingAllowed()`, and `marketingAllowed()`.

**Why Shopify designed it this way:** The Customer Privacy API is intentionally public for apps and themes to check and manage visitor consent status for GDPR, CCPA, and other privacy regulations. It needs to be accessible to all scripts running on the storefront.

**Why it's NOT a vulnerability:** The API does not expose sensitive data — it only provides consent state (analyticsAllowed, marketingAllowed). Making it public is necessary for privacy compliance — third-party scripts need to know whether they have consent to process data. This is standard practice across the web.

**What WOULD be a vulnerability:** If the API exposed PII or customer data. If manipulating the consent state bypassed privacy controls. If the API could be used to disable privacy protections for other scripts.

### 16.38 POS Extensions Can See Transaction Data

**What it is:** POS UI Extensions can subscribe to events like `pos.transaction.created` and `pos.cash.tracking.updated` which contain transaction details, amounts, and cash handling data.

**Why Shopify designed it this way:** POS app developers need transaction data to build payment reconciliation, cash management, and reporting features. The event subscription model provides controlled access to necessary data.

**Why it's NOT a vulnerability:** The data access is intentional for POS app functionality. Extensions run in a sandboxed environment. The merchant chooses which extensions to install. Cash tracking events expose cash handling data, but only to the merchant's own installed extensions.

**What WOULD be a vulnerability:** If POS extensions could access data across different merchant installations (cross-tenant). If POS extensions could modify transaction data after creation. If an extension could access cash handling data without proper scope declaration.

### 16.39 Shopify Magic AI Features

**What it is:** Shopify Magic is a suite of inline AI features (product descriptions, blog posts, image editing, brand voice cloning) built directly into admin fields.

**Why Shopify designed it this way:** Magic is designed to help merchants generate content more efficiently using AI. It has no public API — it's embedded in the admin UI as a first-party feature, which significantly reduces attack surface.

**Why it's NOT a vulnerability:** Magic processes data within Shopify's trust boundary. No public API means no integration attack surface (admin session is the only vector). Brand Voice Cloning analyzes the merchant's own content — the merchant is already authorized to access that content.

**What WOULD be a vulnerability:** If Magic generated content exposed sensitive merchant data to unauthorized parties. If prompt injection via product titles could cause Magic to exfiltrate data. If Magic's AI processing bypassed admin permission boundaries.

### 16.40 Combined Listings / Bundles

**What it is:** Combined Listings group multiple products into a single product detail page. Child products have predictable URLs and share SEO data with the parent.

**Why Shopify designed it this way:** Combined Listings provide a better shopping experience for product variants with different prices, images, and descriptions. The relationship between products is intentionally visible for SEO and storefront navigation.

**Why it's NOT a vulnerability:** Child product URLs being predictable does not enable unauthorized access. The combined listing relationship is intentionally surfable. Products are independent objects with their own access controls.

**What WOULD be a vulnerability:** If the combined listing relationship could be manipulated to associate unrelated products with a merchant's store. If SEO data inheritance could be used for spam or SEO abuse. If a non-Plus merchant could create combined listings (feature restriction bypass).

---

## Quick Reference: By-Design vs. Vulnerability

| Finding | Status | Rationale |
|---------|--------|-----------|
| Admin `.json` endpoints accessible with staff auth | By Design | Staff need programmatic access |
| CDN files publicly accessible | By Design | Public assets for storefront |
| GraphQL introspection works | By Design | Developer experience requirement |
| Opening Soon password bypassable | By Design | Not a security boundary |
| POS PIN is only 4 digits | By Design | Retail convenience tradeoff |
| Rich text editor allows HTML/scripts | By Design | Merchant controls own content |
| MCP tools exposed without auth | By Design | Mirrors public Storefront API |
| Sidekick accesses merchant data | By Design | AI assistant needs data access |
| Storefront API tokenless access | By Design | Public e-commerce requirement |
| Rate limiting absent on endpoint | By Design | Operational control, not security |
| Email verification optional at signup | By Design | Friction reduction tradeoff |
| Public endpoints have permissive CORS | By Design | Headless commerce requirement |
| Web Pixels access customer events | By Design | Analytics/tracking requirement |
| Checkout Kit WebView | By Design | Mobile checkout surface |
| Customer Account API token in localStorage | By Design | Standard web auth pattern |
| Multi-Pass shared accounts | By Design | Multi-store merchant feature |
| Order Printer Liquid access | By Design | Invoice customization |
| Staff can see role-necessary data | By Design | RBAC design choice |
| Admin `.json` without auth | VULNERABILITY | Authentication bypass |
| Cross-tenant CDN file access | VULNERABILITY | Multi-tenant isolation failure |
| Introspection reveals sensitive data | VULNERABILITY | Schema contains secrets |
| Password page protects admin | VULNERABILITY | Security boundary bypass |
| POS PIN bypassed remotely | VULNERABILITY | Remote auth bypass |
| HTML injection across tenants | VULNERABILITY | Stored XSS beyond own store |
| MCP exposes API keys/PII | VULNERABILITY | Credential exposure |
| Sidekick cross-tenant data leak | VULNERABILITY | Multi-tenant isolation |
| Storefront API exposes admin data | VULNERABILITY | Authorization bypass |
| Successful brute-force via rate limit gap | VULNERABILITY | Demonstrated credential compromise |
| Unverified email accesses verified features | VULNERABILITY | Authorization bypass |
| Admin API has permissive CORS | VULNERABILITY | Credential theft via cross-origin |
| Web Pixel sandbox escape | VULNERABILITY | Checkout data theft (Magecart) |
| Checkout Kit token forgery | VULNERABILITY | Payment authorization bypass |
| Customer API cross-tenant IDOR | VULNERABILITY | Customer A sees Customer B's data |
| Multi-Pass token forgery | VULNERABILITY | Authentication bypass |
| Staff accesses data beyond role | VULNERABILITY | Authorization bypass |

### The Golden Test

Before reporting, ask yourself:

1. **Is the data being accessed something the platform INTENTIONALLY needs to be public?**
   - Product catalog? Yes → By design
   - Customer PII? No → Possibly a vulnerability
   - Admin settings? No → Possibly a vulnerability

2. **Is the user accessing this data AUTHORIZED to do so?**
   - Staff member with Orders permission viewing orders? Yes → By design
   - Unauthenticated visitor viewing admin pages? No → Vulnerability

3. **Is the mechanism itself the vulnerability, or is the vulnerability in how you USED it?**
   - GraphQL introspection exists? → Not a vulnerability (by design)
   - GraphQL introspection helped you find an IDOR? → The IDOR is the vulnerability

4. **If this were fixed, would the platform stop working as intended?**
   - CDN files become private → Storefronts break → By design
   - Staff can't see customer names on orders → Fulfillment breaks → By design
   - Rate limits enforced absolutely → Legitimate apps break → By design

### Complete Reference: All 40 By-Design Items

| # | Area | By-Design Status | Vulnerability Threshold |
|---|------|-----------------|----------------------|
| 1 | Admin Staff JSON Endpoints | Staff can access `.json` endpoints with auth | Unauthenticated access or cross-tenant leakage |
| 2 | CDN File Hosting | Files publicly accessible | Cross-tenant access or cache poisoning |
| 3 | GraphQL Introspection | Schema exposed by design | Secrets or PII in schema; IDOR via discovered mutations |
| 4 | Opening Soon Password | Bypassable cosmetic gate | Protects admin resources |
| 5 | POS PIN (4-Digit) | Convenience tradeoff | Remote bypass or programmatic bypass |
| 6 | HTML in Rich Text Editor | Merchant controls own content | Cross-tenant stored XSS |
| 7 | MCP Server Data Exposure | Tool discovery is by design | Credentials, API keys, or PII exposed |
| 8 | Sidekick AI | Accesses own merchant data | Cross-tenant leakage or unauthorized actions via prompt injection |
| 9 | Storefront API Public Access | Public by e-commerce design | Admin data access or unauthorized writes |
| 10 | Rate Limiting | Operational control, not security | Demonstrated successful brute-force |
| 11 | Email Verification at Signup | Optional for reduced friction | Unverified email accesses verified features |
| 12 | CORS on Public Endpoints | Required for headless commerce | Admin endpoints with permissive CORS |
| 13 | Web Pixel Capabilities | Analytics data access by design | Scope boundary bypass or sandbox escape |
| 14 | Checkout Kit WebView | Intended checkout surface | Cross-app data exfiltration or token forgery |
| 15 | Customer Account API | Customer sees own data | Cross-customer IDOR |
| 16 | Multi-Pass Accounts | Multi-store merchant feature | Token forgery or stolen |
| 17 | Order Printer / Stocky | Separate app functionality | Cross-tenant data access |
| 18 | Staff Permissions | RBAC with role-necessary access | Data access beyond role |
| 19 | Hydrogen Health Endpoints | Standard infrastructure | Data leakage via health checks |
| 20 | Storefront API Tokens in JS | Public scope-limited tokens | Admin tokens in client code |
| 21 | Cart AJAX Endpoints Public | Required for shopping | Authenticated action via cart |
| 22 | Customer Account Token in localStorage | Standard OAuth pattern | Cross-origin token theft |
| 23 | App Bridge Session Tokens | In-memory by design | Persistent storage or excess TTL |
| 24 | Legacy REST API | Backward compatibility | Authorization bypass via legacy version |
| 25 | Different API Versions | Intentional versioning | Version downgrade bypasses auth |
| 26 | Private App Tokens | Merchant's own credential | Other merchants' tokens found publicly |
| 27 | Sitemap Product URLs | SEO best practice | Hidden/draft products in sitemap |
| 28 | Script Tags on Storefront | Intended app feature | Unauthenticated script tag creation |
| 29 | App Proxy Context | Required for dynamic content | HMAC verification missing |
| 30 | Product JSON Endpoints | Public by design | Admin-only fields exposed |
| 31 | Monorail Telemetry | Event tracking by design | Data leakage via telemetry |
| 32 | Well-Known Files | RFC/standard practice | Sensitive URLs or credentials exposed |
| 33 | Response Headers | HTTP protocol standard | Session data or PII in headers |
| 34 | Functions Sandbox | Security isolation boundary | Sandbox escape or data beyond scope |
| 35 | Web Pixel Sandbox | Anti-Magecart protection | Sandbox escape or scope bypass |
| 36 | Checkout CSP Strict | PCI compliance requirement | CSP bypass allowing script injection |
| 37 | Customer Privacy API | Required for privacy compliance | PII exposure via privacy API |
| 38 | POS Transaction Events | Intended for app developers | Cross-tenant transaction data access |
| 39 | Shopify Magic AI Features | First-party admin feature | Data exfiltration via AI |
| 40 | Combined Listings | Product grouping feature | Cross-store product association |

### The Decision Matrix

```
                    ┌─────────────────────────────┐
                    │      FOUND SOMETHING?        │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │   Is the target in scope?    │
                    │  (See Section 9)             │
                    └──────┬──────────────┬───────┘
                           │              │
                        YES │              │ NO
                           │              │
              ┌────────────▼──┐           ▼
              │ Is it by       │     STOP - Wrong target
              │ design?        │
              └───┬────────┬──┘
                  │        │
               YES │        │ NO
                  │        │
          ┌───────▼──┐  ┌──▼──────────────┐
          │ NOT A    │  │ Is it explicitly │
          │ VULN     │  │ ineligible?      │
          │ (Sec 16) │  │ (Sections 2-3)   │
          └──────────┘  └──┬────────┬─────┘
                           │        │
                        YES │        │ NO
                           │        │
                    ┌──────▼──┐  ┌──▼──────────────┐
                    │ READ    │  │ Can you chain it │
                    │ Sec 2-3 │  │ realistically?   │
                    └─────────┘  └──┬────────┬─────┘
                                    │        │
                                 YES │        │ NO
                                    │        │
                              ┌─────▼──┐  ┌──▼──────────┐
                              │ REPORT │  │ Is standalone│
                              │ full   │  │ impact       │
                              │ chain  │  │ sufficient?  │
                              └────────┘  └──┬──────┬────┘
                                             │      │
                                          YES │      │ NO
                                             │      │
                                      ┌──────▼┐  ┌─▼────────┐
                                      │REPORT │  │ Abandon or│
                                      │as-is  │  │ hold for  │
                                      └───────┘  │ future    │
                                                 │ chaining  │
                                                 └───────────┘
```

### Three-Step Verification Protocol

Before writing any report, run through this protocol:

**Step 1: The Documentation Test**
- Search Shopify docs for this feature/endpoint/behavior
- If it's documented as intentional → By design (Section 16)
- If it contradicts documented behavior → Possibly a vulnerability
- If undocumented → Investigate further

**Step 2: The Authorization Test**
- Who is accessing what?
- Is the accessor authorized to see this data?
- Is the data within their role scope?
- If the answer to all three is YES → By design
- If any answer is NO → Possibly a vulnerability

**Step 3: The Impact Test**
- What can an attacker actually DO with this?
- Can they steal data? Modify data? Access other tenants?
- Does the impact require other vulnerabilities to work?
- If impact requires other vulns AND you can't demonstrate the chain → Not reportable
- If impact requires other vulns AND you CAN demonstrate the chain → Report the full chain

### Common Mistakes to Avoid

1. **Confusing "in scope for testing" with "not by design"** — Just because you're allowed to test against `*.shopify.com` doesn't mean everything you find is a vulnerability. Many features on in-scope domains are intentionally designed to work the way they work.

2. **Confusing "interesting" with "vulnerable"** — Finding that the Storefront API has no rate limits is interesting. Demonstrating that you can brute-force a customer's password via that gap is a vulnerability. The absence of a control is not a vulnerability — the successful exploitation is.

3. **Confusing "by design" with "outdated design"** — Some by-design behaviors might seem like bad design from a security perspective (4-digit POS PIN, optional email verification). But bad design ≠ vulnerability when the design is intentional and documented.

4. **Confusing "tenancy" with "privacy"** — A merchant's own store data is theirs to control. Cross-tenant access (merchant A accessing merchant B's data) is the vulnerability boundary. Within-tenant access (a merchant accessing their own data through different means) is usually by design.

5. **Confusing "I can see it" with "it's exposed"** — Being able to view your own API tokens, your own store settings, or your own customer data is expected. The vulnerability is OTHER PEOPLE seeing YOUR data, not YOU seeing YOUR data. Use two test stores to demonstrate cross-tenant issues.

6. **Confusing "information disclosure" with "public information"** — Product titles, prices, and descriptions are public information by design. Finding them in a JSON response is not information disclosure. The vulnerability is finding data that is NOT publicly available (internal notes, cost prices, hidden products) in unexpected responses.

7. **Confusing "missing control" with "missing boundary"** — No rate limiting on an API is a missing operational control. It becomes a vulnerability only when an attacker can use that absence to cross a security boundary (access data they shouldn't, perform unauthorized actions). Operational controls and security boundaries are different concepts.

8. **Confusing "store content" with "platform content"** — A merchant's product titles, blog posts, and theme files are the merchant's own content. Merchants control what goes into their store. Platform-level vulnerabilities involve Shopify's OWN content or infrastructure being compromised, not merchants making poor decisions about their own content.

9. **Confusing "self-harm" with "cross-tenant attack"** — A merchant uploading an HTML file with JavaScript to their own CDN is self-harm at worst (they're damaging their own store). Cross-tenant attacks (merchant A affecting merchant B's store) are the real vulnerabilities. Most "stored XSS" in Shopify is self-XSS because the injector and the affected store are the same entity.

10. **Confusing "feature works as intended" with "feature has security implications"** — Many features (B2B pricing, Multi-Pass, Web Pixels, App Proxy) intentionally access data that seems "sensitive." The access is the feature — it's what the feature was designed to do. Security implications arise when the access EXCEEDS the feature's declared scope, not when the feature simply works.

### Chain Analysis Framework

When evaluating whether a chain is realistic, use this framework:

**Prerequisite Analysis:**
- What must the attacker already have? (Access level, permissions, tokens)
- Is this prerequisite realistic for an external attacker?
- If the prerequisite = "already has admin access" → The chain starts too late

**Link Strength Analysis:**
- Is each link in the chain a verifiable weakness?
- Can each link be demonstrated independently?
- Are any links theoretical or assumed?

**Impact Trajectory:**
- Does the chain escalate from low to high privilege?
- Does each link build on the previous?
- Is the final impact proportional to the chain's complexity?

**Realism Score:**
- Chain requires single victim action (click a link) → Realistic
- Chain requires multiple victim actions → Less realistic
- Chain requires victim to bypass browser warnings → Not realistic
- Chain requires physical access → Out of scope
- Chain requires social engineering → Prohibited

### Hunting Strategy for By-Design Features

Understanding what's by design helps you hunt more effectively:

1. **Use by-design features as reconnaissance tools** — GraphQL introspection is by design, but USE it to find undocumented mutations or authorization gaps. CDN files are public, but CHECK if merchants can access OTHER merchants' CDN files. Public API endpoints are by design, but TEST if they return admin-level data.

2. **Focus on the boundaries, not the features** — The boundary between what's by design and what's a vulnerability is where real findings live. Cross-tenant data access is always reportable. Authorization bypass is always reportable. Sandbox escape is always reportable.

3. **Test for scope escalation** — A Web Pixel accessing customer email is by design. A Web Pixel accessing data it DIDN'T declare in its scopes is a vulnerability. A Function accessing order data is by design. A Function accessing data beyond its input query scope is a vulnerability.

4. **Two-account testing** — The single most effective technique for Shopify bug bounty is to create TWO test stores and demonstrate data access between them. Cross-tenant IDOR is consistently the highest-paying vulnerability class.

5. **Chain construction** — Don't report single low-severity issues. Find two or three issues that chain together: authentication gap + permission bypass + data access = critical chain worth $5,000-$50,000.

### Final Reminder

> **If a feature works exactly as documented, behaves exactly as designed, and only accesses data that the accessing user is authorized to see — it is NOT a vulnerability, even if it feels like it should be.**

The line between "by design" and "vulnerability" is clear:
- **By design:** The feature does what it was designed to do
- **Vulnerability:** The feature does something it was NOT designed to do

This guide has identified 40 specific by-design areas. If your finding falls into any of these, it's almost certainly not a vulnerability. Use the decision tree, the verification protocol, and the quick-reference table to confirm. If you're still unsure, ask yourself the Golden Test: "If this were fixed, would the platform break?" If the answer is yes, it's by design.

### Case Study: How to Use This Section

**Scenario:** You discover that `POST /admin/api/2026-07/products.json` returns product data when accessed by a staff member with "Products" permission.

**Your process:**
1. Check Section 16 → See 16.1 (Admin Staff JSON Endpoints) — staff access to JSON endpoints is by design
2. Check the vulnerability threshold → Would be a vuln if unauthenticated or cross-tenant
3. Verify: Is this staff member authorized? Yes (Products permission) → By design
4. Result: NOT a vulnerability

**Scenario:** You discover that `POST /admin/api/2026-07/products.json` returns products from OTHER stores when accessed by your staff member.

**Your process:**
1. Check Section 16 → See 16.1 — cross-tenant access is the vulnerability threshold
2. Verify: Is this cross-tenant? Yes (Store A sees Store B's products) → VULNERABILITY
3. Use two-account differential to prove it
4. Result: REPORT — this is an IDOR vulnerability

**Scenario:** You discover that the Storefront API `customerAccessTokenCreate` mutation has no rate limiting.

**Your process:**
1. Check Section 16 → See 16.10 (Rate Limiting Is Not a Vulnerability)
2. Check the vulnerability threshold → Would be a vuln if demonstrated successful brute-force
3. Verify: Can you actually brute-force a password? If yes → Report with PoC. If no → Not reportable
4. Result: NOT a vulnerability unless you demonstrate credential compromise

**Scenario:** You discover that Web Pixels can access customer email addresses.

**Your process:**
1. Check Section 16 → See 16.13 (Web Pixel API Capabilities) and 16.35 (Web Pixel Sandbox)
2. Check the vulnerability threshold → Would be a vuln if scope boundary bypassed or sandbox escaped
3. Verify: Did the Pixel declare `read_customer_email` scope? If yes → By design. If no → Scope boundary bypass
4. Result: By design if scoped properly; VULNERABILITY if scope is bypassed

**Scenario:** You discover that Sidekick can answer questions about your store's orders.

**Your process:**
1. Check Section 16 → See 16.8 (Sidekick AI) — Sidekick accessing own merchant data is by design
2. Check the vulnerability threshold → Would be a vuln if cross-tenant or unauthorized actions via prompt injection
3. Verify: Are you the authenticated merchant? Is Sidekick accessing YOUR data? → By design
4. Result: NOT a vulnerability

**Scenario:** You discover that B2B company location IDs are sequential integers.

**Your process:**
1. Check Section 16 → See 5.34.5 (Company Location IDs Are Sequential)
2. Vulnerability threshold → Would be a vuln if SERVER-SIDE validation is missing, not that IDs are sequential
3. Verify: Can you access Company B's data using Company A's token by changing the location ID? If yes → IDOR. If no → By design
4. Result: NOT a vulnerability (sequential IDs are not a vulnerability — missing authorization checks are)

### When in Doubt: The Flowchart

```
START: Did you find something?
│
├── Is it on an in-scope domain?
│   └── Section 9
│
├── Is the finding in the "By Design" list (Section 16)?
│   ├── YES → Is it CROSSING the vulnerability threshold?
│   │   ├── YES → VULNERABILITY (report it)
│   │   └── NO → By design (do not report)
│   └── NO → Continue...
│
├── Is the finding in the "Ineligible" list (Sections 2-3)?
│   ├── YES → Do not report
│   └── NO → Continue...
│
├── Can you demonstrate realistic impact?
│   ├── YES → Continue...
│   └── NO → Do not report
│
├── Is the finding against YOUR OWN test store?
│   ├── YES → Continue...
│   └── NO → Stop — test against your own stores
│
├── Can you reproduce it consistently?
│   ├── YES → Continue...
│   └── NO → Do not report
│
├── Is it a single issue or a chain?
│   ├── Chain → Report the FULL chain with all links
│   └── Single → Report as-is
│
└── SUBMIT TO HACKERONE
```

### The Two-Store Rule

The single most important rule for Shopify bug bounty:

**If you cannot demonstrate it using TWO stores you control, it is unlikely to be a valid vulnerability.**

- Cross-tenant IDOR? Create Store A and Store B, show Store A accessing Store B's data
- Permission bypass? Create a staff account with limited permissions on YOUR store, show it accessing data beyond those permissions
- Authentication bypass? Show that an unauthenticated request to YOUR store returns data that requires authentication
- Rate limit bypass? Show that you can successfully brute-force credentials on YOUR store's login endpoint

The two-store rule eliminates false positives from:
- Confusing "I can see my own data" with "I can see anyone's data"
- Confusing "feature works as intended" with "feature has security implications"
- Confusing "public information" with "information disclosure"

Every time you find something, ask: "Can I demonstrate this between two stores I control?" If the answer is no, you likely have a by-design feature or a self-referential finding, not a vulnerability.

1. **Is the data being accessed something the platform INTENTIONALLY needs to be public?**
   - Product catalog? Yes → By design
   - Customer PII? No → Possibly a vulnerability
   - Admin settings? No → Possibly a vulnerability

2. **Is the user accessing this data AUTHORIZED to do so?**
   - Staff member with Orders permission viewing orders? Yes → By design
   - Unauthenticated visitor viewing admin pages? No → Vulnerability

3. **Is the mechanism itself the vulnerability, or is the vulnerability in how you USED it?**
   - GraphQL introspection exists? → Not a vulnerability (by design)
   - GraphQL introspection helped you find an IDOR? → The IDOR is the vulnerability

4. **If this were fixed, would the platform stop working as intended?**
   - CDN files become private → Storefronts break → By design
   - Staff can't see customer names on orders → Fulfillment breaks → By design
   - Rate limits enforced absolutely → Legitimate apps break → By design

---

## APPENDIX E: QUICK DECISION GUIDE — EXPANDED EDITION

### 30+ Additional Decision Points

```
ADDITIONAL DECISION POINTS (Continue from Section 10 main guide):

├── Did you find something related to MCP / Agentic Commerce?
│   ├── Is it that Storefront MCP tools require no auth?
│   │   └── DON'T REPORT (public by design, mirrors Storefront API)
│   ├── Is it that Customer Accounts MCP requires a token?
│   │   └── DON'T REPORT (expected auth mechanism)
│   ├── Is it that Dev MCP runs locally without network auth?
│   │   └── DON'T REPORT (local dev tool by design)
│   └── Does the MCP tool allow access to ADMIN data without auth?
│       └── REPORT (MCP authorization gap)
│
├── Did you find something related to Sidekick AI?
│   ├── Is it that Sidekick respects admin permissions?
│   │   └── DON'T REPORT (security feature)
│   ├── Is it that Sidekick App Extensions require review?
│   │   └── DON'T REPORT (security control)
│   ├── Is it theoretical prompt injection without demonstrated impact?
│   │   └── DON'T REPORT (theoretical)
│   ├── Does Sidekick perform unauthorized actions via prompt injection?
│   │   └── REPORT (demonstrated AI manipulation)
│   └── Is it that Sidekick has no public API?
│       └── DON'T REPORT (reduced attack surface by design)
│
├── Did you find something related to Hydrogen / Headless?
│   ├── Is it a health check endpoint on Oxygen?
│   │   └── DON'T REPORT (standard infrastructure)
│   ├── Is it Storefront API tokens in Hydrogen JS?
│   │   └── DON'T REPORT (public tokens, intentional)
│   ├── Is it cart AJAX working from any origin?
│   │   └── DON'T REPORT (CORS intentionally open for headless)
│   ├── Is it Customer Account API tokens in localStorage?
│   │   └── DON'T REPORT (standard storage mechanism)
│   └── Does a Hydrogen store leak admin tokens in client code?
│       └── REPORT (admin token in client = real leakage)
│
├── Did you find something related to B2B features?
│   ├── Does B2B pricing offer lower prices than consumer?
│   │   └── DON'T REPORT (intentional volume pricing)
│   ├── Is it that client-side quantity rules can be bypassed via API?
│   │   └── DON'T REPORT (server-side enforcement is the boundary)
│   ├── Is it B2B payment terms (Net 30/60)?
│   │   └── DON'T REPORT (intentional feature)
│   ├── Can a consumer access B2B pricing without company auth?
│   │   └── REPORT (pricing leakage across buyer types)
│   ├── Can Company A access Company B's catalog?
│   │   └── REPORT (cross-company IDOR)
│   └── Can quantity rules be bypassed server-side?
│       └── REPORT (server-side enforcement bypass)
│
├── Did you find something related to Shopify Functions?
│   ├── Is it that Functions run in a Wasm sandbox?
│   │   └── DON'T REPORT (security boundary)
│   ├── Is it that Functions have no network access by default?
│   │   └── DON'T REPORT (intentional restriction)
│   ├── Is it that Functions prohibit non-determinism?
│   │   └── DON'T REPORT (correctness requirement)
│   ├── Is it that Functions have resource limits (256 kB, 10 MB)?
│   │   └── DON'T REPORT (documented constraints)
│   ├── Can a Function access data beyond its input query scope?
│   │   └── REPORT (data access boundary bypass)
│   └── Can a malicious Function exfiltrate merchant data via fetch?
│       └── REPORT (if fetch target is enabled without proper controls)
│
├── Did you find something related to Web Pixel API?
│   ├── Is it that Web Pixels can see customer event data?
│   │   └── DON'T REPORT (intended analytics functionality)
│   ├── Is it that Web Pixels run in a sandbox without DOM access?
│   │   └── DON'T REPORT (security feature, not a bug)
│   ├── Is it that Web Pixels make fetch() calls to external endpoints?
│   │   └── DON'T REPORT (intended analytics data sending)
│   ├── Can a Pixel access data beyond its declared scopes?
│   │   └── REPORT (scope boundary bypass)
│   ├── Can a Pixel extract credit card data from checkout?
│   │   └── REPORT (critical sandbox escape)
│   └── Is it that custom pixels have lax sandbox access?
│       └── DON'T REPORT (merchant-created, intentional)
│
├── Did you find something related to Checkout Kit?
│   ├── Is it that Checkout Kit requires JWT auth for inline mode?
│   │   └── DON'T REPORT (intended security mechanism)
│   ├── Is it that inline mode needs third-party cookies?
│   │   └── DON'T REPORT (documented browser limitation)
│   ├── Is it that Checkout Kit needs CSP allowlisting?
│   │   └── DON'T REPORT (standard integration requirement)
│   ├── Can Checkout Kit JWTs be forged or reused?
│   │   └── REPORT (JWT validation bypass)
│   ├── Is it that JWT expires in 60 minutes?
│   │   └── DON'T REPORT (reasonable TTL)
│   └── Can client credentials be extracted from mobile Checkout Kit?
│       └── REPORT ONLY IF it's Shopify's credentials (not third-party app dev's)
│
├── Did you find something related to Markets / Shipping?
│   ├── Is it that market subdomains follow a predictable pattern?
│   │   └── DON'T REPORT (intentional SEO structure)
│   ├── Is it that products can be configured per-market?
│   │   └── DON'T REPORT (intentional Markets functionality)
│   ├── Is it multi-currency rounding adjustments?
│   │   └── DON'T REPORT (documented rounding behavior)
│   ├── Can a product hidden in Market A be accessed from Market A?
│   │   └── REPORT (market visibility enforcement bypass)
│   └── Can shipping rates be manipulated via market-driven shipping?
│       └── REPORT IF demonstrated pricing bypass
│
├── Did you find something related to Storefront API?
│   ├── Is it that Storefront API has no documented rate limits?
│   │   └── DON'T REPORT (limits exist but are undocumented)
│   ├── Is it tokenless access (up to 1,000 query cost)?
│   │   └── DON'T REPORT (intentional limited public access)
│   ├── Is it that public tokens are in theme JS?
│   │   └── DON'T REPORT (scope-limited public tokens)
│   ├── Is it that cart IDs are predictable?
│   │   └── DON'T REPORT (no sensitive data in cart alone)
│   ├── Can you brute-force customer login via Storefront API?
│   │   └── REPORT IF successful credential compromise demonstrated
│   └── Can you access private metafields via Storefront API?
│       └── REPORT (metafield access control bypass)
│
├── Did you find a CDN cache poisoning opportunity?
│   ├── Can you poison the cache to serve 404 for legitimate files?
│   │   └── REPORT (H1-1695604 paid $3,800 for this)
│   └── Is it that CDN files are publicly accessible?
│       └── DON'T REPORT (intentional)
│
├── Did you find a webhook security issue?
│   ├── Is HMAC verification missing on a webhook endpoint?
│   │   └── REPORT (H1-3697491)
│   ├── Is the HMAC comparison using == instead of constant-time?
│   │   └── REPORT (timing attack vector)
│   └── Is the webhook secret the same as the API secret?
│       └── REPORT (key separation issue)
│
└── Did you reproduce a known CVE?
    ├── CVE-2024-45718/45719/45720 (Hydrogen health endpoints)?
    │   └── DON'T REPORT (patched in 2024)
    ├── CVE-2026-45618 (LiquidJS RCE)?
    │   └── REPORT ONLY if found in Shopify's own infrastructure
    ├── CVE-2026-30952 (LiquidJS path traversal)?
    │   └── REPORT ONLY if found in Shopify's own infrastructure
    └── GHSA-6j52-38f8-qhxr (Shop context confusion)?
        └── REPORT ONLY if found in unpatched apps
```
