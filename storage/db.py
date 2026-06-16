import json
import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict


DB_PATH = os.path.expanduser("~/.dns-intel/results.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            scan_type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_result(domain: str, scan_type: str, data: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO scans (domain, scan_type, timestamp, data) VALUES (?, ?, ?, ?)",
        (domain, scan_type, datetime.utcnow().isoformat(), json.dumps(data))
    )
    conn.commit()
    conn.close()


def get_history(domain: str, scan_type: str = None) -> List[dict]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if scan_type:
        c.execute(
            "SELECT id, domain, scan_type, timestamp, data FROM scans WHERE domain=? AND scan_type=? ORDER BY timestamp DESC",
            (domain, scan_type)
        )
    else:
        c.execute(
            "SELECT id, domain, scan_type, timestamp, data FROM scans WHERE domain=? ORDER BY timestamp DESC",
            (domain,)
        )
    rows = c.fetchall()
    conn.close()
    return [
        {"id": r[0], "domain": r[1], "scan_type": r[2], "timestamp": r[3], "data": json.loads(r[4])}
        for r in rows
    ]


def compare_results(domain: str, scan_type: str) -> Optional[Dict]:
    history = get_history(domain, scan_type)
    if len(history) < 2:
        return None

    latest = history[0]["data"]
    previous = history[1]["data"]

    def extract_values(data, key):
        val = data.get(key, [])
        if isinstance(val, list):
            return set(str(v) for v in val)
        return set()

    key_map = {
        "dns": "records",
        "subdomains": "subdomains",
        "cert": "subdomains",
    }
    key = key_map.get(scan_type, "subdomains")

    latest_set = extract_values(latest, key)
    previous_set = extract_values(previous, key)

    return {
        "domain": domain,
        "scan_type": scan_type,
        "latest_timestamp": history[0]["timestamp"],
        "previous_timestamp": history[1]["timestamp"],
        "added": list(latest_set - previous_set),
        "removed": list(previous_set - latest_set),
        "unchanged": list(latest_set & previous_set),
    }
