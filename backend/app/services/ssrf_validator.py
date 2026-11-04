import socket
import ipaddress
from urllib.parse import urlparse
from typing import Tuple

BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),       # Link-local / Cloud metadata (169.254.169.254)
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("224.0.0.0/4"),          # Multicast
    ipaddress.ip_network("240.0.0.0/4"),          # Reserved
    ipaddress.ip_network("255.255.255.255/32"),
    # IPv6 blocked ranges
    ipaddress.ip_network("::/128"),
    ipaddress.ip_network("::1/128"),              # IPv6 loopback
    ipaddress.ip_network("::ffff:0:0/96"),        # IPv4-mapped IPv6
    ipaddress.ip_network("64:ff9b::/96"),         # IPv4/IPv6 translation
    ipaddress.ip_network("2001:db8::/32"),        # Documentation prefix
    ipaddress.ip_network("fc00::/7"),             # Unique local
    ipaddress.ip_network("fe80::/10"),            # Link-local
    ipaddress.ip_network("ff00::/8"),             # Multicast
    ipaddress.ip_network("fd00:ec2::254/128"),    # AWS IMDSv2 IPv6
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "127.0.0.1",
    "::1",
    "metadata.google.internal",
    "metadata",
    "instance-data",
    "169.254.169.254",
}

def is_safe_url(url: str) -> Tuple[bool, str]:
    """
    Validates a URL against SSRF vulnerabilities:
    - Allows only http and https schemes
    - Resolves hostname to IPs and blocks private/loopback/cloud metadata addresses
    - Restricts port to 80, 443, or standard HTTP/HTTPS ports
    """
    if not url or not isinstance(url, str):
        return False, "URL is empty or invalid"

    try:
        parsed = urlparse(url.strip())
    except Exception as e:
        return False, f"Malformed URL: {e}"

    if parsed.scheme.lower() not in ("http", "https"):
        return False, f"Scheme '{parsed.scheme}' not allowed. Only http and https are permitted."

    hostname = parsed.hostname
    if not hostname:
        return False, "No valid hostname found in URL."

    hostname_lower = hostname.lower().strip("[]")
    if hostname_lower in BLOCKED_HOSTNAMES:
        return False, f"Host '{hostname}' is not permitted."

    # Immediate check for direct IP address literals in hostname
    try:
        raw_ip = ipaddress.ip_address(hostname_lower)
        if raw_ip.is_loopback or raw_ip.is_private or raw_ip.is_link_local or raw_ip.is_multicast or raw_ip.is_reserved:
            return False, f"Host '{hostname}' is a restricted IP address."
        for blocked_net in BLOCKED_IP_NETWORKS:
            if raw_ip in blocked_net:
                return False, f"Host '{hostname}' is in a blocked network range."
    except ValueError:
        pass # Not a raw IP literal, proceed to DNS resolution

    # Validate port
    port = parsed.port
    if port and port not in (80, 443, 8080, 8443):
        return False, f"Port '{port}' is not permitted for documentation research."

    # Resolve IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, port or (443 if parsed.scheme == 'https' else 80), proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        return False, f"Could not resolve domain '{hostname}': {e}"
    except Exception as e:
        return False, f"Error validating hostname '{hostname}': {e}"

    for _, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            return False, f"Invalid IP address resolved: {ip_str}"

        if ip_obj.is_loopback or ip_obj.is_private or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved:
            return False, f"Domain resolved to restricted IP address: {ip_str}"

        for blocked_net in BLOCKED_IP_NETWORKS:
            if ip_obj in blocked_net:
                return False, f"Domain resolved to blocked network range: {ip_str}"

    return True, "URL is safe"

