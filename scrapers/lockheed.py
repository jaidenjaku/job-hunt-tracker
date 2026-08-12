from bs4 import BeautifulSoup
import time, random

# Scrapes Lockheed Martin's job search results page.

def get_lockheed_listings(driver, url="https://www.lockheedmartinjobs.com/search-jobs/Information%20Technology%20entry%20level/21014%2C%20Bel%20Air%2C%20Harford%20County%2C%20MD/694/1/4/6252001-4361885-4357407-4348240/39x5394/-76x3564/50/2?pc=21014"):
    driver.get(url)
    # random delay lets the page's JS finish rendering listings before we scrape
    time.sleep(random.uniform(7, 10))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("li")

    jobs = []
    for item in listings:
        job_link = item.find("a", attrs={"data-job-id": True})
        if not job_link:
            continue

        title_element = job_link.find("span", class_="job-title")
        location_element = job_link.find("span", class_="job-location")
        date_element = job_link.find("span", class_="job-date-posted")

        if title_element and location_element:
            jobs.append({
                "title": title_element.get_text(strip=True),
                "link": "https://www.lockheedmartinjobs.com" + job_link["href"],  # site uses relative hrefs
                "location": location_element.get_text(strip=True),
                "date": date_element.get_text(strip=True).replace("Date Posted: ", "") if date_element else "No date",
                "source": "Lockheed Martin",
            })

    return jobs
