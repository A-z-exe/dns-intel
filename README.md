# 🔍 DNS Intel
### Discover • Monitor • Analyze

A powerful DNS reconnaissance, asset discovery, and monitoring platform built for security researchers, penetration testers, and bug bounty hunters.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Version](https://img.shields.io/badge/Version-v0.2.0-orange?style=flat)
![Status](https://img.shields.io/badge/Status-Active%20Development-blue?style=flat)

---

## 🚀 Overview

DNS Intel is an open-source DNS intelligence platform designed to assist security professionals in reconnaissance, asset discovery, DNS monitoring, and infrastructure analysis.

The project combines multiple intelligence sources into a unified command-line interface, enabling researchers to identify assets, monitor DNS changes, discover subdomains, and build domain relationship graphs.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 🔎 DNS Lookup | Query A, AAAA, MX, NS, TXT, CNAME, and SOA records |
| 🔄 Reverse DNS | Resolve PTR records from IP addresses |
| 📜 Certificate Transparency | Discover subdomains using CT logs via crt.sh |
| 🌐 ASN Intelligence | Retrieve ASN, prefix, and organization information |
| 🕵️ Subdomain Enumeration | Multithreaded subdomain discovery |
| 🕸️ Domain Graph | Generate domain relationship maps (JSON export) |
| 💾 History Tracking | Store and compare historical scan results |
| 🔔 Real-time Monitoring | Detect infrastructure changes with Telegram alerts |
| 🚀 Full Recon | Execute all modules with a single command |

---

## 📦 Installation

```bash
git clone https://github.com/A-z-exe/dns-intel.git
cd dns-intel
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the project root for Telegram alerts:

```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**How to get your credentials:**
1. Open `@BotFather` on Telegram → send `/newbot` → copy the token
2. Open `@userinfobot` on Telegram → copy your Chat ID

---

## 🖥️ Usage

### DNS Lookup
```bash
python cli.py dns example.com
```

### Reverse DNS
```bash
python cli.py rdns 1.1.1.1
```

### Certificate Transparency
```bash
python cli.py cert example.com
```

### ASN Lookup
```bash
python cli.py asn 1.1.1.1
```

### Subdomain Enumeration
```bash
python cli.py sub example.com
```

### Domain Relationship Graph
```bash
python cli.py graph example.com
```

### Compare Results Over Time
```bash
python cli.py compare example.com --type subdomains
```

### 🔔 Real-time Monitoring + Telegram Alerts
```bash
# Monitor DNS records every hour
python cli.py monitor example.com --interval 3600 --type dns

# Monitor subdomains every 6 hours
python cli.py monitor example.com --interval 21600 --type subdomains
```

When a change is detected, you receive a Telegram alert:
```
🔔 DNS Change Detected
🌐 Domain: example.com

✅ Added:
  + 192.168.1.1

❌ Removed:
  - 10.0.0.1
```

### Full Recon (All Modules)
```bash
python cli.py full example.com
```

---

## 📁 Project Structure

```
dns-intel/
├── core/
│   ├── dns_lookup.py        # DNS & Reverse DNS
│   ├── cert_transparency.py # crt.sh integration
│   ├── asn_lookup.py        # BGPView ASN info
│   └── subdomain_enum.py    # Multithreaded bruteforce
├── monitor/
│   ├── watcher.py           # DNS change detection
│   └── alerts.py            # Telegram notifications
├── graph/
│   └── domain_graph.py      # Relationship graph builder
├── storage/
│   └── db.py                # SQLite history & compare
├── cli.py                   # Main CLI interface
├── requirements.txt
└── .env                     # Your credentials (not committed)
```

---

## 🛣️ Roadmap

- [x] DNS Lookup
- [x] Reverse DNS
- [x] ASN Lookup
- [x] Certificate Transparency
- [x] Subdomain Enumeration
- [x] Real-time DNS Monitoring + Telegram Alerts
- [ ] Interactive Graph Visualization
- [ ] HTML Report Export
- [ ] Passive DNS Support
- [ ] Docker Support
- [ ] REST API
- [ ] Web Dashboard
- [ ] Multi-Target Reconnaissance

---

## ⚠️ Disclaimer

This project is intended for **educational purposes** and **authorized security testing only**.
Only perform reconnaissance activities against systems and domains that you own or have explicit permission to assess.
The author assumes no responsibility for misuse of this software.

---

## 👨‍💻 Author

**AmirHossein Zarei**
Security Researcher • Python Developer • Bug Bounty Hunter

GitHub: [github.com/A-z-exe](https://github.com/A-z-exe)
