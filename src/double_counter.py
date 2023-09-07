import threading
import time

# Shared resource (counter)
counter = 0

# Lock for synchronizing access to the counter
counter_lock = threading.Lock()

# Event for pausing increment_counter
pause_event = threading.Event()


def double_counter():
    global counter
    pause_event.clear()

    with counter_lock:
        print("Doubling counter...")
        counter *= 2
        print(f"Counter doubled to: {counter}")

    pause_event.set()


if __name__ == "__main__":
    pause_event.set()
    time.sleep(5)
    double_counter()
