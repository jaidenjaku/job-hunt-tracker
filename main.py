from scraper import build_driver, get_saic_listings
from db import init_db, Session, add_job_if_new
from notifier import send_email

init_db()

URL = "https://jobs.saic.com/search/jobs?q=entry+level+software"

driver = build_driver()
jobs = get_saic_listings(driver=driver, url=URL)
driver.quit()

session = Session()
new_count = 0
for job in jobs:
    job["source"] = "saic"
    if add_job_if_new(session, job):
        new_count += 1
        print(f"NEW: {job['title']} — {job['date']}")
        send_email(job=job)

print(f"{new_count} new listings out of {len(jobs)} found")
session.close()

# TEST DB
# session = Session()

# test_job = {
#     "title": "New Job",
#     "location": "Remote",
#     "date": "Jul 31, 2026",
#     "link": "https://NEW.com/test-job-123",
#     "source": "test"
# }

# if add_job_if_new(session, test_job):
#     message = f"Listing:  {test_job["title"]} — {test_job["date"]} — {test_job["link"]}"
#     send_email(message_body=message, job=test_job)

# session.close()
