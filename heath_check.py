cd ~/cdn-project
cp monitor/health_check.py monitor/health_check.py.backup
cat > monitor/health_check.py <<'PY'
import socket
import time

SERVERS = {
    "Server 1": ("10.0.0.1", 8080),
    "Server 2": ("10.0.0.2", 8080),
}

CHECK_INTERVAL = 2
FAILURES_TO_MARK_DEAD = 2

# Shared within this Python process.
server_status = {
    name: {
        "alive": False,
        "latency_ms": None,
        "consecutive_failures": 0,
    }
    for name in SERVERS
}

def check_server(address):
    start = time.monotonic()
    try:
        with socket.create_connection(address, timeout=2):
            latency_ms = (time.monotonic() - start) * 1000
            return True, round(latency_ms, 2)
    except OSError:
        return False, None

def main():
    while True:
        for name, address in SERVERS.items():
            reachable, latency = check_server(address)
            status = server_status[name]

            if reachable:
                status["consecutive_failures"] = 0
                status["alive"] = True
                status["latency_ms"] = latency
            else:
                status["consecutive_failures"] += 1
                if status["consecutive_failures"] >= FAILURES_TO_MARK_DEAD:
                    status["alive"] = False
                    status["latency_ms"] = None

            print(
                f'{name}: {"ALIVE" if status["alive"] else "DEAD"}'
                f' | Latency: {status["latency_ms"]} ms'
                f' | Failures: {status["consecutive_failures"]}',
                flush=True,
            )

        print("-" * 45, flush=True)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
PY
