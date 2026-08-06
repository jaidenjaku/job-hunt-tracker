from bs4 import BeautifulSoup
import time, random

# Scrapes Vanguard's "Early career" filtered job search results page.

def get_vanguard_listings(driver, url="https://www.vanguardjobs.com/job-search-results/?level[]=Early%20career"):
    driver.get(url)
    # random delay lets the page's JS finish rendering listings before we scrape
    time.sleep(random.uniform(7, 10))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", class_="job")

    jobs = []
    for item in listings:
        title_element = item.find("div", class_="jobTitle")
        date_element = item.find("div", class_="joblist-posdate")
        location_element = item.find("div", class_="joblist-location")

        if title_element and date_element and location_element:
            job_link = title_element.find("a")
            jobs.append({
                "title": job_link.get_text(strip=True),
                "link": "https://www.vanguardjobs.com" + job_link["href"],  # site uses relative hrefs
                "location": location_element.get_text(strip=True),
                "date": date_element.get_text(strip=True),
                "source": "Vanguard",
            })

    return jobs