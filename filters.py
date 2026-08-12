import re
from datetime import date, timedelta
from dateutil import parser as date_parser

# Listings older than this are filtered out by is_recent().
MAX_AGE_DAYS = 60

# Job titles containing any of these (case-insensitive) are considered relevant.
# Edit this list to change what gets scraped/emailed.
TARGET_KEYWORDS = [
    "Entry Level",
    "Junior",
    "Associate",
    "Graduate",
    "Automation",
    "Quality Assurance",
    "Security Engineer",
    "Information Security",
    "Database",
    "SQL",
    "Cloud",
    "DevOps",
    "AWS",
    "Site Reliability",
    "Infrastructure",
    "Help Desk",
    "Technical Support",
    "Network",
    "Desktop Support",
    "Developer",
    "Programmer",
    "Full Stack",
    "Front End",
    "Back End",
    "Web Developer",
    "software",
    "data",
    "cad",
    "atc",
    "Analyst",
    "Systems",
    "Cyber",
]
def is_relevant(title):
    # Substring match, not whole-word — e.g. "software" also matches "Software Engineer".
    return any(keyword.lower() in title.lower() for keyword in TARGET_KEYWORDS)

RELATIVE_UNITS = {
    "hour": 1 / 24, "hours": 1 / 24,
    "day": 1, "days": 1,
    "week": 7, "weeks": 7,
    "month": 30, "months": 30,
}

def is_recent(date_str, max_age_days=MAX_AGE_DAYS):
    """True if date_str is within max_age_days, or if it can't be parsed (unknown dates pass)."""
    if not date_str:
        return True

    relative_match = re.search(r"(\d+)\s*(hour|hours|day|days|week|weeks|month|months)\s*ago", date_str, re.IGNORECASE)
    if relative_match:
        amount = int(relative_match.group(1))
        unit_days = RELATIVE_UNITS[relative_match.group(2).lower()]
        return amount * unit_days <= max_age_days

    try:
        parsed = date_parser.parse(date_str, fuzzy=True).date()
    except (ValueError, OverflowError):
        return True  # unparseable date — don't filter it out

    return date.today() - parsed <= timedelta(days=max_age_days)