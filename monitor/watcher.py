import time
import sys
import os
from dataclasses import asdict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dns_lookup import dns_lookup
from core.cert_transparency import cert_search
from core.subdomain_enum import subdomain_enum
from storage.db import save_result, compare_results
from monitor.alerts import alert_changes, send_telegram


def watch(domain: str, interval: int = 3600, scan_type: str = "dns"):
    print(f"👁️  Watching: {domain}")
    print(f"⏱️  Interval: every {interval} seconds")
    print(f"📡  Scan type: {scan_type}")
    print(f"🕐  Started at: {datetime.utcnow().isoformat()}")
    print("─" * 50)

    send_telegram(f"👁️ *DNS Monitor Started*\n🌐 Domain: `{domain}`\n⏱️ Interval: {interval}s\n📡 Type: {scan_type}")

    while True:
        try:
            print(f"\n[{datetime.utcnow().strftime('%H:%M:%S')}] Scanning {domain}...")

            if scan_type == "dns":
                result = dns_lookup(domain)
                save_result(domain, "dns", asdict(result))

            elif scan_type == "subdomains":
                result = subdomain_enum(domain)
                save_result(domain, "subdomains", asdict(result))

            elif scan_type == "cert":
                result = cert_search(domain)
                save_result(domain, "cert", asdict(result))

            changes = compare_results(domain, scan_type)
            if changes:
                if changes["added"] or changes["removed"]:
                    print(f"  ⚠️  Changes detected!")
                    print(f"  Added   : {changes['added']}")
                    print(f"  Removed : {changes['removed']}")
                    alert_changes(domain, changes)
                else:
                    print(f"  ✅ No changes.")
            else:
                print(f"  📝 First snapshot saved.")

        except KeyboardInterrupt:
            print("\n\n🛑 Monitor stopped.")
            send_telegram(f"🛑 *DNS Monitor Stopped*\n🌐 Domain: `{domain}`")
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")

        print(f"  💤 Next scan in {interval}s...")
        time.sleep(interval)
