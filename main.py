from scrapers import *
from filters import is_relevant
from db import init_db, Session, add_job_if_new
from notifier import send_email


SCRAPERS = [get_saic_listings, get_leidos_listings, get_vanguard_listings]

def main():
    init_db()
    session = Session()
    driver = build_driver()

    all_jobs = []
    for scraper_func in SCRAPERS:
        all_jobs.extend(scraper_func(driver))

    driver.quit()

    print(f"\nTotal listings scraped: {len(all_jobs)}")

    relevant_count = 0
    new_count = 0

    for job in all_jobs:
        # filtering jobs
        if not is_relevant(job["title"]):
            continue
        relevant_count += 1

        if add_job_if_new(session, job):
            new_count += 1
            print(f"NEW: {job['title']} ({job['source']}) — email sent")
            send_email(job)

    print(f"\nRelevant listings: {relevant_count}")
    print(f"New listings (emailed): {new_count}")

if __name__ == "__main__":
    main()