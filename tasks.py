from rq import get_current_job

def print_message(msg, extra):
    job = get_current_job()
    print(f"Worker says: {msg}")
    print(f"Extra info: {extra}")
    if job:
        print(f"My job ID is: {job.id}")