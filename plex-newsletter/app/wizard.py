from flask import Flask, request, render_template, redirect
from dotenv import set_key
import os

app = Flask(__name__)

ENV_PATH = "/data/.env"

@app.route("/", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        for key in request.form:
            set_key(ENV_PATH, key.upper(), request.form[key])
        return redirect("/done")

    return render_template("wizard.html")

@app.route("/done")
def done():
    os.system("echo '@weekly python3 /app/newsletter.py >> /data/log.txt 2>&1' | crontab -")
    return "✅ Setup complete! You can now close this tab."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
