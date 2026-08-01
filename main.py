from scraper import build_driver, get_saic_listings, is_relevant
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
    if not is_relevant(title=job["title"]):
        continue

    job["source"] = "saic"
    if add_job_if_new(session, job):
        new_count += 1
        print(f"NEW: {job['title']} — {job['date']}")
        send_email(job=job)

print(f"{new_count} new listings out of {len(jobs)} found")
session.close()