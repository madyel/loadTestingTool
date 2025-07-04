# Professional Load Testing Tool

A Python-based load testing tool designed for **authorized performance testing** of web applications. Simulates HTTP traffic with configurable threads and proxy support.

**Disclaimer:** Use only on systems you own or have explicit permission to test. Unauthorized use may violate laws and terms of service.

## Features

- 🚀 Multi-threaded request generation
- 🔒 Proxy support (via `proxy.txt`)
- 📊 Basic response monitoring
- ⏱️ Request throttling for realistic loads
- 🛑 Safe configuration limits (max 100 threads)

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/yourusername/load-testing-tool.git
   cd load-testing-tool
```
   
2. Install dependencies:
```bash
    pip install -r requirements.txt
```

Usage
Basic Test
```bash
python load_tester.py
```

Follow the interactive prompts to configure your test.

Using Proxies

    Create proxy.txt with your proxies (one per line):
    text

    1.2.3.4:8080
    5.6.7.8:3128

    Enable proxy support when prompted

Sample Output
```text
[Thread 5] Using proxy: 1.2.3.4:8080
[Thread 3] Response: HTTP/1.1 200 OK...
[Thread 7] Error: Connection timed out
```

Ethical Guidelines

✅ Allowed Uses

    Testing your own servers

    Authorized penetration testing

    Performance benchmarking (with permission)

❌ Prohibited Uses

    Unauthorized testing

    Disruptive attacks

    Violating any terms of service