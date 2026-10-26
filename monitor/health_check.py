import csv
import os
import socket
import time
from datetime import datetime

SERVERS = {
    "Server 1": ("10.0.0.1", 8080),
    "Server 2": ("10.0.0.2", 8080),
}

LOG_DIR = "results"
LOG_FILE = os.path.join(LOG_DIR, "server_health.csv")

os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "server", "alive", "latency_ms"])


def check_server(address):
    start = time.perf_counter()
    try:
        with socket.create_connection(address, timeout=2):
            latency = (time.perf_counter() - start) * 1000
            return True, round(latency, 2)
    except OSError:
        return False, None


def main():
    print("Server health monitoring started. Press Ctrl+C to stop.")
    try:
        while True:
            with open(LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f)

                for name, address in SERVERS.items():
                    alive, latency = check_server(address)
                    timestamp = datetime.now().isoformat(timespec="seconds")

                    writer.writerow([timestamp, name, alive, latency])
                    f.flush()

                    if alive:
                        print(
                            f"{name}: ALIVE | Latency: {latency} ms",
                            flush=True,
                        )
                    else:
                        print(f"{name}: DEAD", flush=True)

            print("-" * 40, flush=True)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
