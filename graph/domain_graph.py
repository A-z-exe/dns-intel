from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class GraphNode:
    id: str
    label: str
    node_type: str  # domain, ip, asn, cert


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str  # resolves_to, ptr, subdomain_of, issued_for


@dataclass
class DomainGraph:
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    _node_ids: set = field(default_factory=set, repr=False)

    def add_node(self, id: str, label: str, node_type: str):
        if id not in self._node_ids:
            self.nodes.append(GraphNode(id=id, label=label, node_type=node_type))
            self._node_ids.add(id)

    def add_edge(self, source: str, target: str, relation: str):
        self.edges.append(GraphEdge(source=source, target=target, relation=relation))

    def to_dict(self) -> dict:
        return {
            "nodes": [{"id": n.id, "label": n.label, "type": n.node_type} for n in self.nodes],
            "edges": [{"source": e.source, "target": e.target, "relation": e.relation} for e in self.edges],
        }


def build_graph(domain: str, dns_result=None, cert_result=None, subdomain_result=None, asn_result=None) -> DomainGraph:
    g = DomainGraph()
    g.add_node(domain, domain, "domain")

    if dns_result:
        for rec in dns_result.records:
            if rec.record_type in ("A", "AAAA"):
                g.add_node(rec.value, rec.value, "ip")
                g.add_edge(domain, rec.value, "resolves_to")
            elif rec.record_type == "NS":
                ns = rec.value.rstrip(".")
                g.add_node(ns, ns, "domain")
                g.add_edge(domain, ns, "ns")
            elif rec.record_type == "MX":
                mx = rec.value.split()[-1].rstrip(".")
                g.add_node(mx, mx, "domain")
                g.add_edge(domain, mx, "mx")

    if subdomain_result:
        for sub in subdomain_result.resolved:
            sub_domain = sub["subdomain"]
            g.add_node(sub_domain, sub_domain, "domain")
            g.add_edge(domain, sub_domain, "subdomain_of")
            for ip in sub.get("ips", []):
                g.add_node(ip, ip, "ip")
                g.add_edge(sub_domain, ip, "resolves_to")

    if cert_result:
        for sub in cert_result.subdomains[:20]:
            if sub != domain:
                g.add_node(sub, sub, "domain")
                g.add_edge(domain, sub, "cert_san")

    if asn_result and asn_result.asn_info:
        asn_id = f"AS{asn_result.asn_info.asn}"
        g.add_node(asn_id, f"{asn_id} ({asn_result.asn_info.name})", "asn")
        g.add_edge(asn_result.ip, asn_id, "belongs_to")

    return g
