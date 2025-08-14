from rq import Queue
from redis import Redis
from tasks import print_message

if __name__ == "__main__":
    # Connect to Redis running in Docker
    redis_conn = Redis(host='redis', port=6379)
    # Create a queue
    q = Queue(connection=redis_conn)
    # Enqueue a job
    job = q.enqueue(print_message, 'Hello from the queue!', 'This is an extra argument!')
    print(f"Enqueued job: {job.id}")
