from flask import Flask, render_template, request, redirect, flash
from utils import load_config, save_config
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'replace-with-secure-random-key'

@app.route("/", methods=["GET", "POST"])
def index():
    cfg = load_config()
    if request.method == "POST":
        cfg = {
            "tautulli_url": request.form["tautulli_url"],
            "tautulli_key": request.form["tautulli_key"],
            "email_from": request.form["email_from"],
            "email_pass": request.form["email_pass"],
            "email_to": [x.strip() for x in request.form["email_to"].split(",")],
            "smtp_server": request.form["smtp_server"],
            "smtp_port": int(request.form["smtp_port"])
        }
        save_config(cfg)
        flash("Configuration saved successfully!", "success")
        return redirect("/")
    return render_template("index.html", cfg=cfg)

@app.route("/test-email")
def test_email():
    cfg = load_config()
    if not cfg:
        flash("Please complete configuration first.", "error")
        return redirect("/")
    try:
        msg = MIMEText("This is a test email from your Plex newsletter setup.", "html")
        msg["Subject"] = "📬 Plex Newsletter – Test Email"
        msg["From"] = cfg["email_from"]
        msg["To"] = ", ".join(cfg["email_to"])

        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["email_from"], cfg["email_pass"])
            server.send_message(msg)
        flash("Test email sent successfully!", "success")
    except Exception as e:
        flash(f"Error sending test email: {e}", "error")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
