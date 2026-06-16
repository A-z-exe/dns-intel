import requests
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class CertRecord:
    common_name: str
    issuer: str
    not_before: str
    not_after: str
    san: List[str] = field(default_factory=list)


@dataclass
class CertResult:
    domain: str
    timestamp: str
    certificates: List[CertRecord] = field(default_factory=list)
    subdomains: List[str] = field(default_factory=list)
    error: Optional[str] = None


def cert_search(domain: str) -> CertResult:
    result = CertResult(
        domain=domain,
        timestamp=datetime.utcnow().isoformat()
    )
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        headers = {"User-Agent": "dns-intel-tool/1.0"}
        response = requests.get(url, timeout=20, headers=headers)
        if not response.text.strip():
            result.error = "crt.sh returned empty response. Try again in a moment."
            return result
        data = response.json()

        seen = set()
        for entry in data:
            cn = entry.get("common_name", "")
            name_value = entry.get("name_value", "")

            for name in [cn] + name_value.split("\n"):
                name = name.strip().lstrip("*.")
                if name and name not in seen and domain in name:
                    seen.add(name)
                    result.subdomains.append(name)

            cert = CertRecord(
                common_name=cn,
                issuer=entry.get("issuer_name", ""),
                not_before=entry.get("not_before", ""),
                not_after=entry.get("not_after", ""),
            )
            result.certificates.append(cert)

        result.subdomains = sorted(set(result.subdomains))

    except Exception as e:
        result.error = str(e)

    return result
