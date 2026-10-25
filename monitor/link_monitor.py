import time

link_load = {}
previous_stats = {}

LINK_SPEED_BPS = 10_000_000  # 10 Mbps default

def calculate_utilization(bytes_delta, interval, link_speed_bps):
    if interval <= 0 or link_speed_bps <= 0:
        return 0.0

    bits_per_second = (bytes_delta * 8) / interval
    utilization = bits_per_second / link_speed_bps
    return min(max(utilization, 0.0), 1.0)


def update_port_stats(switch_id, port_no, rx_bytes, tx_bytes, timestamp=None):
    if timestamp is None:
        timestamp = time.monotonic()

    key = (switch_id, port_no)
    current_bytes = rx_bytes + tx_bytes

    if key in previous_stats:
        old_bytes, old_time = previous_stats[key]
        interval = timestamp - old_time
        byte_delta = max(0, current_bytes - old_bytes)

        link_load[key] = calculate_utilization(
            byte_delta, interval, LINK_SPEED_BPS
        )

    previous_stats[key] = (current_bytes, timestamp)


def main():
    print("Link monitor helper ready.", flush=True)
    print("Waiting for OpenFlow port statistics integration.", flush=True)

    while True:
        print("Current link loads:", link_load, flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()
