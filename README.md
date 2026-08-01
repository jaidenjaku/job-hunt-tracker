# Job Hunt Tracker

An automated job-posting scraper and alert system, built to solve a real problem in my own job search: manually checking multiple career sites for new openings. This tool checks target sources on a schedule, filters for relevant roles, deduplicates against previously seen postings, and emails me when something genuinely new shows up.

## What it does

1. **Scrapes** job listings from target company career pages (starting with SAIC)
2. **Filters** results against a keyword list of target roles (software, cloud, devops, network, helpdesk)
3. **Deduplicates** against a persistent SQLite database, so previously seen postings never trigger a repeat alert
4. **Emails** a notification for each genuinely new, relevant listing
5. **Runs automatically** on a schedule via GitHub Actions — no manual checking required

## Why

Manually checking multiple career sites every day for entry-level software/cloud/devops roles is repetitive and easy to fall behind on. This automates that process end-to-end and gives me a running, queryable history of every relevant posting I've seen.

## Tech stack

- **Python**
- **Selenium** — browser automation for scraping (handles bot-detection on sites that block plain HTTP requests)
- **BeautifulSoup** — HTML parsing
- **SQLAlchemy** — ORM / database layer (SQLite)
- **smtplib** — email alerts
- **GitHub Actions** — scheduled, unattended execution (headless, runs Mon–Fri)

## How it works

Each run:
- Launches a headless (in CI) or visible (locally) Chrome browser via Selenium
- Scrapes current job listings from the target source
- Filters titles against a target-role keyword list
- Checks each listing's link against the database — skips anything already seen
- Inserts new listings and sends an email alert for each one
- Commits the updated database back to the repository, so state persists between scheduled runs

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with:
   ```
   SMTP_ADDRESS=your_smtp_server
   EMAIL_ADDRESS=your_email
   EMAIL_PASSWORD=your_app_password
   RECIEVER=where_to_send_alerts
   PORT=587
   ```
3. Run locally:
   ```bash
   python main.py
   ```

For automated runs, add the same values as GitHub Actions secrets (Settings → Secrets and variables → Actions), and the scheduled workflow will handle the rest.
