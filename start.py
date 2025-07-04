#!/usr/bin/env python
# coding: utf-8
# Author: MaDyEl
# Professional Load Testing Tool

import socket
import threading
import time
import random
from fake_useragent import UserAgent

BANNER = r"""
  _______  _______  ______            _______  _       
(       )(  ___  )(  __  \ |\     /|(  ____ \( \      
| () () || (   ) || (  \  )( \   / )| (    \/| (      
| || || || (___) || |   ) | \ (_) / | (__    | |      
| |(_)| ||  ___  || |   | |  \   /  |  __)   | |      
| |   | || (   ) || |   ) |   ) (   | (      | |      
| )   ( || )   ( || (__/  )   | |   | (____/\| (____/\
|/     \||/     \|(______/    \_/   (_______/(_______/
                                                      
"""

def load_proxies_from_file(filename="proxy.txt"):
    """Load proxies from file (format: ip:port)"""
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File {filename} not found. Create one with authorized proxy addresses.")
        return []

class LoadTester(threading.Thread):
    def __init__(self, target_url, proxies, thread_id, requests_per_thread=1):
        threading.Thread.__init__(self)
        self.target_url = target_url
        self.proxies = proxies
        self.thread_id = thread_id
        self.requests_per_thread = requests_per_thread
        self.user_agent = UserAgent().random
        self.running = True

    def stop(self):
        self.running = False

    def create_request(self):
        host = self.target_url.replace("http://", "").replace("https://", "").split('/')[0]
        return (
            f"GET {self.target_url} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: {self.user_agent}\r\n"
            "Connection: close\r\n\r\n"
        )

    def run(self):
        proxy = random.choice(self.proxies) if self.proxies else None
        request = self.create_request()

        for _ in range(self.requests_per_thread):
            if not self.running:
                break

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)

                if proxy:
                    proxy_host, proxy_port = proxy.split(':')
                    print(f"[Thread {self.thread_id}] Using proxy: {proxy}")
                    s.connect((proxy_host, int(proxy_port)))
                else:
                    s.connect((socket.gethostbyname(self.target_url), 80))

                s.send(request.encode())
                response = s.recv(1024)
                print(f"[Thread {self.thread_id}] Response: {response[:100]}...")
                s.close()

            except Exception as e:
                print(f"[Thread {self.thread_id}] Error: {str(e)}")
            finally:
                time.sleep(random.uniform(0.1, 1.0))  # Realistic throttling

def main():
    print(BANNER)
    print("Professional Load Testing Tool")
    print("Use only on authorized systems!\n")

    # Configuration
    target_url = input("Enter target URL (e.g., http://example.com): ").strip()
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    try:
        num_threads = int(input("Threads (1-100): "))
        num_threads = max(1, min(num_threads, 100))  # Safety limit
    except ValueError:
        num_threads = 10

    try:
        requests_per_thread = int(input("Requests per thread (1-10): "))
        requests_per_thread = max(1, min(requests_per_thread, 10))
    except ValueError:
        requests_per_thread = 1

    # Proxy configuration (optional)
    use_proxies = input("Use proxies? (y/n): ").lower() == 'y'
    proxies = load_proxies_from_file() if use_proxies else []

    # Start test
    print(f"\nStarting test on {target_url} with {num_threads} threads...")
    threads = []
    try:
        for i in range(num_threads):
            t = LoadTester(target_url, proxies, i, requests_per_thread)
            t.start()
            threads.append(t)
            time.sleep(0.1)  # Stagger thread starts

        input("\nPress Enter to stop test...\n")
    finally:
        print("Stopping threads...")
        for t in threads:
            t.stop()
        for t in threads:
            t.join()
        print("Test completed.")

if __name__ == "__main__":
    main()