from scrapers.driver import build_driver
from scrapers.leidos import get_leidos_listings
from scrapers.vanguard import get_vanguard_listings

driver = build_driver()
# jobs = get_leidos_listings(driver)
jobs = get_vanguard_listings(driver)
driver.quit()

print(f"Found {len(jobs)} jobs")
for job in jobs:
    print(job)