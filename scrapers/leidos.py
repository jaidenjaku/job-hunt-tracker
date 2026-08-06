from bs4 import BeautifulSoup
import time, random

# Scrapes Leidos's "college"-level job board (entry-level/new-grad roles).

def get_leidos_listings(driver, url="https://careers.leidos.com/search/job-level/college/jobs"):
    driver.get(url)
    # random delay lets the page's JS finish rendering listings before we scrape,
    # and avoids looking like a bot hitting the page at a fixed interval
    time.sleep(random.uniform(7, 10))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", class_="jobs-section__item")

    jobs = []
    for item in listings:
        job_element = item.find("a")
        job_location = item.find("div", class_="large-3 columns")
        if job_element and job_location:
            jobs.append({
                "title": job_element.text.strip(),
                "link": job_element["href"],
                "location": list(job_location.stripped_strings)[-1],  # last text node holds the actual location
                "date": "No da",  # Leidos listing cards don't expose a post date
                "source": "Leidos",
            })
    return jobs