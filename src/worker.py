import os
import threading
import time
import redis
from rq import Worker, Queue, Connection

# Shared resource (counter)
counter = 0

# Lock for synchronizing access to the counter
counter_lock = threading.Lock()

# Event for pausing increment_counter
pause_event = threading.Event()


# Function to increment the counter
def increment_counter(value_to_increment):
    global counter
    pause_event.wait()

    with counter_lock:
        print(f"Incrementing counter by {value_to_increment}...")
        counter += value_to_increment
        print(f"Counter incremented to: {counter}")
        time.sleep(5)  # Sleep for 5 seconds after each increment


if __name__ == "__main__":
    pause_event.set()  # Initially set the event to allow increment_counter to run

    # Setup RQ
    listen = ["default"]
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    conn = redis.from_url(redis_url)

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
