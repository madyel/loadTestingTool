#!/usr/bin/env python3
"""Professional Load Testing Tool."""

# Author: MaDyEl

import argparse
import logging
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests
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

MAX_THREADS = 100
MAX_REQUESTS_PER_THREAD = 10
REQUEST_TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_proxies(filename: str = "proxy.txt") -> list[str]:
    """Load proxies from file (format: ip:port)."""
    try:
        with open(filename) as f:
            proxies = [line.strip() for line in f if line.strip()]
        logger.info("Loaded %d proxies from %s", len(proxies), filename)
        return proxies
    except FileNotFoundError:
        logger.warning("Proxy file '%s' not found.", filename)
        return []


def send_request(url: str, proxy: str | None, ua: UserAgent) -> dict:
    """Send a single HTTP request and return result stats."""
    headers = {"User-Agent": ua.random}
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    try:
        resp = requests.get(
            url, headers=headers, proxies=proxies, timeout=REQUEST_TIMEOUT
        )
        return {"status": resp.status_code, "size": len(resp.content), "error": None}
    except requests.exceptions.RequestException as exc:
        return {"status": None, "size": 0, "error": str(exc)}


def worker(
    thread_id: int,
    url: str,
    proxies: list[str],
    requests_count: int,
    ua: UserAgent,
) -> dict[str, int]:
    """Run all requests for a single worker thread."""
    proxy = random.choice(proxies) if proxies else None
    stats: dict[str, int] = {"success": 0, "errors": 0}

    for _ in range(requests_count):
        if proxy:
            logger.debug("[Thread %d] Using proxy: %s", thread_id, proxy)

        result = send_request(url, proxy, ua)

        if result["error"]:
            logger.warning("[Thread %d] Error: %s", thread_id, result["error"])
            stats["errors"] += 1
        else:
            logger.info(
                "[Thread %d] %s -> HTTP %d (%d bytes)",
                thread_id,
                url,
                result["status"],
                result["size"],
            )
            stats["success"] += 1

        time.sleep(random.uniform(0.1, 1.0))  # Realistic throttling

    return stats


def run_test(
    url: str,
    num_threads: int,
    requests_per_thread: int,
    proxies: list[str],
) -> None:
    """Run the load test with the given configuration."""
    ua = UserAgent()
    total_success = 0
    total_errors = 0

    logger.info(
        "Starting test on %s with %d threads (%d requests each)",
        url,
        num_threads,
        requests_per_thread,
    )

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(worker, i, url, proxies, requests_per_thread, ua): i
            for i in range(num_threads)
        }
        try:
            for future in as_completed(futures):
                stats = future.result()
                total_success += stats["success"]
                total_errors += stats["errors"]
        except KeyboardInterrupt:
            logger.info("Test interrupted by user.")
            executor.shutdown(wait=False, cancel_futures=True)

    logger.info(
        "Test completed — Success: %d | Errors: %d", total_success, total_errors
    )


def _prompt_int(prompt: str, default: int, lo: int, hi: int) -> int:
    try:
        return max(lo, min(int(input(prompt)), hi))
    except ValueError:
        return default


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Professional Load Testing Tool")
    parser.add_argument("--url", help="Target URL")
    parser.add_argument(
        "--threads",
        type=int,
        help=f"Number of threads (1-{MAX_THREADS})",
    )
    parser.add_argument(
        "--requests",
        type=int,
        dest="requests_per_thread",
        help=f"Requests per thread (1-{MAX_REQUESTS_PER_THREAD})",
    )
    parser.add_argument(
        "--proxies",
        action="store_true",
        help="Load proxies from proxy file",
    )
    parser.add_argument(
        "--proxy-file",
        default="proxy.txt",
        help="Path to proxy file (default: proxy.txt)",
    )
    return parser.parse_args()


def main() -> None:
    print(BANNER)
    print("Professional Load Testing Tool")
    print("Use only on authorized systems!\n")

    args = parse_args()

    url = args.url or input("Enter target URL (e.g., http://example.com): ").strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    if not parsed.netloc:
        logger.error("Invalid URL: %s", url)
        sys.exit(1)

    if args.threads is not None:
        num_threads = max(1, min(args.threads, MAX_THREADS))
    else:
        num_threads = _prompt_int(
            f"Threads (1-{MAX_THREADS}): ", 10, 1, MAX_THREADS
        )

    if args.requests_per_thread is not None:
        requests_per_thread = max(1, min(args.requests_per_thread, MAX_REQUESTS_PER_THREAD))
    else:
        requests_per_thread = _prompt_int(
            f"Requests per thread (1-{MAX_REQUESTS_PER_THREAD}): ",
            1,
            1,
            MAX_REQUESTS_PER_THREAD,
        )

    if args.proxies:
        proxies = load_proxies(args.proxy_file)
    else:
        use_proxies = input("Use proxies? (y/n): ").lower() == "y"
        proxies = load_proxies(args.proxy_file) if use_proxies else []

    run_test(url, num_threads, requests_per_thread, proxies)


if __name__ == "__main__":
    main()
