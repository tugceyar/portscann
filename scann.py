import os
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

PORTS = [22, 80, 443]
TIMEOUT = 0.5
RESULTS = []
lock = Lock()


def banner():
    print("""
        Port tarama  
    """)


def ping(ip):
    command = f"ping -c 1 -W 1 {ip} > /dev/null 2>&1"
    return os.system(command) == 0


def scan_ports(ip):
    open_ports = []
    for port in PORTS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports


def scan_host(ip):
    ip = str(ip)

    if ping(ip):
        ports = scan_ports(ip)
        port_text = ",".join(map(str, ports)) if ports else "-"
        with lock:
            RESULTS.append((ip, "AKTİF", port_text))
    else:
        with lock:
            RESULTS.append((ip, "PASİF", "-"))


def scan_network(network):
    print(f"\n Taranan Network: {network}\n")

    with ThreadPoolExecutor(max_workers=50) as executor:
        for ip in ipaddress.IPv4Network(network, strict=False):
            executor.submit(scan_host, ip)


def print_table():
    print("\n{:<16} {:<10} {:<20}".format("IP ADRESİ", "DURUM", "AÇIK PORTLAR"))
    print("-" * 50)

    for ip, status, ports in sorted(RESULTS):
        print("{:<16} {:<10} {:<20}".format(ip, status, ports))


if __name__ == "__main__":
    banner()
    network = input("Network giriniz")
    scan_network(network)
    print_table()
