from bs4 import BeautifulSoup
import time, random


def get_leidos_listings(driver, url="https://careers.leidos.com/search/job-level/college/jobs"):
    driver.get(url)
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
                "location": list(job_location.stripped_strings)[-1],
                "date": "No da",
                "source": "Leidos",
            })
    return jobs