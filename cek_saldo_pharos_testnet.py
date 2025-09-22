import requests
from decimal import Decimal

URL = "https://api.zan.top/node/v1/pharos/testnet/7bbf30cd3a774b4ebbd9750aa6204994"
ADDRESS = "0xdf712323c4b7c67aa3517baa9c1e4c8a924a86cd"

# ANSI warna
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"

def get_balance(address):
    payload = {
        "jsonrpc":"2.0",
        "method":"eth_getBalance",
        "params":[address, "latest"],
        "id":1
    }
    res = requests.post(URL, json=payload).json()
    hex_bal = res.get("result")
    if not hex_bal:
        return None
    wei = int(hex_bal, 16)
    return Decimal(wei) / Decimal(10**18)

def get_tx_count(address):
    payload = {
        "jsonrpc":"2.0",
        "method":"eth_getTransactionCount",
        "params":[address, "latest"],
        "id":1
    }
    res = requests.post(URL, json=payload).json()
    hex_count = res.get("result")
    if not hex_count:
        return None
    return int(hex_count, 16)

if __name__ == "__main__":
    saldo = get_balance(ADDRESS)
    tx_count = get_tx_count(ADDRESS)

    print(f"{GREEN}📊 Wallet Info{RESET}")
    print(f"{CYAN}🪪 Address : {ADDRESS}{RESET}")
    print(f"{YELLOW}💎 Saldo   : {saldo} ZAN{RESET}" if saldo is not None else "Gagal cek saldo")
    print(f"{BLUE}📝 Tx Count: {tx_count}{RESET}" if tx_count is not None else "Gagal cek transaksi")
