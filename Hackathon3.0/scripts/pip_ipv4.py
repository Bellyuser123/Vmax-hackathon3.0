"""Forces pip to use IPv4 to bypass Windows IPv6 TCP timeout / connection reset issues."""

import sys
import socket

# Monkeypatch socket.getaddrinfo to strictly return IPv4 (AF_INET) addresses
_orig_getaddrinfo = socket.getaddrinfo

def _ipv4_getaddrinfo(host, port, family=0, *args):
    return _orig_getaddrinfo(host, port, socket.AF_INET, *args)

socket.getaddrinfo = _ipv4_getaddrinfo

# Invoke pip
from pip._internal.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
