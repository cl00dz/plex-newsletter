import requests, os, smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv("/data/.env")

def get_recent():
    url = f"{os.getenv('TAUTULLI_URL')}/api/v2?apikey={os.getenv('TAUTULLI_KEY')}&cmd=get_recently_added&count=20"
    r = requests.get(url).json()
    return r["response"]["data"]["recently_added"]

def build_email(items):
    html = "<h2>🎬 New on Plex This Week</h2><ul>"
    for i in items:
        html += f"<li><b>{i['title']} ({i.get('year', '')})</b> - {i['media_type']}</li>"
    html += "</ul>"
    return html

def send_email(content):
    msg = MIMEText(content, "html")
    msg["Subject"] = "📬 Weekly Plex Update"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = os.getenv("EMAIL_TO")

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)

items = get_recent()
send_email(build_email(items))
