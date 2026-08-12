from bs4 import BeautifulSoup
import time, random

# Scrapes Booz Allen's "university" (early-career/internship) job board.

def get_boozallen_listings(driver, url="https://careers.boozallen.com/talent/university"):
    driver.get(url)
    # random delay lets the page's JS finish rendering listings before we scrape
    time.sleep(random.uniform(7, 10))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("tr")

    jobs = []
    for item in listings:
        title_cell = item.find("td", attrs={"data-th": "Title"})
        location_cell = item.find("td", attrs={"data-th": "Location"})

        if title_cell and location_cell:
            job_link = title_cell.find("a")
            if job_link:
                jobs.append({
                    "title": job_link.get_text(strip=True),
                    "link": job_link["href"],  # site uses absolute hrefs
                    "location": location_cell.get_text(strip=True),
                    "date": "No date",  # Booz Allen listing rows don't expose a post date
                    "source": "Booz Allen",
                })

    return jobs
