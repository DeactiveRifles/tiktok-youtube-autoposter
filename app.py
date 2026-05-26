from flask import Flask, render_template
import threading
import time

app = Flask(__name__)

running = False
logs = []

def add_log(message):
    logs.append(message)
    if len(logs) > 100:
        logs.pop(0)

def background_worker():
    global running
    while running:
        add_log("Checking TikTok for new uploads...")
        time.sleep(10)

@app.route("/")
def home():
    return render_template("index.html", logs=logs, running=running)

@app.route("/start")
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=background_worker, daemon=True).start()
        add_log("Bot started")
    return render_template("index.html", logs=logs, running=running)

@app.route("/stop")
def stop():
    global running
    running = False
    add_log("Bot stopped")
    return render_template("index.html", logs=logs, running=running)

if __name__ == "__main__":
    app.run(debug=True)
