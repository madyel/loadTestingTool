# Professional Load Testing Tool

A Python load testing tool for **authorized performance testing** of web applications.
It simulates configurable HTTP traffic using multiple threads and optional proxy support.

> **Disclaimer:** Use this tool only on systems you own or have explicit written
> permission to test. Unauthorized use may violate laws and terms of service.

---

## Features

- Multi-threaded request generation (up to 100 concurrent threads)
- HTTP and HTTPS support via the `requests` library
- Optional proxy support (via `proxy.txt`)
- Structured logging with timestamps
- Request throttling for realistic load simulation
- CLI flags for non-interactive automation
- Safe configuration limits enforced at runtime

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Installation

```bash
git clone https://github.com/yourusername/loadTestingTool.git
cd loadTestingTool
pip install -r requirements.txt
```

## Usage

### Interactive mode

```bash
python start.py
```

Follow the prompts to set the target URL, thread count, requests per thread,
and whether to use proxies.

### CLI mode

```bash
python start.py --url http://example.com --threads 20 --requests 5
```

| Flag | Description | Default |
|------|-------------|---------|
| `--url` | Target URL | prompted |
| `--threads` | Number of threads (1–100) | prompted |
| `--requests` | Requests per thread (1–10) | prompted |
| `--proxies` | Load proxies from proxy file | `false` |
| `--proxy-file` | Path to proxy file | `proxy.txt` |

### Using proxies

Create a `proxy.txt` file with one proxy per line in `ip:port` format:

```
1.2.3.4:8080
5.6.7.8:3128
```

Then run with proxy support:

```bash
python start.py --url http://example.com --proxies
```

## Sample output

```
[12:34:56] INFO Starting test on http://example.com with 10 threads (5 requests each)
[12:34:57] INFO [Thread 0] http://example.com -> HTTP 200 (1234 bytes)
[12:34:57] INFO [Thread 2] http://example.com -> HTTP 200 (1234 bytes)
[12:34:58] WARNING [Thread 5] Error: Connection timed out
[12:35:10] INFO Test completed — Success: 48 | Errors: 2
```

## Ethical guidelines

**Allowed uses**

- Testing your own servers and infrastructure
- Authorized penetration testing engagements
- Performance benchmarking with explicit permission

**Prohibited uses**

- Testing systems without explicit authorization
- Disruptive or denial-of-service attacks
- Any activity that violates applicable laws or terms of service

## License

MIT License — see [LICENSE](LICENSE) for details.
