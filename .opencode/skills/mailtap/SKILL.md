---
name: mailtap
description: >-
  Temporary email automation via mail.tm API.
  Membuat akun temporer, cek inbox, tunggu email, ekstrak OTP/link verifikasi.
  Terintegrasi dengan browser-local untuk registrasi akun di target.
license: MIT
compatibility: opencode
metadata:
  category: automation
  technique: email-temp
---

# MailTap — Email Temporary Automation                        
Tool untuk membuat dan mengelola email temporer via mail.tm API. Digunakan saat registrasi akun di platform target yang memerlukan verifikasi email.

**Tools**: `mailtap`
**Penyimpanan**: `~/.tempmail/accounts.json`

---

## Quick Reference

```bash
# Buat akun baru (opsional: jika list akun tidak ada atau tidak bisa digunakan)
mailtap --create <nama>

# Lihat daftar akun (prioritas)
mailtap list

# Cek inbox (default akun: shopify_attacker)
mailtap inbox <nama>

# Baca pesan spesifik (default akun: shopify_attacker)
mailtap read <nama> <msg_id_prefix>
```

---

## Tunggu & Ekstrak

```bash
# Tunggu email masuk (timeout default 60s)
mailtap wait <nama>

# Filter by subject
mailtap wait <nama> --subject "verifikasi"

# Ambil OTP (4-8 digit)
mailtap wait <nama> --otp

# Ambil link verifikasi
mailtap wait <nama> --link

# Dengan timeout kustom
mailtap wait <nama> --subject "konfirmasi" --timeout 120 --otp
```

---

## Akun Multi

```bash
# Buat akun victim dan attacker terpisah
mailtap --create victim
mailtap --create attacker

# Cek semua akun
mailtap list

```

---

## Notes

- Akun mail.tm valid ~7 hari, setelah itu email hangus
- Password default: `Testing123`
- API bersifat receive-only (SMTP tidak didukung)
- Gunakan `--json` pada `wait` untuk parsing programatik:
  ```bash
  mailtap wait target --otp --json
  → {"found": true, "id": "...", "subject": "...", "otp": "482916", ...}
  ```
