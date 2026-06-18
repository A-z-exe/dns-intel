#!/usr/bin/env python3
import argparse
import json
import sys
from dataclasses import asdict
from monitor.watcher import watch

from core.dns_lookup import dns_lookup, reverse_dns, get_ip
from core.cert_transparency import cert_search
from core.asn_lookup import asn_lookup
from core.subdomain_enum import subdomain_enum
from graph.domain_graph import build_graph
from storage.db import save_result, get_history, compare_results


BANNER = """
██████╗ ███╗   ██╗███████╗    ██╗███╗   ██╗████████╗███████╗██╗
██╔══██╗████╗  ██║██╔════╝    ██║████╗  ██║╚══██╔══╝██╔════╝██║
██║  ██║██╔██╗ ██║███████╗    ██║██╔██╗ ██║   ██║   █████╗  ██║
██║  ██║██║╚██╗██║╚════██║    ██║██║╚██╗██║   ██║   ██╔══╝  ██║
██████╔╝██║ ╚████║███████║    ██║██║ ╚████║   ██║   ███████╗███████╗
╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝
        DNS Intelligence Platform — by A-z-exe
        github.com/A-z-exe      telegram: @A_z_exe


        
"""

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_section(title):
    print(f"\n{BOLD}{CYAN}{'─'*50}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*50}{RESET}")


def cmd_dns(args):
    print_section(f"DNS Lookup — {args.domain}")
    result = dns_lookup(args.domain)
    if result.error:
        print(f"{RED}Error: {result.error}{RESET}")
    for rec in result.records:
        print(f"  {YELLOW}{rec.record_type:<8}{RESET} {rec.value}  {CYAN}(TTL: {rec.ttl}){RESET}")
    save_result(args.domain, "dns", asdict(result))
    if args.json:
        print(json.dumps(asdict(result), indent=2))


def cmd_rdns(args):
    print_section(f"Reverse DNS — {args.ip}")
    result = reverse_dns(args.ip)
    if result.error:
        print(f"{RED}Error: {result.error}{RESET}")
    for rec in result.records:
        print(f"  {GREEN}{rec.value}{RESET}")


def cmd_cert(args):
    print_section(f"Certificate Transparency — {args.domain}")
    result = cert_search(args.domain)
    if result.error:
        print(f"{RED}Error: {result.error}{RESET}")
        return
    print(f"  Found {GREEN}{len(result.subdomains)}{RESET} unique subdomains from certificates:\n")
    for sub in result.subdomains[:50]:
        print(f"  {GREEN}•{RESET} {sub}")
    if len(result.subdomains) > 50:
        print(f"  {YELLOW}... and {len(result.subdomains)-50} more{RESET}")
    save_result(args.domain, "cert", asdict(result))


def cmd_asn(args):
    ip = args.ip or get_ip(args.domain) if hasattr(args, 'domain') else args.ip
    print_section(f"ASN Lookup — {ip}")
    result = asn_lookup(ip)
    if result.error:
        print(f"{RED}Error: {result.error}{RESET}")
        return
    if result.asn_info:
        info = result.asn_info
        print(f"  ASN    : {GREEN}AS{info.asn}{RESET}")
        print(f"  Name   : {info.name}")
        print(f"  Country: {info.country}")
        print(f"  Prefixes: {', '.join(info.prefixes)}")


def cmd_sub(args):
    print_section(f"Subdomain Enumeration — {args.domain}")
    print(f"  {YELLOW}Running... (this may take a moment){RESET}")
    result = subdomain_enum(args.domain)
    if result.error:
        print(f"{RED}Error: {result.error}{RESET}")
        return
    print(f"\n  Found {GREEN}{len(result.subdomains)}{RESET} subdomains:\n")
    for sub in result.resolved:
        ips = ", ".join(sub["ips"])
        print(f"  {GREEN}•{RESET} {sub['subdomain']:<40} {CYAN}{ips}{RESET}")
    save_result(args.domain, "subdomains", asdict(result))


def cmd_graph(args):
    print_section(f"Building Domain Graph — {args.domain}")
    dns_result = dns_lookup(args.domain)
    ip = get_ip(args.domain)
    asn_result = asn_lookup(ip) if ip else None
    cert_result = cert_search(args.domain)

    graph = build_graph(
        args.domain,
        dns_result=dns_result,
        cert_result=cert_result,
        asn_result=asn_result
    )

    data = graph.to_dict()
    print(f"  Nodes : {GREEN}{len(data['nodes'])}{RESET}")
    print(f"  Edges : {GREEN}{len(data['edges'])}{RESET}\n")

    for node in data["nodes"]:
        print(f"  [{YELLOW}{node['type']:<8}{RESET}] {node['label']}")

    out_file = f"{args.domain}_graph.json"
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n  {GREEN}Graph saved to {out_file}{RESET}")


