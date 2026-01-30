import os

from flask import Flask
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from routes.user_routes.user_routes import users_bp


load_dotenv()

app = Flask(__name__)


CORS_ORIGINS = "*"
CORS(app, origins=CORS_ORIGINS, supports_credentials=False)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/perfil")
def perfi():
    return render_template("perfil.html")


"""rutas usuarios"""
app.register_blueprint(users_bp)


PORT = int(os.getenv("PORT", "5000"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
