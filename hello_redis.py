import os
import redis
import time

# Wait a moment to ensure Redis is ready (especially important in Docker Compose)
time.sleep(2)

# Get the Redis host from environment variable, default to 'localhost' if not set
redis_host = os.getenv('REDIS_HOST', 'localhost')

# Connect to Redis server
r = redis.Redis(host=redis_host, port=6379, db=0)

# Set a key-value pair in Redis
greeting = 'Hello, Redis from Docker!'
r.set('greeting', greeting)

# Retrieve the value for the key 'greeting' from Redis
value = r.get('greeting')

# Decode the value from bytes to string and print it
print(value.decode())  # Output: Hello, Redis from Docker!