def cmd_compare(args):
    print_section(f"Compare Results — {args.domain} ({args.type})")
    diff = compare_results(args.domain, args.type)
    if not diff:
        print(f"  {YELLOW}Not enough history to compare. Run the scan at least twice.{RESET}")
        return
    print(f"  Previous : {diff['previous_timestamp']}")
    print(f"  Latest   : {diff['latest_timestamp']}\n")
    if diff["added"]:
        print(f"  {GREEN}[+] Added ({len(diff['added'])}):{RESET}")
        for item in diff["added"]:
            print(f"      + {item}")
    if diff["removed"]:
        print(f"  {RED}[-] Removed ({len(diff['removed'])}):{RESET}")
        for item in diff["removed"]:
            print(f"      - {item}")
    if not diff["added"] and not diff["removed"]:
        print(f"  {GREEN}No changes detected.{RESET}")


def cmd_full(args):
    print_section(f"Full Recon — {args.domain}")
    dns_result = dns_lookup(args.domain)
    ip = get_ip(args.domain)

    print(f"\n{BOLD}[1/4] DNS Records{RESET}")
    for rec in dns_result.records:
        print(f"  {YELLOW}{rec.record_type:<8}{RESET} {rec.value}")

    print(f"\n{BOLD}[2/4] Certificate Transparency{RESET}")
    cert_result = cert_search(args.domain)
    print(f"  Found {GREEN}{len(cert_result.subdomains)}{RESET} subdomains from certs")

    print(f"\n{BOLD}[3/4] Subdomain Enumeration{RESET}")
    sub_result = subdomain_enum(args.domain)
    print(f"  Found {GREEN}{len(sub_result.subdomains)}{RESET} active subdomains")

    print(f"\n{BOLD}[4/4] ASN Info{RESET}")
    asn_result = None
    if ip:
        asn_result = asn_lookup(ip)
        if asn_result.asn_info:
            print(f"  AS{asn_result.asn_info.asn} — {asn_result.asn_info.name} ({asn_result.asn_info.country})")

    graph = build_graph(args.domain, dns_result, cert_result, sub_result, asn_result)
    out_file = f"{args.domain}_graph.json"
    with open(out_file, "w") as f:
        json.dump(graph.to_dict(), f, indent=2)

    save_result(args.domain, "dns", asdict(dns_result))
    save_result(args.domain, "cert", asdict(cert_result))
    save_result(args.domain, "subdomains", asdict(sub_result))

    print(f"\n  {GREEN}Full recon complete. Graph saved to {out_file}{RESET}")


def cmd_monitor(args):
    print_section(f"DNS Monitor — {args.domain}")
    watch(
        domain=args.domain,
        interval=args.interval,
        scan_type=args.type
    )


def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="DNS Intelligence Platform")
    sub = parser.add_subparsers(dest="command")

    p_dns = sub.add_parser("dns", help="DNS lookup")
    p_dns.add_argument("domain")
    p_dns.add_argument("--json", action="store_true")

    p_rdns = sub.add_parser("rdns", help="Reverse DNS")
    p_rdns.add_argument("ip")

    p_cert = sub.add_parser("cert", help="Certificate Transparency search")
    p_cert.add_argument("domain")

    p_asn = sub.add_parser("asn", help="ASN Lookup")
    p_asn.add_argument("ip")

    p_sub = sub.add_parser("sub", help="Subdomain enumeration")
    p_sub.add_argument("domain")

    p_graph = sub.add_parser("graph", help="Build domain relationship graph")
    p_graph.add_argument("domain")

    p_compare = sub.add_parser("compare", help="Compare scan results over time")
    p_compare.add_argument("domain")
    p_compare.add_argument("--type", default="subdomains", choices=["dns", "subdomains", "cert"])

    p_full = sub.add_parser("full", help="Full recon on a domain")
    p_full.add_argument("domain")

    p_monitor = sub.add_parser("monitor", help="Monitor DNS changes and alert via Telegram")
    p_monitor.add_argument("domain")
    p_monitor.add_argument("--interval", type=int, default=3600, help="Check interval in seconds")
    p_monitor.add_argument("--type", default="dns", choices=["dns", "subdomains", "cert"])

    args = parser.parse_args()

    commands = {
        "dns": cmd_dns,
        "rdns": cmd_rdns,
        "cert": cmd_cert,
        "asn": cmd_asn,
        "sub": cmd_sub,
        "graph": cmd_graph,
        "compare": cmd_compare,
        "full": cmd_full,
        "monitor": cmd_monitor,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
