import smtplib, os
from dotenv import load_dotenv

load_dotenv()

SMTP_ADDRESS = os.environ.get('SMTP_ADDRESS')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECIEVER = os.environ.get('RECIEVER')
PORT = os.environ.get('PORT')

def send_email(job):
    print("sending email...")
    subject = f"New Job: {job['title']}"
    body = f"Listing:  {job['title']} — {job['date']} — {job['link']}"
    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=PORT) as connection:
            connection.starttls()  #encrypt message
            connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_ADDRESS, 
                to_addrs=RECIEVER, 
                msg=f"Subject: New Job: {subject}\n\n{body}".encode("utf-8")
            )
        print("email sent!")
    except Exception as e:
        print(f"FAILED to send: {e}")