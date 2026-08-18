# Sends an email alert for each new job listing found. Credentials come from
# a local .env file (see load_dotenv) so secrets never get committed.
import smtplib, os, sqlite3
from dotenv import load_dotenv

load_dotenv()

SMTP_ADDRESS = os.environ.get('SMTP_ADDRESS')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECIEVER = os.environ.get('RECIEVER')
FRIEND_EMAIL = os.environ.get('FRIEND_EMAIL')
PORT = os.environ.get('PORT')


def _send(subject, body, to=None):
    print("sending email...")
    to_addrs = to or [RECIEVER, FRIEND_EMAIL]
    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=PORT) as connection:
            connection.starttls()  #encrypt message
            connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_ADDRESS,
                to_addrs=to_addrs,
                msg=f"Subject: {subject}\n\n{body}".encode("utf-8")
            )
        print("email sent!")
    except Exception as e:
        # swallow errors so one failed email doesn't crash the whole scrape run
        print(f"FAILED to send: {e}")


def send_email(job, to=None):
    subject = f"New Job: {job['title']}"
    body = f"Listing:  {job['title']} — {job['date']} — {job['link']}"
    _send(subject, body, to=to)


def send_backlog_to_friend(db_path, friend_email):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT title, date_posted, link FROM job_listings")
    rows = cur.fetchall()
    conn.close()

    subject = f"Job backlog: {len(rows)} listings"
    body = "\n\n".join(f"{title} — {date} — {link}" for title, date, link in rows)
    _send(subject, body, to=friend_email)