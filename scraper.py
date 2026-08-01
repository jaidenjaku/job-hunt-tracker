from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, os


def build_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    # options.add_argument("--start-maximized")
    # Github servers don't have displays so it runs headless. Meaning no external chrome browser pops up.
    if os.environ.get("GITHUB_ACTIONS"):
        options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=options)

def get_saic_listings(driver, url):
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


TARGET_KEYWORDS = ["software", "developer", "engineer", "IT", "help desk", "network", "cloud", "devops", "entry level", "Automation", "Junior"]

def is_relevant(title):
    return any(keyword.lower() in title.lower() for keyword in TARGET_KEYWORDS)