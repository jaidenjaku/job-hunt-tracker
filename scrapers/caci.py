from bs4 import BeautifulSoup
import time, random

# Scrapes CACI's job search results, pre-filtered to "junior" query.

def get_caci_listings(driver, url="https://searchcareers.caci.com/careers?query=junior&start=0&location=Bel+Air%2C+MD&sort_by=match&filter_distance=80&filter_include_remote=1&filter_include_relocation=0&filter_minimum_clearance_requiredto_start=none&filter_skills_category=software+%26+engineering%2Cinformation+technology%2Csupport+services%2Cintelligence+analysts"):
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
            date_text = date_element.get_text(strip=True).replace("Posted ", "") if date_element else ""
            jobs.append({
                "title": title_element.get_text(strip=True),
                "link": "https://searchcareers.caci.com" + job_link["href"],  # site uses relative hrefs
                "location": location_element.get_text(strip=True),
                "date": date_text or "No date",  # subData is often empty on CACI's board
                "source": "CACI",
            })

    return jobs
