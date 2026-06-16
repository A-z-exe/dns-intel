import dns.resolver
import dns.reversename
import socket
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class DNSRecord:
    record_type: str
    value: str
    ttl: Optional[int] = None


@dataclass
class DNSResult:
    domain: str
    timestamp: str
    records: List[DNSRecord] = field(default_factory=list)
    error: Optional[str] = None


RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"]


def dns_lookup(domain: str, record_types: List[str] = None) -> DNSResult:
    if record_types is None:
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]

    result = DNSResult(
        domain=domain,
        timestamp=datetime.utcnow().isoformat()
    )

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                result.records.append(DNSRecord(
                    record_type=rtype,
                    value=str(rdata),
                    ttl=answers.ttl
                ))
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        except Exception as e:
            result.error = str(e)

    return result


def reverse_dns(ip: str) -> DNSResult:
    result = DNSResult(
        domain=ip,
        timestamp=datetime.utcnow().isoformat()
    )
    try:
        rev_name = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(rev_name, "PTR")
        for rdata in answers:
            result.records.append(DNSRecord(
                record_type="PTR",
                value=str(rdata)
            ))
    except Exception as e:
        result.error = str(e)

    return result


def get_ip(domain: str) -> Optional[str]:
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None
