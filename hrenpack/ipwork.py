"""
Network IP address utilities.

Provides functions to get local IPv4 addresses.

Утилиты для работы с IP-адресами сети.

Предоставляет функции для получения локальных IPv4 адресов.
"""

import socket


def get_ipv4_addresses(exclude_localhost: bool = False) -> list:
    """
    Get all IPv4 addresses of the local host.

    Получает все IPv4 адреса локального хоста.

    Args:
        exclude_localhost (bool): Exclude 127.0.0.1 from results, default False / Исключить 127.0.0.1 из результатов

    Returns:
        list: List of IPv4 addresses / Список IPv4 адресов
    """
    ip_addresses = []

    # Get hostname
    hostname = socket.gethostname()

    try:
        # Get all IP addresses associated with the host
        addresses = socket.getaddrinfo(hostname, None)

        for addr_info in addresses:
            # addr_info[0] - address family (AF_INET for IPv4)
            # addr_info[4][0] - IP address
            if addr_info[0] == socket.AF_INET:  # IPv4
                ip = addr_info[4][0]
                if ip not in ip_addresses and (ip != '127.0.0.1' or not exclude_localhost):
                    ip_addresses.append(ip)

    except socket.gaierror:
        pass

    # If no addresses found, try another method
    if not ip_addresses:
        try:
            # Create temporary socket to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))  # Connect to external server
            local_ip = s.getsockname()[0]
            s.close()
            if local_ip != '127.0.0.1' or not exclude_localhost:
                ip_addresses.append(local_ip)
        except:
            pass

    return ip_addresses
