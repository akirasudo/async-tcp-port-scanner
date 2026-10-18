
# Async TCP Port Scanner

A lightweight asynchronous TCP port scanner written in Python using `asyncio`.

## Features

- Asynchronous scanning using `asyncio`
- Scan specific TCP ports or a range of ports
- Limit concurrent connections with a semaphore
- Configurable connection timeout
- Optional HTTP response inspection
- Logging with configurable verbosity
- Input validation for port numbers and arguments

## Requirements

- Python 3.9 or newer
- No external dependencies

## Usage

### Scan specific ports

```bash
python scanner.py 127.0.0.1 -p 80 443 8080
```

### Scan a range of ports

```bash
python scanner.py 127.0.0.1 --start-port 1 --end-port 1000
```

### Set a custom timeout

```bash
python scanner.py 127.0.0.1 -p 80 443 -t 3
```

### Enable verbose logging

```bash
python scanner.py 127.0.0.1 -p 80 443 --verbose
```

### Inspect HTTP responses

```bash
python scanner.py 127.0.0.1 -p 80 --banner
```

## Example Output

```text
INFO Target: 127.0.0.1
INFO Ports to scan: [8000, 8001]
INFO PORT 8000 OPEN
INFO PORT 8001 CLOSED
```

## How It Works

The scanner uses Python's `asyncio` library to perform TCP connection attempts asynchronously.

A semaphore limits the number of concurrent connections. Timeouts prevent connection attempts from waiting indefinitely.

Results are collected and displayed after all requested ports have been checked.

When HTTP inspection is enabled, the scanner sends an HTTP request and reads up to 1024 bytes of the response.

## Disclaimer

Use this tool only on systems you own or have explicit permission to test. Unauthorized scanning may violate applicable laws or policies.
