import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv("PORT", "5000"))

app = Flask(__name__)


@app.route("/", methods=["GET"])
def status():
    return "app funcionando"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
