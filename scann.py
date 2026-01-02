import socket
from tabulate import tabulate
from colorama import Fore, init

init(autoreset=True)

def host_kontrol(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        s.connect((ip, port))
        s.close()
        return Fore.GREEN + "ERİŞİLEBİLİR"
    except:
        return Fore.RED + "ERİŞİLEMİYOR"


print(Fore.CYAN + """
====================================
   SOCKET TABANLI NETWORK SCANNER
====================================
""")

network = input("IP bloğunu gir (örn: 192.168.1): ").strip()
port = int(input("Kontrol edilecek port: "))

sonuclar = []

print(Fore.YELLOW + "\n[+] Tarama başlatıldı...\n")

for i in range(1, 255):
    ip = f"{network}.{i}"
    durum = host_kontrol(ip, port)
    sonuclar.append([ip, durum])
    print(f"{ip} → {durum}")

print(Fore.CYAN + "\n📊 TARAMA SONUÇLARI\n")
print(tabulate(sonuclar, headers=["IP Adresi", "Durum"], tablefmt="grid"))
