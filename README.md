# Redis Task Queue — Project-Based Course

Welcome! This hands-on course will guide you through building a **Background Job System** using Redis. By the end, you’ll have a portfolio-ready project that can send email notifications, generate PDF reports, and process images — all asynchronously!

---

## Table of Contents

1. [Kickoff — Setting the Stage](#1-kickoff--setting-the-stage)
2. [Task Queue Basics](#2-task-queue-basics)
3. [Real Task #1 — Send Email Notifications](#3-real-task-1--send-email-notifications)
4. [Real Task #2 — Generate PDF Reports](#4-real-task-2--generate-pdf-reports)
5. [Error Handling & Retries](#5-error-handling--retries)
6. [Scheduled Jobs](#6-scheduled-jobs)
7. [Monitoring & Admin Panel](#7-monitoring--admin-panel)
8. [Real Task #3 — Image Processing](#8-real-task-3--image-processing)
9. [Scaling & Performance](#9-scaling--performance)
10. [Final Project — Background Job System](#10-final-project--background-job-system)

---

## 1. Kickoff — Setting the Stage (with Docker)

**Goal:** Set up your environment and connect to Redis, all inside Docker containers.

### Steps

1. **Project Structure**
   ```
   redis-task-queue/
   ├── docker-compose.yml
   ├── Dockerfile
   ├── hello_redis.py
   └── ...
   ```

2. **Create a Dockerfile**
   ```dockerfile
   # Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["python", "hello_redis.py"]
   ```

3. **Create requirements.txt**
   ```
   redis
   ```

4. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     redis:
       image: redis:7
       ports:
         - "6379:6379"
     app:
       build: .
       depends_on:
         - redis
       environment:
         - REDIS_HOST=redis
       volumes:
         - .:/app
       command: python hello_redis.py
   ```

5. **Create hello_redis.py**
   ```python
   import os
   import redis
   import time

   # Wait for Redis to be ready
   time.sleep(2)

   # Use Docker service name as host
   redis_host = os.getenv('REDIS_HOST', 'localhost')
   r = redis.Redis(host=redis_host, port=6379, db=0)

   # Set a key
   r.set('greeting', 'Hello, Redis from Docker!')

   # Get the key
   value = r.get('greeting')
   print(value.decode())  # Output: Hello, Redis from Docker!
   ```
   **Notes:**
   - The Python app connects to the `redis` service defined in docker-compose.
   - `time.sleep(2)` gives Redis a moment to start up.
   - All code runs inside containers—no local installs needed!

6. **Run Everything with Docker Compose**
   ```bash
   docker-compose up --build
   ```
   - This will build the Python app image, start Redis, and run your script.
   - You should see `Hello, Redis from Docker!` in the logs.

---

**Continue to the next step using Docker for all services and scripts!**

---

## 2. Task Queue Basics

**Goal:** Build your first queue using [RQ (Redis Queue)](https://python-rq.org/).

### Steps

1. **Install RQ**
   ```bash
   pip install rq
   ```
2. **Create a Producer Script**

   `producer.py`:
   ```python
   from rq import Queue
   from redis import Redis

   # Function to be queued
   def print_message(msg):
       print(f"Worker says: {msg}")

   # Connect to Redis
   redis_conn = Redis()
   q = Queue(connection=redis_conn)

   # Enqueue the task
   job = q.enqueue(print_message, 'Hello from the queue!')
   print(f"Enqueued job: {job.id}")
   ```
   **Notes:**
   - `Queue` is the RQ queue object.
   - `enqueue` schedules a function to run in the background.

3. **Create a Worker Script**

   `worker.py`:
   ```python
   from rq import Worker, Queue, Connection
   from redis import Redis

   # Import the function to be run by the worker
   from producer import print_message

   listen = ['default']
   redis_conn = Redis()

   if __name__ == '__main__':
       with Connection(redis_conn):
           worker = Worker(list(map(Queue, listen)))
           worker.work()
   ```
   **Notes:**
   - The worker listens for jobs and executes them.
   - Import the function you want to run in the worker.

4. **Run the Queue**
   - Start Redis (if not running): `docker start redis`
   - Start the worker: `python worker.py`
   - In another terminal, enqueue a job: `python producer.py`

---

## 3. Real Task #1 — Send Email Notifications

**Goal:** Send emails in the background using the queue.

### Steps

1. **Install Email Library**
   ```bash
   pip install yagmail
   ```
2. **Configure Email (using Gmail for demo)**
   - Set up [App Passwords](https://support.google.com/accounts/answer/185833?hl=en) for Gmail.
   - Store credentials securely (e.g., in environment variables).

3. **Update Producer to Enqueue Email Jobs**

   `producer.py`:
   ```python
   from rq import Queue
   from redis import Redis
   from email_tasks import send_email

   redis_conn = Redis()
   q = Queue(connection=redis_conn)

   # Enqueue email job
   job = q.enqueue(send_email, 'to@example.com', 'Subject', 'Body text')
   print(f"Enqueued email job: {job.id}")
   ```

4. **Create Email Task**

   `email_tasks.py`:
   ```python
   import yagmail
   import os

   def send_email(to, subject, body):
       # Load credentials from environment variables
       user = os.environ['EMAIL_USER']
       password = os.environ['EMAIL_PASS']
       yag = yagmail.SMTP(user=user, password=password)
       yag.send(to=to, subject=subject, contents=body)
       print(f"Email sent to {to}")
   ```
   **Notes:**
   - Use environment variables for credentials: `export EMAIL_USER=... EMAIL_PASS=...`
   - `yagmail` simplifies sending emails with Gmail.

5. **Update Worker to Import Email Task**

   `worker.py`:
   ```python
   from rq import Worker, Queue, Connection
   from redis import Redis
   from email_tasks import send_email
   # ... existing code ...
   ```

6. **Test**
   - Start the worker: `python worker.py`
   - Enqueue an email job: `python producer.py`

---

## 4. Real Task #2 — Generate PDF Reports

**Goal:** Generate PDF files asynchronously.

### Steps

1. **Install PDF Library**
   ```bash
   pip install reportlab
   ```
2. **Create PDF Task**

   `pdf_tasks.py`:
   ```python
   from reportlab.pdfgen import canvas

   def generate_pdf(filename, text):
       c = canvas.Canvas(filename)
       c.drawString(100, 750, text)
       c.save()
       print(f"PDF generated: {filename}")
   ```

3. **Update Producer to Enqueue PDF Jobs**

   `producer.py`:
   ```python
   from pdf_tasks import generate_pdf
   # ... existing code ...
   job = q.enqueue(generate_pdf, 'report.pdf', 'This is your report!')
   print(f"Enqueued PDF job: {job.id}")
   ```

4. **Update Worker to Import PDF Task**

   `worker.py`:
   ```python
   from pdf_tasks import generate_pdf
   # ... existing code ...
   ```

5. **Test**
   - Start the worker: `python worker.py`
   - Enqueue a PDF job: `python producer.py`

---

## 5. Error Handling & Retries

**Goal:** Handle failures and retry jobs automatically.

### Steps

1. **Simulate Email Failures**
   - Modify `send_email` to raise an exception randomly:
   ```python
   import random
   def send_email(...):
       if random.random() < 0.5:
           raise Exception('Simulated failure!')
       # ... existing code ...
   ```
2. **Enable Retries in Producer**
   ```python
   from rq import Retry
   job = q.enqueue(send_email, ..., retry=Retry(max=3, interval=[10, 30, 60]))
   ```
   **Notes:**
   - `max=3` means 3 attempts.
   - `interval` sets wait times between retries.

3. **View Failed Jobs**
   - Install RQ CLI: `pip install rq-dashboard`
   - Run: `rq info` or `rq-dashboard`
   - Or, list failed jobs in Python:
   ```python
   from rq.registry import FailedJobRegistry
   registry = FailedJobRegistry('default', connection=redis_conn)
   print(registry.get_job_ids())
   ```

---

## 6. Scheduled Jobs

**Goal:** Run jobs on a schedule (like cron).

### Steps

1. **Install Scheduler**
   ```bash
   pip install rq-scheduler
   ```
2. **Schedule a Recurring Job**
   ```python
   from rq_scheduler import Scheduler
   from datetime import timedelta

   scheduler = Scheduler(connection=redis_conn)
   scheduler.schedule(
       scheduled_time=datetime.utcnow(),
       func=send_email,
       args=['to@example.com', 'Weekly Digest', 'Here is your digest!'],
       interval=604800,  # 1 week in seconds
       repeat=None
   )
   ```
   **Notes:**
   - `interval` is in seconds (604800 = 1 week).
   - `repeat=None` means repeat forever.

3. **Run the Scheduler Worker**
   ```bash
   rqscheduler &
   python worker.py
   ```

---

## 7. Monitoring & Admin Panel

**Goal:** Visualize your queues and jobs.

### Steps

1. **Install RQ Dashboard**
   ```bash
   pip install rq-dashboard
   ```
2. **Run the Dashboard**
   ```bash
   rq-dashboard
   ```
   - Visit [http://localhost:9181](http://localhost:9181)
   - See active, queued, and failed jobs in real time.

---

## 8. Real Task #3 — Image Processing

**Goal:** Process images in the background.

### Steps

1. **Install Pillow**
   ```bash
   pip install pillow
   ```
2. **Create Image Processing Task**

   `image_tasks.py`:
   ```python
   from PIL import Image

   def resize_image(input_path, output_path, size):
       with Image.open(input_path) as img:
           img = img.resize(size)
           img.save(output_path)
           print(f"Image saved to {output_path}")
   ```

3. **Update Producer to Enqueue Image Jobs**

   `producer.py`:
   ```python
   from image_tasks import resize_image
   # ... existing code ...
   job = q.enqueue(resize_image, 'input.jpg', 'output.jpg', (800, 600))
   print(f"Enqueued image job: {job.id}")
   ```

4. **Update Worker to Import Image Task**

   `worker.py`:
   ```python
   from image_tasks import resize_image
   # ... existing code ...
   ```

5. **Test**
   - Start the worker: `python worker.py`
   - Enqueue an image job: `python producer.py`

---

## 9. Scaling & Performance

**Goal:** Run multiple workers and optimize throughput.

### Steps

1. **Run Multiple Workers**
   ```bash
   python worker.py &
   python worker.py &
   # ... as many as needed
   ```
2. **Load Test**
   - Enqueue many jobs in a loop in `producer.py`:
   ```python
   for i in range(100):
       q.enqueue(print_message, f"Job {i}")
   ```
3. **Optimize Redis**
   - [Redis Performance Tuning Docs](https://redis.io/docs/management/optimization/)
   - Adjust `redis.conf` as needed.

---

## 10. Final Project — Background Job System

**Goal:** Combine all features and deploy.

### Steps

1. **Combine Email, PDF, and Image Tasks**
   - Import all tasks in `worker.py`.
   - Enqueue any job type from `producer.py`.

2. **Deploy with Docker Compose**
   - Create a `docker-compose.yml`:
   ```yaml
   version: '3'
   services:
     redis:
       image: redis
       ports:
         - "6379:6379"
     worker:
       build: .
       command: python worker.py
       depends_on:
         - redis
     scheduler:
       image: python:3
       volumes:
         - .:/app
       working_dir: /app
       command: rqscheduler
       depends_on:
         - redis
   ```
   - Add a `Dockerfile` for your worker if needed.

3. **Deploy to Cloud (Optional)**
   - [Heroku Redis](https://devcenter.heroku.com/articles/heroku-redis)
   - [Railway](https://railway.app/)

---

## Learning Tips

- **Read the code comments!** Every script is annotated to help you understand each line.
- **Experiment:** Try changing parameters, adding new tasks, or breaking things to see how error handling works.
- **Ask Questions:** If you’re stuck, search the docs or ask for help.

---

## 14-Day Challenge (Optional)

- **Day 1:** Set up Redis and test connection
- **Day 2:** Build your first queue
- **Day 3:** Add email sending
- **Day 4:** Add PDF generation
- **Day 5:** Add image processing
- **Day 6:** Handle errors and retries
- **Day 7:** Add scheduled jobs
- **Day 8:** Set up monitoring
- **Day 9:** Scale with multiple workers
- **Day 10:** Optimize performance
- **Day 11:** Refactor and clean up code
- **Day 12:** Add tests
- **Day 13:** Deploy to the cloud
- **Day 14:** Demo and document your project

---

Happy building! 🚀
# redis-task-queue
