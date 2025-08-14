# Step 4.2: Generate PDF Reports as Background Jobs

## Short Explanation
- The producer enqueues jobs to generate PDF reports with random filenames and content.
- The worker picks up these jobs and uses the `reportlab` library to generate and save the PDF files.
- This simulates a real-world use case where reports are generated asynchronously in the background.

## Code Example

**In `tasks.py`:**
```python
def generate_pdf_report(filename, content):
    """
    Generates a PDF report with the given content and saves it to disk.
    """
    job = get_current_job()
    print(f"Generating PDF report: {filename} (Job ID: {job.id if job else 'N/A'})")
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, content)
        c.save()
        print(f"PDF report saved as {filename}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")
```

**In `producer.py`:**
```python
random_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".pdf"
random_content = 'PDF Report Content: ' + ''.join(random.choices(string.ascii_letters + string.digits, k=20))
job3 = q.enqueue(generate_pdf_report, random_filename, random_content)
print(f"Enqueued PDF report job: {job3.id} to generate {random_filename}")
```

## Where to Find the PDFs
- Generated PDF files will be saved in the working directory of the worker container (usually `/app` inside the container).
- To access them, you can copy them from the container to your host using `docker cp` or mount a volume in Docker Compose.

## Summary
- This demonstrates how to use a task queue to generate reports in the background, offloading heavy work from the main application.
