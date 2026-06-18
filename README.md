# 🔍 DNS Intelligence Platform

<<<<<<< HEAD
> A powerful DNS reconnaissance, asset discovery, and real-time monitoring tool for security researchers and bug bounty hunters.
=======
> A powerful DNS reconnaissance and asset discovery tool for security researchers and bug bounty hunters.
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Purpose](https://img.shields.io/badge/Purpose-Educational%20%26%20Defensive-blue?style=flat)
<<<<<<< HEAD
![Version](https://img.shields.io/badge/Version-1.1.0-orange?style=flat)
=======
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔎 DNS Lookup | Query all record types (A, AAAA, MX, NS, TXT, CNAME, SOA) |
| 🔄 Reverse DNS | PTR record resolution for IPs |
| 📜 Certificate Transparency | Find subdomains via crt.sh |
| 🌐 ASN Lookup | Organization and prefix info via BGPView |
| 🕵️ Subdomain Enumeration | Fast multithreaded bruteforce |
| 🕸️ Domain Graph | Visual relationship mapping (JSON export) |
| 💾 History & Compare | Save results and detect changes over time |
<<<<<<< HEAD
| 🔔 DNS Monitor | Real-time monitoring with Telegram alerts |
=======
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4
| 🚀 Full Recon | Run all modules in one command |

---

## 📦 Installation

```bash
git clone https://github.com/A-z-exe/dns-intel.git
cd dns-intel
pip install -r requirements.txt
```

---

<<<<<<< HEAD
## ⚙️ Configuration

Create a `.env` file in the project root:

```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

**How to get Telegram credentials:**
1. Open `@BotFather` on Telegram → `/newbot` → copy the token
2. Open `@userinfobot` on Telegram → copy your Chat ID

---

=======
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4
## 🚀 Usage

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
# Outputs: example.com_graph.json
```

### Compare Results Over Time
```bash
python cli.py compare example.com --type subdomains
```

<<<<<<< HEAD
### 🔔 DNS Monitor + Telegram Alerts
```bash
# Monitor DNS records every hour
python cli.py monitor example.com --interval 3600 --type dns

# Monitor subdomains every 6 hours
python cli.py monitor example.com --interval 21600 --type subdomains

# Monitor certificates every 12 hours
python cli.py monitor example.com --interval 43200 --type cert
```

When a change is detected, you receive a Telegram message like:
```
🔔 DNS Change Detected
🌐 Domain: example.com

✅ Added:
  + 192.168.1.1

❌ Removed:
  - 10.0.0.1
```

=======
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4
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
<<<<<<< HEAD
├── monitor/
│   ├── watcher.py           # DNS change detection
│   └── alerts.py            # Telegram notifications
=======
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4
├── graph/
│   └── domain_graph.py      # Relationship graph builder
├── storage/
│   └── db.py                # SQLite history & compare
├── cli.py                   # Main CLI interface
<<<<<<< HEAD
├── requirements.txt
└── .env                     # Your credentials (not committed)
```

---

## 📋 Requirements

```
dnspython>=2.4.0
requests>=2.31.0
python-dotenv>=1.0.0
=======
└── requirements.txt
>>>>>>> 7cc461b33a0a7a2948e5cd98b511eaca7d905fd4
```

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes** and **authorized security testing only**.
Only use on domains you own or have explicit permission to test.
The author is not responsible for any misuse.

---

## 👤 Author

**AmirHossein Zarei** — [github.com/A-z-exe](https://github.com/A-z-exe)

🔐 Security Researcher | 🐍 Python Developer | 🐛 Bug Bounty Hunter
