from bs4 import BeautifulSoup
import time, random

# Scrapes Northrop Grumman's job search results, pre-filtered to entry-level
# Software Engineering / IT / Data & Analytics roles.

def get_northropgrumman_listings(driver, url="https://jobs.northropgrumman.com/careers?domain=ngc.com&triggerGoButton=false&start=0&location=Bel+Air%2C+MD&pid=1340073516738&sort_by=timestamp&filter_distance=80&filter_include_remote=1&filter_include_relocation=0&filter_experience_level=Entry&filter_department=Software+Engineering%2CInformation+Technology%2CData+%26+Analytics"):
    driver.get(url)
    # random delay lets the page's JS finish rendering listings before we scrape
    time.sleep(random.uniform(7, 10))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", attrs={"data-test-id": "job-listing"})

    jobs = []
    for item in listings:
        job_link = item.find("a")
        title_element = item.find("div", class_="title-1aNJK")
        location_element = item.find("div", class_="fieldValue-3kEar")
        date_element = item.find("div", class_="subData-13Lm1")

        if job_link and title_element and location_element:
            jobs.append({
                "title": title_element.get_text(strip=True),
                "link": "https://jobs.northropgrumman.com" + job_link["href"],  # site uses relative hrefs
                "location": location_element.get_text(strip=True),
                "date": date_element.get_text(strip=True).replace("Posted ", "") if date_element else "No date",
                "source": "Northrop Grumman",
            })

    return jobs
