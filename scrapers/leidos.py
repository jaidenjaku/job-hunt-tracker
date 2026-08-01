from bs4 import BeautifulSoup
import time


def get_leidos_listings(driver, url=""):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", class_="jobs-section__item")

    jobs = []
    for item in listings:
        job_element = item.find("")
        job_location = item.find("", class_="")
        date_posted = item.find("", class_="")
        if job_element and job_location and date_posted:
            jobs.append({
                "title": job_element.text.strip(),
                "link": job_element["href"],
                "location": " ",
                "date": " ",
            })
    return jobs