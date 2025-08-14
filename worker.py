from rq import Worker, Queue
from redis import Redis
from tasks import print_message

# List of queues to listen to
listen = ['default']
# Connect to Redis running in Docker
redis_conn = Redis(host='redis', port=6379, db=0)

if __name__ == '__main__':
    # Set up the worker to listen to the queue
    worker = Worker([Queue(name, connection=redis_conn) for name in listen], connection=redis_conn)
    worker.work()
