from flask import Flask
from threading import Thread
import os


app = Flask(__name__)


@app.route("/")
def home():

    return "Staff Bot is online"



def run():

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                8080
            )
        )
    )



def keep_alive():

    thread = Thread(
        target=run
    )

    thread.daemon = True

    thread.start()
