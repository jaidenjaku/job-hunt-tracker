from scrapers.driver import build_driver
from scrapers.saic import get_saic_listings
from scrapers.leidos import get_leidos_listings
from filters import is_relevant
from db import init_db, Session, add_job_if_new
from notifier import send_email


SCRAPERS = [get_saic_listings, get_leidos_listings]

def main():
    init_db()
    session = Session()
    driver = build_driver()

    all_jobs = []
    for scraper_func in SCRAPERS:
        all_jobs.extend(scraper_func(driver))

    driver.quit()

    for job in all_jobs:
        # filtering jobs
        if not is_relevant(job["title"]):
            continue
        if add_job_if_new(session, job):
            send_email(job)

if __name__ == "__main__":
    main()