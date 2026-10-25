#!/usr/bin/env python3
"""Send a Wake-on-LAN magic packet.

Usage: wake_on_lan.py <mac | host name> [broadcast address]

Host names are defined in HOSTS below. The packet is a broadcast, so it must be
sent from a machine on the same LAN as the target (not through Tailscale).
"""
import socket
import sys

HOSTS = {
    "s720": "90:1b:0e:65:2c:9f",  # Futro S720, 192.168.1.101
}
DEFAULT_BROADCAST = "192.168.1.255"


def send_magic_packet(mac: str, broadcast: str = DEFAULT_BROADCAST) -> None:
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    if len(mac_bytes) != 6:
        raise ValueError(f"invalid MAC address: {mac}")
    packet = b"\xff" * 6 + mac_bytes * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for _ in range(3):
            sock.sendto(packet, (broadcast, 9))


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    target = sys.argv[1]
    mac = HOSTS.get(target, target)
    broadcast = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BROADCAST
    send_magic_packet(mac, broadcast)
    print(f"Magic packet sent to {mac} via {broadcast}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
