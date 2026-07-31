from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, os

URL = "https://jobs.saic.com/search/jobs?q=entry+level+software"

options = Options()
options.add_experimental_option("detach", True)

# NOT headless on purpose — headless is one of the easiest things bot detection flags
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")

# hides the most obvious "this is automated" signal
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# chrome profile to remember the login session info
# user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
# options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=options)

driver.get(URL)
time.sleep(5)  # let the page fully load and any background checks resolve

soup = BeautifulSoup(driver.page_source, "html.parser")
listings = soup.find_all("div", class_="jobs-section__item")
print(f"Found {len(listings)} listings")

for item in listings:
    job_element = item.find("a")
    job_location = item.find("div", class_="large-4 columns")
    date_posted = item.find("div", class_="large-2 columns")
    if job_element and job_location and date_posted:
        title = job_element.text
        link = job_element["href"]

        loc_chunks = list(job_location.stripped_strings)
        location = " ".join(loc_chunks[-1].split())

        date_chunks = list(date_posted.stripped_strings)
        date = " ".join(date_chunks[-1].split())
        print(f"date: {date}")

driver.quit()