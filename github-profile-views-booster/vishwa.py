import json
import threading
from time import sleep
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

import httpx
from colorama import Fore

config_file = json.load(open('config.json', 'r', encoding='utf-8'))
lock = threading.Lock()

def safe_print(*args):
    lock.acquire()
    for arg in args:
        print(arg, end=' ')
    print()
    lock.release()

def run():
    while True:
        try:
            url = config_file['counter_url']
            response = httpx.get(url, timeout=10)
        except httpx.ConnectTimeout:
            safe_print(f"{Fore.LIGHTRED_EX}[-] Timeout error.")
            continue

        if response.status_code == 200:
            with lock:
                count = config_file.get('count', 0)
                count += 1
                config_file['count'] = count
            safe_print(f"{Fore.LIGHTGREEN_EX}[+] Successful request! Total successful requests sent: {count}")
        elif 'Bad Signature' in response.text:
            safe_print(f"{Fore.LIGHTRED_EX}[-] Invalid Camo Link! Please change valid link.")
            break
        else:
            safe_print(f"{Fore.LIGHTRED_EX}[-] Error request.")

clear()
threads = config_file.get('threads', 100)

for _ in range(threads):
    threading.Thread(target=run).start()
