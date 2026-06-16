import requests
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class ASNInfo:
    asn: str
    name: str
    country: str
    prefixes: List[str] = field(default_factory=list)


@dataclass
class ASNResult:
    ip: str
    timestamp: str
    asn_info: Optional[ASNInfo] = None
    error: Optional[str] = None


def asn_lookup(ip: str) -> ASNResult:
    result = ASNResult(
        ip=ip,
        timestamp=datetime.utcnow().isoformat()
    )
    try:
        url = f"https://api.bgpview.io/ip/{ip}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") == "ok":
            prefixes = data["data"].get("prefixes", [])
            asn_list = []
            for p in prefixes:
                asn_data = p.get("asn", {})
                asn_list.append(ASNInfo(
                    asn=str(asn_data.get("asn", "")),
                    name=asn_data.get("name", ""),
                    country=asn_data.get("country_code", ""),
                    prefixes=[p.get("prefix", "")]
                ))
            if asn_list:
                result.asn_info = asn_list[0]
    except Exception as e:
        result.error = str(e)

    return result
