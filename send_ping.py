from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Poll Bot#8440 is online."


def run():
    app.run(host='0.0.0.0', port=8000)


def ping():
    t = Thread(target=run)
    t.start()
