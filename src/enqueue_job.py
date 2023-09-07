import os
import redis
from rq import Queue


def enqueue_jobs(values_to_increment):
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    conn = redis.from_url(redis_url)
    q = Queue(connection=conn)

    for value in values_to_increment:
        q.enqueue("worker.increment_counter", value)


if __name__ == "__main__":
    # Values to be incremented
    values_to_increment = [1, 2, 3, 4, 5]
    enqueue_jobs(values_to_increment)
