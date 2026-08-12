# Entry point: scrapes all configured job sites, filters for relevant titles,
# stores new listings in the db, and emails an alert for each new one.
from scrapers import *
from filters import is_relevant, is_recent
from db import init_db, Session, add_job_if_new
from notifier import send_email

# Add a company's scraper function here to include it in the run.
SCRAPERS = [get_saic_listings, get_leidos_listings, get_vanguard_listings, get_boozallen_listings, get_lockheed_listings, get_northropgrumman_listings, get_caci_listings]

def main():
    init_db()
    session = Session()
    driver = build_driver()  # single shared Selenium driver reused across all scrapers

    all_jobs = []
    for scraper_func in SCRAPERS:
        all_jobs.extend(scraper_func(driver))

    driver.quit()

    print(f"\nTotal listings scraped: {len(all_jobs)}")

    relevant_count = 0
    new_count = 0

    for job in all_jobs:
        # keyword-match the title against filters.TARGET_KEYWORDS
        if not is_relevant(job["title"]):
            continue
        # drop listings older than filters.MAX_AGE_DAYS; unparseable/missing dates pass through
        if not is_recent(job["date"]):
            continue
        relevant_count += 1

        # add_job_if_new dedupes on link (see db.py); only email truly new listings
        if add_job_if_new(session, job):
            new_count += 1
            print(f"NEW: {job['title']} ({job['source']}) — email sent")
            send_email(job)

    print(f"\nRelevant listings: {relevant_count}")
    print(f"New listings (emailed): {new_count}")

if __name__ == "__main__":
    main()