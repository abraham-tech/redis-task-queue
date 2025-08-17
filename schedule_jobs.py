from rq_scheduler import Scheduler  # Import the RQ Scheduler class
from redis import Redis  # Import Redis client
from datetime import datetime, timedelta  # For scheduling times
from tasks import print_message  # Import the task to be scheduled (make sure this exists)

# Connect to Redis (host name 'redis' comes from docker-compose service name)
redis_conn = Redis(host='redis', port=6379, db=0)

# Create a Scheduler instance, which will manage scheduled jobs
scheduler = Scheduler(connection=redis_conn)

# Schedule a job to run every minute
# - func: the function to run (must be importable by the worker)
# - args: arguments to pass to the function
# - interval: how often to repeat (in seconds)
# - repeat: how many times to repeat (None = forever)
# - scheduled_time: when to start (default: now)

job = scheduler.schedule(
    scheduled_time=datetime.utcnow(),  # Start immediately
    func=print_message,                # The function to run
    args=["Hello from the scheduled job!"],  # Arguments for the function
    interval=60,                       # Run every 60 seconds (1 minute)
    repeat=None                        # Repeat forever
)

print(f"Scheduled job {job.id} to run every minute.")  # Print confirmation
