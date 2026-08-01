from bs4 import BeautifulSoup
import time


def get_saic_listings(driver, url="https://jobs.saic.com/search/jobs?q=entry+level+software"):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", class_="jobs-section__item")

    jobs = []
    for item in listings:
        job_element = item.find("a")
        job_location = item.find("div", class_="large-4 columns")
        date_posted = item.find("div", class_="large-2 columns")
        if job_element and job_location and date_posted:
            jobs.append({
                "title": job_element.text.strip(),
                "link": job_element["href"],
                "location": " ".join(list(job_location.stripped_strings)[-1].split()),
                "date": " ".join(list(date_posted.stripped_strings)[-1].split()),
            })
    return jobs