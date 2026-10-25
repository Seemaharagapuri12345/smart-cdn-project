import socket
import time

SERVERS = {
    "Server 1": ("10.0.0.1", 8080),
    "Server 2": ("10.0.0.2", 8080),
}

def check_server(address):
    try:
        with socket.create_connection(address, timeout=2):
            return True
    except OSError:
        return False

def main():
    while True:
        for name, address in SERVERS.items():
            if check_server(address):
                print(f"{name}: ALIVE", flush=True)
            else:
                print(f"{name}: DEAD", flush=True)
        print("-" * 30, flush=True)
        time.sleep(2)

if __name__ == "__main__":
    main()
