import requests
import dns.resolver
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import concurrent.futures


@dataclass
class SubdomainResult:
    domain: str
    timestamp: str
    subdomains: List[str] = field(default_factory=list)
    resolved: List[dict] = field(default_factory=list)
    error: Optional[str] = None


WORDLIST = [
    "www", "mail", "ftp", "api", "dev", "staging", "test", "admin",
    "portal", "vpn", "ssh", "smtp", "pop", "imap", "ns1", "ns2",
    "blog", "shop", "cdn", "static", "media", "img", "assets",
    "app", "mobile", "m", "beta", "alpha", "login", "auth", "oauth",
    "dashboard", "panel", "secure", "git", "gitlab", "jenkins", "ci",
    "docs", "support", "help", "status", "monitor", "grafana",
    "db", "database", "mysql", "postgres", "redis", "mongo",
    "internal", "intranet", "corp", "office", "remote", "vpn2",
]


def _check_subdomain(subdomain: str, domain: str) -> Optional[dict]:
    full = f"{subdomain}.{domain}"
    try:
        answers = dns.resolver.resolve(full, "A")
        ips = [str(r) for r in answers]
        return {"subdomain": full, "ips": ips}
    except Exception:
        return None


def subdomain_enum(domain: str, wordlist: List[str] = None, threads: int = 20) -> SubdomainResult:
    if wordlist is None:
        wordlist = WORDLIST

    result = SubdomainResult(
        domain=domain,
        timestamp=datetime.utcnow().isoformat()
    )

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(_check_subdomain, sub, domain): sub
                for sub in wordlist
            }
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    result.subdomains.append(res["subdomain"])
                    result.resolved.append(res)

        result.subdomains.sort()
        result.resolved.sort(key=lambda x: x["subdomain"])

    except Exception as e:
        result.error = str(e)

    return result
