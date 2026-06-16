# 🔍 DNS Intelligence Platform

> A powerful DNS reconnaissance and asset discovery tool for security researchers and bug bounty hunters.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Purpose](https://img.shields.io/badge/Purpose-Educational%20%26%20Defensive-blue?style=flat)

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
| 🚀 Full Recon | Run all modules in one command |

---

## 📦 Installation

```bash
git clone https://github.com/A-z-exe/dns-intel.git
cd dns-intel
pip install -r requirements.txt
```

---

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
├── graph/
│   └── domain_graph.py      # Relationship graph builder
├── storage/
│   └── db.py                # SQLite history & compare
├── cli.py                   # Main CLI interface
└── requirements.txt
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
