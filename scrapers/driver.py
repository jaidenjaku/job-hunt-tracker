# Builds the shared Selenium Chrome driver used by all scrapers.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def build_driver():
    options = Options()
    options.add_experimental_option("detach", True)  # keep browser open after script exits (local debugging)
    # options.add_argument("--start-maximized")
    # spoofed UA + automation flags below help avoid basic bot detection on job sites
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Github servers don't have displays so it runs headless. Meaning no external chrome browser pops up.
    if os.environ.get("GITHUB_ACTIONS"):
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    return driver