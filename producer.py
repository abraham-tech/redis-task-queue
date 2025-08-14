import time
import random
import string
from rq import Queue
from redis import Redis
from tasks import print_message, send_email, generate_pdf_report

redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

while True:
    # Enqueue print_message as before
    job1 = q.enqueue(print_message, 'Hello from the queue!', 'This is an extra argument!')
    print(f"Enqueued job: {job1.id}")

    time.sleep(1)  # Wait one second before sending the email

    # Generate a random email address
    random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@example.com"

    # Enqueue send_email example (view in MailHog web UI at http://localhost:8025)
    job2 = q.enqueue(
        send_email,
        random_email,  # Random recipient
        "Test Subject",
        "This is the body of the email."
    )
    print(f"Enqueued email job: {job2.id} to {random_email} (Check MailHog at http://localhost:8025)")

    time.sleep(1)  # Wait one second before next iteration

    # Enqueue generate_pdf_report job
    random_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".pdf"
    random_content = 'PDF Report Content: ' + ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    job3 = q.enqueue(generate_pdf_report, random_filename, random_content)
    print(f"Enqueued PDF report job: {job3.id} to generate {random_filename}")

    time.sleep(1)  # Wait one second before next iteration
