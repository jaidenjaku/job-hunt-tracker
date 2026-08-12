# Scratch script for manually testing a single scraper in isolation
# (without running the full main.py pipeline / db / email steps).
from scrapers.driver import build_driver
from scrapers.leidos import get_leidos_listings
from scrapers.vanguard import get_vanguard_listings
from scrapers.boozallen import get_boozallen_listings
from scrapers.lockheed import get_lockheed_listings
from scrapers.northropgrumman import get_northropgrumman_listings
from scrapers.caci import get_caci_listings

driver = build_driver()
# jobs = get_leidos_listings(driver)  # swap which scraper to test here
# jobs = get_vanguard_listings(driver)
# jobs = get_boozallen_listings(driver)
# jobs = get_lockheed_listings(driver)
# jobs = get_northropgrumman_listings(driver)
jobs = get_caci_listings(driver)
driver.quit()

print(f"Found {len(jobs)} jobs")
for job in jobs:
    print(job)