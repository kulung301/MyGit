import requests
import socket

def get_public_ip():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        return "Gagal cek IP publik"

def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Gagal cek IP lokal"

if __name__ == "__main__":
    print("🌐 IP Publik :", get_public_ip())
    print("🏠 IP Lokal  :", get_local_ip())
