# Flask
# threading
from flask import Flask
from threading import Thread
import random

app = Flask('')

@app.route('/')

def home():
    return 'ok'

def run():
    app.run(
        host = '0.0.0.0',
        port = random.randint(2000,9000)
    )

def keep_live():
    t = Thread(target = run)
    t.start()